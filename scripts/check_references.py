"""Run local source-text checks for platform references without executing their tools."""

from __future__ import annotations

from pathlib import Path

from cyrisk_platform.references import validate_reference_files


def main() -> int:
    validate_reference_files(Path(__file__).resolve().parents[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
