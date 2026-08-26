"""Deliberately generate the expected output for the sealed fictional handoff fixture."""

from __future__ import annotations

import json
from pathlib import Path

from cyrisk_platform.models import PlatformHandoffManifest
from cyrisk_platform.validator import validate_manifest

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "fixtures" / "synthetic_handoff.json"
EXPECTED_PATH = ROOT / "fixtures" / "expected_validation.json"


def main() -> int:
    manifest = PlatformHandoffManifest.model_validate_json(INPUT_PATH.read_text(encoding="utf-8"))
    expected = validate_manifest(manifest).model_dump(mode="json")
    EXPECTED_PATH.write_text(
        json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
