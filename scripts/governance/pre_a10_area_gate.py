#!/usr/bin/env python3
"""Read-only validator for the CE pre-A10 review register.

This tool reports review status; it never authorizes Runtime Adoption, production,
deployment, or SEAL. Standard-library only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = {
    "NOT_STARTED",
    "SOURCE_REVIEW_IN_PROGRESS",
    "SOURCE_RECONCILED",
    "RECOMMENDATION_READY",
    "OWNER_DISCUSSION_REQUIRED",
    "OWNER_DECISION_RECORDED",
    "CLOSED_PRESERVE",
    "DEFERRED_BY_EXPLICIT_DISPOSITION",
}
COMPLETE_STATUSES = {
    "OWNER_DECISION_RECORDED",
    "CLOSED_PRESERVE",
    "DEFERRED_BY_EXPLICIT_DISPOSITION",
}
REVIEW_FIELDS = ("review_summary", "evidence_refs")


class RegisterError(ValueError):
    """The register is malformed or inconsistent."""


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_register(data: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(data, dict):
        raise RegisterError("register root must be a JSON object")

    if data.get("schema_version") != "1.0":
        errors.append("schema_version must equal '1.0'")
    if data.get("project") != "CONSTELLATIONS ECLIPTIC":
        errors.append("project identifier is missing or incorrect")
    if data.get("classification") != "WORKING_CONTROL_PLANE_CANDIDATE_NON_AUTHORITATIVE":
        errors.append("classification must remain non-authoritative")
    for field in ("authority_effect", "normative_effect", "runtime_authorization_effect"):
        if data.get(field) != "NONE":
            errors.append(f"{field} must remain 'NONE'")
    if data.get("a10_authorized") is not False:
        errors.append("a10_authorized must remain false in this register")

    areas = data.get("areas")
    if not isinstance(areas, list) or not areas:
        errors.append("areas must be a non-empty array")
        areas = []

    ids: set[str] = set()
    incomplete: list[str] = []
    complete: list[str] = []

    for idx, area in enumerate(areas):
        prefix = f"areas[{idx}]"
        if not isinstance(area, dict):
            errors.append(f"{prefix} must be an object")
            continue

        area_id = area.get("id")
        if not _nonempty(area_id):
            errors.append(f"{prefix}.id is required")
            area_id = f"<missing-{idx}>"
        elif area_id in ids:
            errors.append(f"duplicate area id: {area_id}")
        ids.add(area_id)

        title = area.get("title")
        if not _nonempty(title):
            errors.append(f"{area_id}.title is required")

        status = area.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{area_id}.status is not an allowed status")
            status = "NOT_STARTED"

        source_refs = area.get("source_refs")
        if not isinstance(source_refs, list) or not source_refs or not all(_nonempty(x) for x in source_refs):
            errors.append(f"{area_id}.source_refs must contain at least one explicit source reference")

        owner_required = area.get("owner_decision_required")
        if not isinstance(owner_required, bool):
            errors.append(f"{area_id}.owner_decision_required must be boolean")
            owner_required = True

        summary = area.get("review_summary")
        evidence_refs = area.get("evidence_refs")
        is_closed_status = status in COMPLETE_STATUSES
        has_summary = _nonempty(summary)
        has_evidence = isinstance(evidence_refs, list) and len(evidence_refs) > 0 and all(_nonempty(x) for x in evidence_refs)

        disposition_ref = area.get("disposition_ref")
        owner_disposition = area.get("owner_disposition")

        if status == "OWNER_DECISION_RECORDED" and not (_nonempty(disposition_ref) and _nonempty(owner_disposition)):
            errors.append(f"{area_id}: OWNER_DECISION_RECORDED requires disposition_ref and owner_disposition")
        if status == "DEFERRED_BY_EXPLICIT_DISPOSITION" and not (_nonempty(disposition_ref) and _nonempty(owner_disposition)):
            errors.append(f"{area_id}: DEFERRED_BY_EXPLICIT_DISPOSITION requires explicit disposition reference")
        if owner_required and status == "CLOSED_PRESERVE":
            errors.append(f"{area_id}: owner decision is required; use OWNER_DECISION_RECORDED or explicit deferral")
        if is_closed_status and not has_summary:
            errors.append(f"{area_id}: completed status requires review_summary")
        if is_closed_status and not has_evidence:
            errors.append(f"{area_id}: completed status requires evidence_refs")

        if is_closed_status and has_summary and has_evidence:
            if owner_required and status not in {"OWNER_DECISION_RECORDED", "DEFERRED_BY_EXPLICIT_DISPOSITION"}:
                incomplete.append(area_id)
            elif status in {"OWNER_DECISION_RECORDED", "DEFERRED_BY_EXPLICIT_DISPOSITION"} and not (
                _nonempty(disposition_ref) and _nonempty(owner_disposition)
            ):
                incomplete.append(area_id)
            else:
                complete.append(area_id)
        else:
            incomplete.append(area_id)

    if errors:
        raise RegisterError("; ".join(errors))

    review_complete = len(areas) > 0 and not incomplete
    return {
        "document_id": data.get("document_id"),
        "area_count": len(areas),
        "complete_count": len(complete),
        "incomplete_count": len(incomplete),
        "incomplete_area_ids": incomplete,
        "pre_a10_area_review": "COMPLETE" if review_complete else "INCOMPLETE",
        "a10_runtime_adoption": "NOT_AUTHORIZED_BY_THIS_TOOL",
        "production_authorization": "NOT_AUTHORIZED_BY_THIS_TOOL",
        "seal": "NOT_AUTHORIZED_BY_THIS_TOOL",
        "authority_effect": "NONE",
        "errors": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register", type=Path, help="path to the pre-A10 area register JSON")
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="return exit status 2 when the review register is valid but incomplete",
    )
    args = parser.parse_args(argv)

    try:
        with args.register.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        report = validate_register(data)
    except (OSError, json.JSONDecodeError, RegisterError) as exc:
        print(json.dumps({"validation": "INVALID", "error": str(exc)}, indent=2))
        return 1

    print(json.dumps(report, indent=2))
    if args.require_complete and report["pre_a10_area_review"] != "COMPLETE":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
