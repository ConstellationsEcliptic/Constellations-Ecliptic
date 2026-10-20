from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "fixtures" / "verify_portable_source_identity.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def build_case(base: Path):
    repo = base / "authoring_repo"
    repo.mkdir(parents=True)
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.email", "ce-test@example.invalid")
    git(repo, "config", "user.name", "CE synthetic test")
    (repo / "src").mkdir()
    (repo / "scripts").mkdir()
    (repo / "README.md").write_text("Synthetic Source Foundation fixture only.\n", encoding="utf-8")
    (repo / "src/core.py").write_text("VALUE = 17\n", encoding="utf-8")
    script = repo / "scripts/run.sh"
    script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    script.chmod(0o755)
    git(repo, "add", "README.md", "src/core.py", "scripts/run.sh")
    git(repo, "commit", "-m", "synthetic source identity fixture")
    commit = git(repo, "rev-parse", "HEAD")
    tree = git(repo, "rev-parse", "HEAD^{tree}")

    snapshot = base / "source_snapshot"
    snapshot.mkdir()
    shutil.copy2(repo / "README.md", snapshot / "README.md")
    (snapshot / "src").mkdir()
    shutil.copy2(repo / "src/core.py", snapshot / "src/core.py")
    (snapshot / "scripts").mkdir()
    shutil.copy2(repo / "scripts/run.sh", snapshot / "scripts/run.sh")

    bundle = base / "source.bundle"
    git(repo, "bundle", "create", str(bundle), "--all")

    identity = {
        "schema_version": "0.4",
        "identity_algorithm": "CE_SOURCE_TREE_SHA256_V1",
        "repository": "synthetic://source-foundation-regression",
        "commit": commit,
        "git_tree_oid": tree,
        "source_tree_sha256": "",
        "tracked_file_count": 3,
        "git_object_type": "commit",
        "clean_worktree": True,
        "submodules_present": False,
    }
    # The source digest is deliberately calculated independently from the clean committed working-tree content using the defined CE V1 record convention.
    rows = []
    for rel, mode in (("README.md", "100644"), ("src/core.py", "100644"), ("scripts/run.sh", "100755")):
        payload = (repo / rel).read_bytes()
        rows.append(f"blob\t{mode}\t{rel}\t{hashlib.sha256(payload).hexdigest()}")
    rows.sort(key=lambda item: item.encode("utf-8"))
    identity["source_tree_sha256"] = hashlib.sha256(("\n".join(rows) + "\n").encode("utf-8")).hexdigest()

    identity_path = base / "identity.json"
    identity_path.write_text(json.dumps(identity, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return {
        "repo": repo,
        "bundle": bundle,
        "identity": identity_path,
        "snapshot": snapshot,
    }


def invoke(case, expected_bundle_sha=None, expected_identity_sha=None):
    command = [
        sys.executable, str(VERIFIER),
        "--bundle", str(case["bundle"]),
        "--identity", str(case["identity"]),
        "--snapshot", str(case["snapshot"]),
        "--expected-bundle-sha256", expected_bundle_sha or sha256_file(case["bundle"]),
        "--expected-identity-sha256", expected_identity_sha or sha256_file(case["identity"]),
    ]
    return subprocess.run(command, capture_output=True, text=True, check=False)


class PortableSourceIdentityVerifierTests(unittest.TestCase):
    def test_clean_snapshot_without_git_directory_passes_from_offline_bundle(self):
        with tempfile.TemporaryDirectory(prefix="ce_source_id_clean_") as td:
            case = build_case(Path(td))
            require(not (Path(case["snapshot"]) / ".git").exists(), "snapshot must not rely on a .git directory")
            result = invoke(case)
            require(result.returncode == 0, f"clean snapshot failed: {result.stdout} {result.stderr}")
            require("SOURCE_IDENTITY_CONSISTENCY_PASS_NOT_AUTHORITY" in result.stdout, "consistency result marker absent")

    def test_extra_file_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="ce_source_id_extra_") as td:
            case = build_case(Path(td))
            (Path(case["snapshot"]) / "UNTRACKED.txt").write_text("extra\n", encoding="utf-8")
            result = invoke(case)
            require(result.returncode == 2, f"extra file accepted: {result.stdout}")
            require("source snapshot file-set mismatch" in result.stdout, f"unexpected rejection: {result.stdout}")

    def test_modified_source_content_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="ce_source_id_content_") as td:
            case = build_case(Path(td))
            (Path(case["snapshot"]) / "src/core.py").write_text("VALUE = 18\n", encoding="utf-8")
            result = invoke(case)
            require(result.returncode == 2, f"modified source accepted: {result.stdout}")
            require("source snapshot content mismatch" in result.stdout, f"unexpected rejection: {result.stdout}")

    def test_executable_mode_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="ce_source_id_mode_") as td:
            case = build_case(Path(td))
            if os.name != "posix":
                self.skipTest("NOT RUN: executable-mode parity needs a POSIX runner")
            (Path(case["snapshot"]) / "scripts/run.sh").chmod(0o644)
            result = invoke(case)
            require(result.returncode == 2, f"mode mismatch accepted: {result.stdout}")
            require("executable mode mismatch" in result.stdout, f"unexpected rejection: {result.stdout}")

    def test_bundle_and_identity_are_independently_hash_pinned(self):
        with tempfile.TemporaryDirectory(prefix="ce_source_id_pins_") as td:
            case = build_case(Path(td))
            bundle_hash = sha256_file(case["bundle"])
            identity_hash = sha256_file(case["identity"])
            with Path(case["bundle"]).open("ab") as handle:
                handle.write(b"tamper")
            result = invoke(case, expected_bundle_sha=bundle_hash, expected_identity_sha=identity_hash)
            require(result.returncode == 2, f"modified bundle accepted: {result.stdout}")
            require("Git bundle SHA-256 does not match external pin" in result.stdout, f"unexpected rejection: {result.stdout}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
