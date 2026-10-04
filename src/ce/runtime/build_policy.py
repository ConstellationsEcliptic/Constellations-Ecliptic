from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


FORBIDDEN_BUILD_TOKENS = (
    "-ffast-math",
    "-Ofast",
    "/fp:fast",
    "/fp:except",
    "fast-math",
)
FORBIDDEN_RUNTIME_DOWNLOAD_TOKENS = (
    "pip install http",
    "curl http",
    "wget http",
    "requests.get(",
    "urllib.request.urlretrieve",
)


@dataclass(frozen=True)
class BuildPolicyFinding:
    path: str
    token: str
    category: str


def scan_build_policy(root: Path) -> tuple[BuildPolicyFinding, ...]:
    findings: list[BuildPolicyFinding] = []
    candidates = list((root / "build").rglob("*")) + list((root / "tools").rglob("*"))
    for path in candidates:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lowered = text.lower()
        for token in FORBIDDEN_BUILD_TOKENS:
            if token.lower() in lowered:
                findings.append(BuildPolicyFinding(path.relative_to(root).as_posix(), token, "FLOATING_POINT"))
        for token in FORBIDDEN_RUNTIME_DOWNLOAD_TOKENS:
            if token.lower() in lowered:
                findings.append(BuildPolicyFinding(path.relative_to(root).as_posix(), token, "RUNTIME_DOWNLOAD"))
    return tuple(findings)
