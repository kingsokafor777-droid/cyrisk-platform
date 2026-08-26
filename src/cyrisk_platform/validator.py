"""Deterministic local handoff-manifest validation with no external execution."""

from __future__ import annotations

from .models import PlatformHandoffManifest, PlatformValidationResult


class HandoffValidationError(ValueError):
    """A fail-closed handoff manifest integrity failure."""


def validate_manifest(manifest: PlatformHandoffManifest) -> PlatformValidationResult:
    """Validate and seal only a closed reference-only manifest in local memory."""

    sealed = manifest.seal() if manifest.manifest_hash is None else manifest
    if not sealed.verify_integrity():
        raise HandoffValidationError("manifest_integrity_failure")
    return PlatformValidationResult(
        manifest_hash=sealed.manifest_hash or "",
        component_ids=tuple(sorted(component.component_id for component in sealed.components)),
        reference_ids=tuple(sorted(reference.reference_id for reference in sealed.references)),
    )
