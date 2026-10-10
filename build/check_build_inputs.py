from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for p in ROOT.rglob('*'):
 rel=p.relative_to(ROOT)
 if any(part in {'__pycache__','.pytest_cache','.mypy_cache','.ruff_cache'} for part in rel.parts) or p.suffix in {'.pyc','.pyo','.tmp'}: raise SystemExit(f'GENERATED_ARTIFACT_PRESENT: {rel.as_posix()}')
 if p.is_symlink(): raise SystemExit(f'SYMLINK_PRESENT: {rel.as_posix()}')
print('BUILD_INPUTS_CLEAN')
