from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "fixtures" / "validate_source_authority_r1_hardened.py"
EXPECTED_SOURCE_SHA256 = "ed1b1129f812235722b159e41f72a134aeac79f1d8c8d37cc590d456bb744e34"
EXPECTED_SOURCE_SIZE = 5226


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def expected_aggregate(rows: dict[str, str]) -> str:
    payload = "\n".join(f"{name} {digest}" for name, digest in sorted(rows.items())) + "\n"
    return sha256_bytes(payload.encode("utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


def build_synthetic_subject(root: Path) -> dict[str, object]:
    """Build only a synthetic test fixture. It is not CE canonical upstream data."""
    root.mkdir(parents=True, exist_ok=True)

    h8_bytes = b"SYNTHETIC TEST FIXTURE: source-authority parent\n"
    lock_bytes = b"SYNTHETIC TEST FIXTURE: canonical-lock bytes\n"
    h8_hash = sha256_bytes(h8_bytes)
    lock_hash = sha256_bytes(lock_bytes)

    (root / "evidence/parent/CE_V1_H8_FULL_CHAIN_REHARDENED_R2-2026-09-23.zip").parent.mkdir(
        parents=True, exist_ok=True
    )
    (root / "evidence/parent/CE_V1_H8_FULL_CHAIN_REHARDENED_R2-2026-09-23.zip").write_bytes(h8_bytes)
    (root / "evidence/canonical-data/canonical-data-lock.rev4-h3-truth-repaired.yaml").parent.mkdir(
        parents=True, exist_ok=True
    )
    (root / "evidence/canonical-data/canonical-data-lock.rev4-h3-truth-repaired.yaml").write_bytes(lock_bytes)

    ephemeris = root / "evidence/canonical-data/ephemeris"
    ephemeris.mkdir(parents=True, exist_ok=True)
    payloads = {
        "seas_18.se1": b"SYNTHETIC TEST FIXTURE seas_18.se1\n",
        "semo_18.se1": b"SYNTHETIC TEST FIXTURE semo_18.se1\n",
        "sepl_18.se1": b"SYNTHETIC TEST FIXTURE sepl_18.se1\n",
    }
    artifact_hashes: dict[str, str] = {}
    artifact_blobs: dict[str, str] = {}
    for name, payload in payloads.items():
        (ephemeris / name).write_bytes(payload)
        artifact_hashes[name] = sha256_bytes(payload)
        artifact_blobs[name] = git_blob_sha1(payload)

    aggregate = expected_aggregate(artifact_hashes)
    record = {
        "resolution_status": "PARTIAL_RESOLUTION_NOT_ESTABLISHED",
        "sealed": False,
        "authorized": False,
        "fail_closed": True,
        "parent": {
            "h8_package_sha256": h8_hash,
            "expected_h8_package_sha256": h8_hash,
            "frozen_master_sha256": "b46c52ab9a767fd2a5765f7e56e8e45f4d8404bf9c68121f3a92189f4add6542",
        },
        "canonical_lock": {
            "id": "CE-V1-CANONICAL-DATA-2026D-SE-V2.10.3BFINAL",
            "revision": 4,
            "sha256": lock_hash,
            "expected_sha256": lock_hash,
            "status": "SEAL_CANDIDATE",
        },
        "upstream_authority": {
            "iana": {
                "release": "2026d",
                "release_date": "2026-09-11",
                "commit": "d633fe7ed3de8e00ce7cac991376a064a1373bb1",
                "archive_sha256": "0cb2aa8e333c3dc049badc42a0c61f21987b8cd44e107fa900bad764aacc7767",
                "signing_primary_fingerprint": "7E3792A9D8ACF7D633BC1588ED97E90E62AA7E34",
            },
            "swisseph": {
                "repository": "https://github.com/aloistr/swisseph.git",
                "release_tag": "v2.10.3bfinal",
                "commit": "f4dcd18e8005dde95fd8a8d2312ed12f9accd1b0",
                "upstream_basis": "JPL_DE441",
                "artifact_files": {
                    name: {
                        "sha256": artifact_hashes[name],
                        "git_blob_oid_sha1": artifact_blobs[name],
                        "object_type_required": "blob",
                    }
                    for name in payloads
                },
                "canonical_aggregate_sha256": aggregate,
                "expected_canonical_aggregate_sha256": aggregate,
            },
        },
        "ce_production_source_authority": {
            "status": "NOT_ESTABLISHED",
            "repository_locator": None,
            "exact_commit": None,
            "source_tree_sha256": None,
            "approved_signer_fingerprint": None,
            "approved_keyring_sha256": None,
            "signed_source_statement": None,
        },
    }
    write_json(root / "CE_SOURCE_AUTHORITY_RECORD_R1.json", record)
    return {
        "root": root,
        "ephemeris": ephemeris,
        "hashes": artifact_hashes,
    }


def prepare_test_validator(destination: Path, fixture: dict[str, object]) -> Path:
    """Copy the hash-pinned archived validator and patch only content identities for synthetic data."""
    original = SOURCE.read_bytes()
    require(len(original) == EXPECTED_SOURCE_SIZE, f"archived validator size mismatch: {len(original)}")
    require(sha256_bytes(original) == EXPECTED_SOURCE_SHA256, "archived validator SHA-256 mismatch")

    code = original.decode("utf-8")
    root = Path(fixture["root"])
    h8_path = root / "evidence/parent/CE_V1_H8_FULL_CHAIN_REHARDENED_R2-2026-09-23.zip"
    lock_path = root / "evidence/canonical-data/canonical-data-lock.rev4-h3-truth-repaired.yaml"
    h8_hash = sha256_bytes(h8_path.read_bytes())
    lock_hash = sha256_bytes(lock_path.read_bytes())
    ephemeris = Path(fixture["ephemeris"])
    hashes = {p.name: sha256_bytes(p.read_bytes()) for p in ephemeris.iterdir() if p.is_file()}
    blobs = {p.name: git_blob_sha1(p.read_bytes()) for p in ephemeris.iterdir() if p.is_file()}
    aggregate = expected_aggregate(hashes)

    replacements = [
        (r"EXPECTED_H8='[0-9a-f]{64}'", f"EXPECTED_H8='{h8_hash}'"),
        (r"EXPECTED_LOCK='[0-9a-f]{64}'", f"EXPECTED_LOCK='{lock_hash}'"),
        (r"EXPECTED_AGG='[0-9a-f]{64}'", f"EXPECTED_AGG='{aggregate}'"),
        (
            r"EXPECTED=\{.*?\n\}",
            "EXPECTED={\n" + "".join(f" '{name}':'{digest}',\n" for name, digest in sorted(hashes.items())) + "}",
        ),
        (
            r"BLOBS=\{.*?\n\}",
            "BLOBS={\n" + "".join(f" '{name}':'{digest}',\n" for name, digest in sorted(blobs.items())) + "}",
        ),
    ]
    for pattern, replacement in replacements:
        code, count = re.subn(pattern, replacement, code, count=1, flags=re.DOTALL)
        require(count == 1, f"could not patch expected constant pattern: {pattern}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(code, encoding="utf-8")
    return destination


def invoke(validator: Path, root: Path, optimized: bool) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(validator), str(root)])
    return subprocess.run(command, capture_output=True, text=True, check=False)


class HardenedSourceAuthorityRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        raw = SOURCE.read_bytes()
        require(len(raw) == EXPECTED_SOURCE_SIZE, f"archived validator size mismatch: {len(raw)}")
        require(sha256_bytes(raw) == EXPECTED_SOURCE_SHA256, "archived validator SHA-256 mismatch")

    def _new_case(self, base: Path, case_name: str):
        case_dir = base / case_name
        fixture = build_synthetic_subject(case_dir / "subject")
        validator = prepare_test_validator(case_dir / "tools" / "validate_hardened_test_copy.py", fixture)
        return fixture, validator

    def test_pristine_synthetic_fixture_passes_in_both_modes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ce_c1_pristine_") as td:
            for optimized in (False, True):
                fixture, validator = self._new_case(Path(td), f"case_{optimized}")
                result = invoke(validator, Path(fixture["root"]), optimized)
                require(
                    result.returncode == 0,
                    f"pristine mode optimized={optimized} failed: rc={result.returncode} stdout={result.stdout} stderr={result.stderr}",
                )
                require(
                    "C1_R3_HARDENED_SOURCE_AUTHORITY_VALIDATOR_PASS" in result.stdout,
                    f"success marker absent: {result.stdout}",
                )

    def test_extra_canonical_file_is_rejected_in_both_modes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ce_c1_extra_") as td:
            for optimized in (False, True):
                fixture, validator = self._new_case(Path(td), f"case_{optimized}")
                (Path(fixture["ephemeris"]) / "UNEXPECTED.se1").write_bytes(b"unexpected synthetic extra\n")
                result = invoke(validator, Path(fixture["root"]), optimized)
                require(
                    result.returncode == 20,
                    f"extra file not rejected in mode optimized={optimized}: rc={result.returncode} stdout={result.stdout}",
                )
                require("ephemeris file-set mismatch" in result.stdout, f"unexpected failure reason: {result.stdout}")

    def test_expected_payload_symlink_is_rejected_in_both_modes(self) -> None:
        if not hasattr(os, "symlink"):
            self.skipTest("NOT RUN: Python/OS does not expose symlink creation")
        with tempfile.TemporaryDirectory(prefix="ce_c1_symlink_") as td:
            base = Path(td)
            for optimized in (False, True):
                case_base = base / f"case_{optimized}"
                fixture, validator = self._new_case(case_base, "subject_case")
                ephemeris = Path(fixture["ephemeris"])
                expected_file = ephemeris / "seas_18.se1"
                external_target = case_base / "external_same_bytes.se1"
                external_target.write_bytes(expected_file.read_bytes())
                expected_file.unlink()
                try:
                    expected_file.symlink_to(external_target)
                except (OSError, NotImplementedError) as exc:
                    self.skipTest(f"NOT RUN: symlink creation unavailable on this runner: {exc}")
                result = invoke(validator, Path(fixture["root"]), optimized)
                require(
                    result.returncode == 20,
                    f"symlink not rejected in mode optimized={optimized}: rc={result.returncode} stdout={result.stdout}",
                )
                require("symlink:" in result.stdout, f"unexpected failure reason: {result.stdout}")

    def test_canonical_payload_mutation_is_rejected_in_both_modes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ce_c1_mutation_") as td:
            for optimized in (False, True):
                fixture, validator = self._new_case(Path(td), f"case_{optimized}")
                target = Path(fixture["ephemeris"]) / "seas_18.se1"
                data = bytearray(target.read_bytes())
                data[0] ^= 0x01
                target.write_bytes(data)
                result = invoke(validator, Path(fixture["root"]), optimized)
                require(
                    result.returncode == 20,
                    f"byte mutation not rejected in mode optimized={optimized}: rc={result.returncode} stdout={result.stdout}",
                )
                require("hash mismatch" in result.stdout, f"unexpected failure reason: {result.stdout}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
