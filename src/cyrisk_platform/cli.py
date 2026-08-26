"""Local JSON manifest validation command; no provision or deployment command exists."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from .models import PlatformHandoffManifest
from .validator import validate_manifest


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a reference-only Cyrisk platform manifest."
    )
    parser.add_argument("manifest", type=Path, help="Local PlatformHandoffManifest JSON path")
    args = parser.parse_args(argv)
    manifest = PlatformHandoffManifest.model_validate_json(
        args.manifest.read_text(encoding="utf-8")
    )
    print(validate_manifest(manifest).model_dump_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
