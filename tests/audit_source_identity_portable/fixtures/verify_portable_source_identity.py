#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath


HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
ALGORITHM = "CE_SOURCE_TREE_SHA256_V1"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_object_oid(kind: bytes, payload: bytes) -> str:
    header = kind + b" " + str(len(payload)).encode("ascii") + b"\0"
    return hashlib.sha1(header + payload).hexdigest()


def run_git_bytes(git_dir: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "--git-dir", str(git_dir), *args],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", "replace").strip() or "git command failed"
        raise VerificationError(message)
    return result.stdout


def run_git_text(git_dir: Path, *args: str) -> str:
    return run_git_bytes(git_dir, *args).decode("utf-8", "strict").strip()


def safe_git_path(raw_path: bytes) -> str:
    try:
        value = raw_path.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-UTF-8 source path rejected") from exc
    path = PurePosixPath(value)
    require(bool(value), "empty source path rejected")
    require(not path.is_absolute(), "absolute source path rejected")
    require(".." not in path.parts and "." not in path.parts, "dot-segment source path rejected")
    require("\\" not in value, "backslash source path rejected")
    require(not any(ord(char) < 32 or ord(char) == 127 for char in value), "control character in source path rejected")
    require(not re.match(r"^[A-Za-z]:", value), "drive-qualified source path rejected")
    return value


def commit_records(git_dir: Path, commit: str) -> tuple[list[str], dict[str, tuple[str, str]]]:
    raw = run_git_bytes(git_dir, "ls-tree", "-r", "-z", "--full-tree", commit)
    records: list[str] = []
    expected: dict[str, tuple[str, str]] = {}
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        try:
            meta, raw_path = entry.split(b"\t", 1)
            mode_b, object_type, oid_b = meta.split(b" ", 2)
        except ValueError as exc:
            raise VerificationError("malformed git ls-tree record") from exc
        path = safe_git_path(raw_path)
        mode = mode_b.decode("ascii", "strict")
        require(object_type == b"blob", f"non-blob source object rejected: {path}")
        require(mode in ( "100644", "100755" ), f"unsupported source file mode rejected: {mode} {path}")
        oid = oid_b.decode("ascii", "strict")
        require(bool(HEX40.fullmatch(oid)), f"non-SHA-1 Git object ID rejected: {path}")
        blob = run_git_bytes(git_dir, "cat-file", "blob", oid)
        require(git_object_oid(b"blob", blob) == oid, f"Git blob object hash mismatch: {path}")
        content_hash = sha256_bytes(blob)
        records.append(f"blob\t{mode}\t{path}\t{content_hash}")
        require(path not in expected, f"duplicate source path rejected: {path}")
        expected[path] = (content_hash, mode)
    records.sort(key=lambda item: item.encode("utf-8"))
    return records, expected


def compute_source_tree_digest(records: list[str]) -> str:
    payload = ("\n".join(records) + "\n").encode("utf-8") if records else b""
    return sha256_bytes(payload)


def snapshot_records(snapshot: Path) -> dict[str, Path]:
    require(snapshot.exists() and snapshot.is_dir() and not snapshot.is_symlink(), "source snapshot missing or not a regular directory")
    found: dict[str, Path] = {}
    for current, dirnames, filenames in os.walk(snapshot, topdown=True, followlinks=False):
        current_path = Path(current)
        for dirname in list(dirnames):
            child = current_path / dirname
            require(not child.is_symlink(), f"symlink directory rejected: {child.relative_to(snapshot).as_posix()}")
            require(child.is_dir(), f"non-directory entry in directory list: {child.relative_to(snapshot).as_posix()}")
        for filename in filenames:
            path = current_path / filename
            rel = path.relative_to(snapshot).as_posix()
            safe_git_path(rel.encode("utf-8"))
            require(not path.is_symlink(), f"symlink source file rejected: {rel}")
            require(path.is_file(), f"non-regular source file rejected: {rel}")
            require(rel not in found, f"duplicate snapshot path rejected: {rel}")
            found[rel] = path
    return found


def verify(args: argparse.Namespace) -> dict[str, object]:
    bundle = Path(args.bundle).resolve()
    identity_path = Path(args.identity).resolve()
    snapshot = Path(args.snapshot).resolve()

    require(bundle.is_file() and not bundle.is_symlink(), "Git bundle missing or non-regular")
    require(identity_path.is_file() and not identity_path.is_symlink(), "identity statement missing or non-regular")
    require(bool(HEX64.fullmatch(args.expected_bundle_sha256)), "expected bundle SHA-256 invalid")
    require(bool(HEX64.fullmatch(args.expected_identity_sha256)), "expected identity SHA-256 invalid")
    actual_bundle_sha = sha256_file(bundle)
    actual_identity_sha = sha256_file(identity_path)
    require(actual_bundle_sha == args.expected_bundle_sha256, "Git bundle SHA-256 does not match external pin")
    require(actual_identity_sha == args.expected_identity_sha256, "identity statement SHA-256 does not match external pin")

    try:
        identity = json.loads(identity_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise VerificationError(f"identity JSON invalid: {exc}") from exc
    require(isinstance(identity, dict), "identity statement must be an object")
    require(identity.get("schema_version") == "0.4", "identity schema version mismatch")
    require(identity.get("identity_algorithm") == ALGORITHM, "identity algorithm mismatch")
    require(identity.get("clean_worktree") is True, "identity does not attest clean worktree")
    require(identity.get("submodules_present") is False, "identity does not exclude submodules")

    commit = identity.get("commit")
    require(isinstance(commit, str) and bool(HEX40.fullmatch(commit)), "identity commit must be a full SHA-1")
    expected_tree = identity.get("git_tree_oid")
    require(isinstance(expected_tree, str) and bool(HEX40.fullmatch(expected_tree)), "identity tree OID must be a full SHA-1")
    expected_digest = identity.get("source_tree_sha256")
    require(isinstance(expected_digest, str) and bool(HEX64.fullmatch(expected_digest)), "identity source-tree digest invalid")
    expected_count = identity.get("tracked_file_count")
    require(isinstance(expected_count, int) and not isinstance(expected_count, bool) and expected_count >= 0, "tracked file count invalid")

    bundle_check = subprocess.run(["git", "bundle", "verify", str(bundle)], capture_output=True, text=True, check=False)
    require(bundle_check.returncode == 0, "git bundle verify failed: " + (bundle_check.stderr.strip() or bundle_check.stdout.strip()))

    with tempfile.TemporaryDirectory(prefix="ce_source_identity_") as td:
        mirror = Path(td) / "source.git"
        clone = subprocess.run(["git", "clone", "--mirror", str(bundle), str(mirror)], capture_output=True, text=True, check=False)
        require(clone.returncode == 0, "offline Git bundle clone failed: " + (clone.stderr.strip() or clone.stdout.strip()))
        require(run_git_text(mirror, "cat-file", "-t", commit) == "commit", "pinned commit object is absent or not a commit")
        commit_payload = run_git_bytes(mirror, "cat-file", "commit", commit)
        require(git_object_oid(b"commit", commit_payload) == commit, "Git commit object hash mismatch")
        actual_tree = run_git_text(mirror, "rev-parse", f"{commit}^{{tree}}")
        require(actual_tree == expected_tree, "Git tree OID does not match pinned identity")
        tree_payload = run_git_bytes(mirror, "cat-file", "tree", actual_tree)
        require(git_object_oid(b"tree", tree_payload) == actual_tree, "Git tree object hash mismatch")
        require(run_git_text(mirror, "rev-parse", "--show-object-format") == "sha1", "unsupported Git object format")
        records, expected_files = commit_records(mirror, commit)
        actual_digest = compute_source_tree_digest(records)
        require(actual_digest == expected_digest, "source-tree SHA-256 does not match pinned identity")
        require(len(records) == expected_count, "tracked-file count does not match pinned identity")

        actual_files = snapshot_records(snapshot)
        require(set(actual_files) == set(expected_files), "source snapshot file-set mismatch")
        for rel, (expected_content_sha, expected_mode) in expected_files.items():
            path = actual_files[rel]
            actual_content_sha = sha256_file(path)
            require(actual_content_sha == expected_content_sha, f"source snapshot content mismatch: {rel}")
            executable = bool(path.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
            require(executable == (expected_mode == "100755"), f"source snapshot executable mode mismatch: {rel}")

    return {
        "status": "SOURCE_IDENTITY_CONSISTENCY_PASS_NOT_AUTHORITY",
        "commit": commit,
        "git_tree_oid": expected_tree,
        "source_tree_sha256": expected_digest,
        "tracked_file_count": expected_count,
        "bundle_sha256": actual_bundle_sha,
        "identity_sha256": actual_identity_sha,
        "authority_effect": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a source snapshot against an externally hash-pinned offline Git bundle and identity statement.")
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--identity", required=True)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--expected-bundle-sha256", required=True)
    parser.add_argument("--expected-identity-sha256", required=True)
    args = parser.parse_args()
    try:
        result = verify(args)
        print(json.dumps(result, sort_keys=True))
        print("SOURCE_IDENTITY_CONSISTENCY_PASS_NOT_AUTHORITY")
        return 0
    except Exception as exc:
        print(f"NON-AUTHORIZED: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
