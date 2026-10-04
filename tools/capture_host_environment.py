from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import platform
import sys

from ce.foundation.hashing import sha256_file
from ce.runtime.environment_identity import (
    HOST_NATIVE_ENVIRONMENT_KIND,
    HOST_NATIVE_ENVIRONMENT_SCHEMA_VERSION,
    host_native_environment_digest,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture a content-addressed CE host-native runtime environment "
            "manifest. This is evidence-only and never authorizes runtime."
        )
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--component",
        action="append",
        default=[],
        metavar="NAME=PATH",
        help="Identity-bearing environment component. Repeatable.",
    )
    return parser


def _parse_components(values: list[str]) -> tuple[list[dict[str, object]], dict[str, str]]:
    components: list[dict[str, object]] = []
    observed_paths: dict[str, str] = {}
    names: set[str] = set()
    for raw in values:
        if "=" not in raw:
            raise ValueError("component_requires_NAME_EQUALS_PATH")
        name, raw_path = raw.split("=", 1)
        name = name.strip()
        path = Path(raw_path).expanduser().resolve()
        if not name:
            raise ValueError("component_name_empty")
        if name in names:
            raise ValueError(f"duplicate_component_name:{name}")
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"component_missing_or_nonregular:{name}")
        digest = sha256_file(path)
        components.append(
            {
                "name": name,
                "size_bytes": path.stat().st_size,
                "sha256": digest,
            }
        )
        observed_paths[name] = str(path)
        names.add(name)
    components.sort(key=lambda item: str(item["name"]))
    return components, observed_paths


def main() -> int:
    args = _parser().parse_args()
    python_executable = Path(sys.executable).resolve()
    if python_executable.is_symlink() or not python_executable.is_file():
        raise SystemExit("python_executable_missing_or_nonregular")

    components, observed_paths = _parse_components(args.component)
    uname = platform.uname()
    manifest = {
        "schema_version": HOST_NATIVE_ENVIRONMENT_SCHEMA_VERSION,
        "kind": HOST_NATIVE_ENVIRONMENT_KIND,
        "os": {
            "system": uname.system,
            "release": uname.release,
            "version": uname.version,
            "machine": uname.machine,
        },
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "platform": platform.platform(aliased=False, terse=False),
            "executable_sha256": sha256_file(python_executable),
            "executable_size_bytes": python_executable.stat().st_size,
        },
        "components": components,
    }
    digest = host_native_environment_digest(manifest)
    envelope = {
        "identity_manifest": manifest,
        "runtime_environment_digest": digest,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "observed_paths": observed_paths,
        "capture_role": "EVIDENCE_ONLY_NON_AUTHORITY",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    import json
    args.output.write_text(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
