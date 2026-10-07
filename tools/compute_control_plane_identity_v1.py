from __future__ import annotations

from pathlib import Path

from ce.foundation.control_plane_identity import control_plane_sha256


ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    print(control_plane_sha256(ROOT))
