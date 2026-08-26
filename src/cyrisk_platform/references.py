"""Local source-text checks for reference artifacts; no orchestration tool is invoked."""

from __future__ import annotations

from pathlib import Path


class ReferenceValidationError(ValueError):
    """A required reference-only boundary is absent or a forbidden execution cue is present."""


def _require_contains(content: str, expected: str, label: str) -> None:
    if expected not in content:
        raise ReferenceValidationError(f"missing_{label}")


def validate_reference_files(root: Path) -> tuple[str, ...]:
    """Check local Compose, Terraform, and telemetry references without executing tools."""

    compose = (root / "compose.reference.yml").read_text(encoding="utf-8")
    terraform = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted((root / "terraform").glob("*.tf"))
    )
    telemetry = (root / "otel" / "collector.reference.yaml").read_text(encoding="utf-8")
    _require_contains(compose, "profiles: [reference]", "compose_profile")
    _require_contains(compose, "127.0.0.1:", "loopback_port")
    _require_contains(compose, "read_only: true", "read_only")
    _require_contains(terraform, "var.enable_deployment == false", "deployment_guard")
    _require_contains(terraform, 'providers         = "none"', "provider_free_output")
    if 'provider "' in terraform or 'resource "' in terraform:
        raise ReferenceValidationError("terraform_execution_surface_present")
    for attribute in ("enduser.id", "http.request.header.authorization", "cyrisk.evidence.payload"):
        _require_contains(telemetry, attribute, "telemetry_minimization")
    return ("compose", "terraform", "telemetry")
