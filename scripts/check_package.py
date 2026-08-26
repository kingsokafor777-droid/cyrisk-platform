"""Verify that the wheel carries public typed validator source but no fixture or test content."""

from __future__ import annotations

import zipfile
from pathlib import Path


def main() -> int:
    wheels = sorted(Path("dist").glob("cyrisk_platform-0.1.0-*.whl"))
    if len(wheels) != 1:
        raise SystemExit("expected exactly one cyrisk_platform v0.1.0 wheel")
    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
    required = {
        "cyrisk_platform/__init__.py",
        "cyrisk_platform/models.py",
        "cyrisk_platform/references.py",
        "cyrisk_platform/validator.py",
        "cyrisk_platform/py.typed",
    }
    missing = required - names
    if missing:
        raise SystemExit(f"wheel missing required content: {sorted(missing)}")
    forbidden = {
        name for name in names if name.startswith("fixtures/") or name.startswith("tests/")
    }
    if forbidden:
        raise SystemExit(f"wheel contains forbidden content: {sorted(forbidden)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
