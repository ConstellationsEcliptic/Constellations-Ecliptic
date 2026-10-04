from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ce.runtime.reproducibility import RuntimeCapture, compare_capture_outputs


def _parse(path: Path) -> RuntimeCapture:
    raw = json.loads(path.read_text(encoding="utf-8"))
    payload = raw.get("capture", raw)
    if not isinstance(payload, dict):
        raise ValueError("capture_payload_mapping_required")
    return RuntimeCapture(
        capture_id=payload["capture_id"],
        captured_at_utc=payload["captured_at_utc"],
        platform=payload["platform"],
        python_version=payload["python_version"],
        execution_profile_id=payload["execution_profile_id"],
        execution_profile_revision=payload["execution_profile_revision"],
        source_commit=payload["source_commit"],
        source_tree_sha256_v2=payload["source_tree_sha256_v2"],
        dependency_lock_digest=payload["dependency_lock_digest"],
        runtime_image_digest=payload["runtime_image_digest"],
        timezone_bundle_digest=payload["timezone_bundle_digest"],
        ephemeris_bundle_digest=payload["ephemeris_bundle_digest"],
        native_library_sha256=payload["native_library_sha256"],
        native_runtime_version=payload["native_runtime_version"],
        swiss_source_commit=payload["swiss_source_commit"],
        calling_convention=payload["calling_convention"],
        fixtures=tuple(payload["fixtures"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate/compare CE native reproducibility captures.")
    parser.add_argument("capture", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--tolerances", type=Path)
    args = parser.parse_args()

    capture = _parse(args.capture)
    print(f"CAPTURE_VALID {capture.content_sha256()}")

    if args.reference is None:
        return 0

    reference = _parse(args.reference)
    tolerances: dict[str, Any] = {}
    if args.tolerances:
        tolerances = json.loads(args.tolerances.read_text(encoding="utf-8"))
    errors = compare_capture_outputs(reference, capture, numeric_tolerances=tolerances)
    if errors:
        for error in errors:
            print(f"PARITY_FAIL {error}")
        return 1
    print("PARITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
