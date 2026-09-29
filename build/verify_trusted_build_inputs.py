from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "build" / "trusted-build-lock.json"
ENV = ROOT / "build" / "trusted-build-environment.json"
DEP_LOCK = ROOT / "build" / "trusted-build-dependency-lock.txt"

EXPECTED_IMAGE_DIGEST = "sha256:3e2de9c40ca4e3d73240059f9d48baff27908f10293e985a2f382a0378e6df4a"
EXPECTED_PYTHON = "3.13.15"
EXPECTED_ARCH = "x86_64"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


EXPECTED_DEPENDENCY_LOCK_SHA256 = "708f9230ce520ffdfa0d0b02da5a6871d439e533e814c8722f0a89e84a0c6f8e"
EXPECTED_TRUSTED_BUILD_LOCK_SHA256 = "6f9ef3a29b69a8aa81a34b2cec7d85b6cf04b915bc8c535f8eee9e6fc6799b7c"
EXPECTED_ENVIRONMENT_RECORD_SHA256 = "5321acb42c949a5b82f679a7c26dfa84f3435103ecda0bcbbd063f262fa1da75"

EXPECTED_TRUSTED_BUILD_DEPENDENCY_LOCK = """# CE V1 Trusted Build candidate dependency lock
# Install only from pre-fetched artifacts using --no-index --require-hashes.
pip==26.2.1 \\
    --hash=sha256:71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e
setuptools==82.0.1 \\
    --hash=sha256:a59e362652f08dcd477c78bb6e7bd9d80a7995bc73ce773050228a348ce2e5bb
"""

def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    env = json.loads(ENV.read_text(encoding="utf-8"))
    if sha256(LOCK) != EXPECTED_TRUSTED_BUILD_LOCK_SHA256:
        raise SystemExit("TRUSTED_BUILD_LOCK_SHA256_MISMATCH")
    if sha256(ENV) != EXPECTED_ENVIRONMENT_RECORD_SHA256:
        raise SystemExit("ENVIRONMENT_RECORD_SHA256_MISMATCH")
    if sha256(DEP_LOCK) != EXPECTED_DEPENDENCY_LOCK_SHA256:
        raise SystemExit("DEPENDENCY_LOCK_SHA256_MISMATCH")

    actual_py = ".".join(map(str, sys.version_info[:3]))
    if actual_py != EXPECTED_PYTHON or lock["python"]["version"] != actual_py:
        raise SystemExit(f"PYTHON_VERSION_MISMATCH:{actual_py}!={EXPECTED_PYTHON}")

    actual_arch = platform.machine()
    if actual_arch != EXPECTED_ARCH or lock["python"]["architecture"] != actual_arch:
        raise SystemExit(f"ARCHITECTURE_MISMATCH:{actual_arch}!={EXPECTED_ARCH}")

    lock_env = lock["environment"]
    env_identity = env["environment_identity"]

    if lock_env["kind"] != "CONTENT_ADDRESSED_CONTAINER_IMAGE":
        raise SystemExit("LOCK_ENVIRONMENT_KIND_MISMATCH")
    if env_identity["kind"] != "CONTENT_ADDRESSED_CONTAINER_IMAGE":
        raise SystemExit("ENVIRONMENT_KIND_MISMATCH")
    if lock_env["digest"] != EXPECTED_IMAGE_DIGEST:
        raise SystemExit("LOCK_ENVIRONMENT_DIGEST_MISMATCH")
    if env_identity["base_image_digest"] != EXPECTED_IMAGE_DIGEST:
        raise SystemExit("ENVIRONMENT_BASE_DIGEST_MISMATCH")
    if env_identity["image_ref"].rsplit("@", 1)[-1] != EXPECTED_IMAGE_DIGEST:
        raise SystemExit("ENVIRONMENT_IMAGE_REF_DIGEST_MISMATCH")
    if lock_env["image_ref"].rsplit("@", 1)[-1] != EXPECTED_IMAGE_DIGEST:
        raise SystemExit("LOCK_IMAGE_REF_DIGEST_MISMATCH")
    if env["toolchain"] != {
        "python": EXPECTED_PYTHON,
        "architecture": EXPECTED_ARCH,
        "pip": "26.2.1",
        "setuptools": "82.0.1",
    }:
        raise SystemExit("ENVIRONMENT_TOOLCHAIN_MISMATCH")
    if lock["build_frontend"]["pip_wheel_sha256"] != "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e":
        raise SystemExit("LOCK_PIP_HASH_MISMATCH")
    if lock["build_backend"]["setuptools_wheel_sha256"] != "a59e362652f08dcd477c78bb6e7bd9d80a7995bc73ce773050228a348ce2e5bb":
        raise SystemExit("LOCK_SETUPTOOLS_HASH_MISMATCH")
    if env["dependency_artifacts"] != {
        "pip_26_2_1_sha256": "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e",
        "setuptools_82_0_1_sha256": "a59e362652f08dcd477c78bb6e7bd9d80a7995bc73ce773050228a348ce2e5bb",
    }:
        raise SystemExit("ENVIRONMENT_DEPENDENCY_HASH_MISMATCH")
    policy_expected = {
        "runtime_dependencies": [],
        "dependency_acquisition": "PREFETCH_OUTSIDE_BUILD_NETWORK",
        "dependency_installation": "FORCE_REINSTALL_FROM_PRE_FETCHED_HASHED_ARTIFACTS",
        "network_during_build": False,
        "source_date_epoch": 0,
        "bytecode_generation": False,
        "source_package_excludes": ["evidence/", "provenance/"],
    }
    if lock["build_policy"] != {"source_date_epoch": 0, "dependency_installation": "FORCE_REINSTALL_FROM_PRE_FETCHED_HASHED_ARTIFACTS", "network_during_build": False, "runtime_dependencies": [], "source_package_excludes": ["evidence/", "provenance/"]}:
        raise SystemExit("LOCK_BUILD_POLICY_MISMATCH")
    if env["build_policy"] != policy_expected:
        raise SystemExit("ENVIRONMENT_BUILD_POLICY_MISMATCH")
    if lock["authorization"] != {
        "trusted_build": "NOT_ESTABLISHED",
        "production_runtime": "NOT_AUTHORIZED",
        "seal": "NO",
        "authorization": "NON_AUTHORIZED",
        "fail_closed": True,
    }:
        raise SystemExit("LOCK_AUTHORIZATION_MISMATCH")
    if env["authorization"] != lock["authorization"]:
        raise SystemExit("ENVIRONMENT_AUTHORIZATION_MISMATCH")

    dep_text = DEP_LOCK.read_text(encoding="utf-8")
    if dep_text != EXPECTED_TRUSTED_BUILD_DEPENDENCY_LOCK:
        raise SystemExit("TRUSTED_BUILD_DEPENDENCY_LOCK_CONTENT_MISMATCH")
    if "pip==26.2.1" not in dep_text or "sha256:71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e" not in dep_text:
        raise SystemExit("DEPENDENCY_LOCK_PIP_ENTRY_MISMATCH")
    if "setuptools==82.0.1" not in dep_text or "sha256:a59e362652f08dcd477c78bb6e7bd9d80a7995bc73ce773050228a348ce2e5bb" not in dep_text:
        raise SystemExit("DEPENDENCY_LOCK_SETUPTOOLS_ENTRY_MISMATCH")

    if lock["build_frontend"]["pip_version"] != "26.2.1":
        raise SystemExit("PIP_VERSION_MISMATCH")
    if lock["build_backend"]["setuptools_version"] != "82.0.1":
        raise SystemExit("SETUPTOOLS_VERSION_MISMATCH")
    if lock["build_policy"]["dependency_installation"] != "FORCE_REINSTALL_FROM_PRE_FETCHED_HASHED_ARTIFACTS":
        raise SystemExit("DEPENDENCY_INSTALLATION_POLICY_MISMATCH")

    if not DEP_LOCK.is_file():
        raise SystemExit("TRUSTED_BUILD_DEPENDENCY_LOCK_MISSING")

    if lock["authorization"]["trusted_build"] != "NOT_ESTABLISHED":
        raise SystemExit("UNAUTHORIZED_TRUSTED_BUILD_STATE")

    print("TRUSTED_BUILD_INPUTS_PASS")
    print(f"PYTHON={actual_py}")
    print(f"ARCH={actual_arch}")
    print(f"IMAGE_DIGEST={EXPECTED_IMAGE_DIGEST}")
    print(f"LOCK_SHA256={sha256(LOCK)}")
    print(f"ENVIRONMENT_SHA256={sha256(ENV)}")
    print(f"DEPENDENCY_LOCK_SHA256={sha256(DEP_LOCK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
