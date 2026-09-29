from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "build" / "trusted-build-lock.json"
DEP_LOCK = ROOT / "build" / "trusted-build-dependency-lock.txt"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    expected_py = lock["python"]["version"]
    actual_py = ".".join(map(str, sys.version_info[:3]))
    if actual_py != expected_py:
        raise SystemExit(f"PYTHON_VERSION_MISMATCH:{actual_py}!={expected_py}")

    if platform.machine() != "x86_64":
        raise SystemExit(f"ARCHITECTURE_MISMATCH:{platform.machine()}!=x86_64")

    if not DEP_LOCK.is_file():
        raise SystemExit("TRUSTED_BUILD_DEPENDENCY_LOCK_MISSING")

    if lock["authorization"]["trusted_build"] != "NOT_ESTABLISHED":
        raise SystemExit("UNAUTHORIZED_TRUSTED_BUILD_STATE")

    if lock["environment_identity"]["immutable_digest"] is not None:
        raise SystemExit("UNEXPECTED_IMMUTABLE_DIGEST_VALUE")

    print("TRUSTED_BUILD_INPUTS_PASS")
    print(f"PYTHON={actual_py}")
    print(f"ARCH={platform.machine()}")
    print(f"LOCK_SHA256={sha256(LOCK)}")
    print(f"DEPENDENCY_LOCK_SHA256={sha256(DEP_LOCK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
