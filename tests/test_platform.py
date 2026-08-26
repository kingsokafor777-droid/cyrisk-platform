from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from pydantic import ValidationError

from cyrisk_platform.cli import main
from cyrisk_platform.models import PlatformHandoffManifest
from cyrisk_platform.references import ReferenceValidationError, validate_reference_files
from cyrisk_platform.validator import HandoffValidationError, validate_manifest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "synthetic_handoff.json"
EXPECTED_PATH = ROOT / "fixtures" / "expected_validation.json"


def manifest() -> PlatformHandoffManifest:
    return PlatformHandoffManifest.model_validate_json(FIXTURE_PATH.read_text(encoding="utf-8"))


def payload() -> dict[str, object]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_unsealed_and_sealed_manifests_validate_deterministically() -> None:
    first = validate_manifest(manifest())
    sealed = manifest().seal()
    second = validate_manifest(sealed)
    assert first == second
    assert first.model_dump(mode="json") == json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    assert first.deployment_executed is False
    assert len(first.component_ids) == 10


def test_validator_rejects_an_altered_declared_integrity_hash() -> None:
    sealed = manifest().seal().model_copy(update={"manifest_hash": "0" * 64})
    with pytest.raises(HandoffValidationError, match="manifest_integrity_failure"):
        validate_manifest(sealed)


@pytest.mark.parametrize(
    "mutation", ["unknown_component", "duplicate_component", "missing_component"]
)
def test_closed_component_inventory_rejects_invalid_membership(mutation: str) -> None:
    invalid = payload()
    components = invalid["components"]
    assert isinstance(components, list)
    if mutation == "unknown_component":
        components[0]["component_id"] = "other-component"
    elif mutation == "duplicate_component":
        components[1]["component_id"] = components[0]["component_id"]
    else:
        components.pop()
    with pytest.raises(ValidationError):
        PlatformHandoffManifest.model_validate(invalid)


def test_reference_only_literal_and_reference_set_fail_closed() -> None:
    invalid = payload()
    invalid["deployment_enabled"] = True
    with pytest.raises(ValidationError):
        PlatformHandoffManifest.model_validate(invalid)
    invalid = payload()
    references = invalid["references"]
    assert isinstance(references, list)
    references[0]["relative_path"] = "compose.yml"
    with pytest.raises(ValidationError, match="closed platform handoff set"):
        PlatformHandoffManifest.model_validate(invalid)


def _copy_reference_tree(destination: Path) -> None:
    destination.mkdir()
    shutil.copy(ROOT / "compose.reference.yml", destination / "compose.reference.yml")
    shutil.copytree(ROOT / "terraform", destination / "terraform")
    shutil.copytree(ROOT / "otel", destination / "otel")


def test_reference_files_validate_without_executing_tools() -> None:
    assert validate_reference_files(ROOT) == ("compose", "terraform", "telemetry")


@pytest.mark.parametrize(
    ("target", "replacement", "expected"),
    [
        ("compose.reference.yml", "profiles: [reference]", "missing_compose_profile"),
        ("terraform/versions.tf", "terraform {", 'provider "example" {}\nterraform {'),
        (
            "otel/collector.reference.yaml",
            "enduser.id",
            "missing_telemetry_minimization",
        ),
    ],
)
def test_reference_checks_reject_missing_boundary_or_execution_surface(
    tmp_path: Path, target: str, replacement: str, expected: str
) -> None:
    copied = tmp_path / "references"
    _copy_reference_tree(copied)
    path = copied / target
    path.write_text(path.read_text(encoding="utf-8").replace(replacement, ""), encoding="utf-8")
    if expected == 'provider "example" {}\nterraform {':
        path.write_text(
            'provider "example" {}\n' + path.read_text(encoding="utf-8"), encoding="utf-8"
        )
        expected = "terraform_execution_surface_present"
    with pytest.raises(ReferenceValidationError, match=expected):
        validate_reference_files(copied)


def test_cli_emits_local_validation_json(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(FIXTURE_PATH)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["deployment_executed"] is False
    assert output["component_ids"][0] == "cyrisk-audit-export"
