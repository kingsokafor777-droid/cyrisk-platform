"""Strict contracts for a reference-only Cyrisk platform handoff manifest."""

from __future__ import annotations

from typing import Final, Literal

from cyrisk_core.canonical import content_hash
from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION: Final[Literal["cyrisk.platform/v1"]] = "cyrisk.platform/v1"
HASH_PATTERN = r"^[a-f0-9]{64}$"
ID_PATTERN = r"^[a-z][a-z0-9_-]{2,63}$"
PROGRAM_COMPONENTS: Final[frozenset[str]] = frozenset(
    {
        "cyrisk-core",
        "cyrisk-model",
        "cyrisk-evidence",
        "cyrisk-controls",
        "cyrisk-register",
        "cyrisk-ccm",
        "cyrisk-scenarios",
        "cyrisk-audit-export",
        "cyrisk-console",
        "cyrisk-platform",
    }
)
REQUIRED_REFERENCE_PATHS: Final[frozenset[tuple[str, str, str]]] = frozenset(
    {
        ("compose-reference", "compose.reference.yml", "compose"),
        ("terraform-reference", "terraform", "terraform"),
        ("telemetry-reference", "otel/collector.reference.yaml", "telemetry"),
        ("release-runbook", "docs/runbooks/release-verification.md", "runbook"),
    }
)


class StrictModel(BaseModel):
    """Fail closed on unknown fields so credentials and runtime instructions cannot enter."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class ComponentReference(StrictModel):
    """A hash-shaped declared release reference, not an attestation or remote lookup."""

    component_id: str = Field(pattern=ID_PATTERN)
    source_commit: str = Field(pattern=r"^[a-f0-9]{40}$")
    release_version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    artifact_sha256: str = Field(pattern=HASH_PATTERN)


class ReferenceArtifact(StrictModel):
    """A local path declaration with a no-execution status."""

    reference_id: str = Field(pattern=ID_PATTERN)
    relative_path: str = Field(pattern=r"^[a-z0-9_./-]+$")
    kind: Literal["compose", "terraform", "telemetry", "runbook"]
    execution_status: Literal["not_executed"] = "not_executed"


class PlatformHandoffManifest(StrictModel):
    """Full-program handoff manifest; it can only describe reference-only configuration."""

    schema_version: Literal["cyrisk.platform/v1"] = SCHEMA_VERSION
    environment_mode: Literal["reference-only"] = "reference-only"
    deployment_enabled: Literal[False] = False
    components: tuple[ComponentReference, ...] = Field(min_length=10, max_length=10)
    references: tuple[ReferenceArtifact, ...] = Field(min_length=4, max_length=4)
    limitation: str = Field(min_length=1, max_length=500)
    manifest_hash: str | None = Field(default=None, pattern=HASH_PATTERN)

    @model_validator(mode="after")
    def require_closed_program_inventory(self) -> PlatformHandoffManifest:
        component_ids = [component.component_id for component in self.components]
        if len(component_ids) != len(set(component_ids)):
            raise ValueError("component references must be unique")
        if set(component_ids) != PROGRAM_COMPONENTS:
            raise ValueError("component references must equal the closed Cyrisk program inventory")
        reference_ids = [reference.reference_id for reference in self.references]
        if len(reference_ids) != len(set(reference_ids)):
            raise ValueError("reference identifiers must be unique")
        reference_paths = {
            (reference.reference_id, reference.relative_path, reference.kind)
            for reference in self.references
        }
        if reference_paths != REQUIRED_REFERENCE_PATHS:
            raise ValueError("reference artifacts must equal the closed platform handoff set")
        return self

    def computed_hash(self) -> str:
        return content_hash(self.model_dump(mode="json", exclude={"manifest_hash"}))

    def seal(self) -> PlatformHandoffManifest:
        return self.model_copy(update={"manifest_hash": self.computed_hash()})

    def verify_integrity(self) -> bool:
        return self.manifest_hash is not None and self.manifest_hash == self.computed_hash()


class PlatformValidationResult(StrictModel):
    """Local manifest integrity outcome; it is never runtime or deployment evidence."""

    schema_version: Literal["cyrisk.platform/v1"] = SCHEMA_VERSION
    manifest_hash: str = Field(pattern=HASH_PATTERN)
    component_ids: tuple[str, ...]
    reference_ids: tuple[str, ...]
    deployment_executed: Literal[False] = False
    limitation: str = (
        "Validates only this local reference manifest; it does not verify deployed infrastructure, "
        "component provenance, security posture, runtime health, or authorization."
    )
