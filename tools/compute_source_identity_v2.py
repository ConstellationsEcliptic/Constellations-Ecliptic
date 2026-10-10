from __future__ import annotations

from pathlib import Path

from ce.foundation.source_tree_identity import source_tree_sha256

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    print(source_tree_sha256(ROOT))
