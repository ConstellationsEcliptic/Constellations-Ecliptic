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


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    env = json.loads(ENV.read_text(encoding="utf-8"))

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

    if lock["build_frontend"]["pip_version"] != "26.2.1":
        raise SystemExit("PIP_VERSION_MISMATCH")
    if lock["build_backend"]["setuptools_version"] != "82.0.1":
        raise SystemExit("SETUPTOOLS_VERSION_MISMATCH")

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
