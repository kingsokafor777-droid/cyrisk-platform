# Architecture

The platform release is a repository-local validation layer. Its Python validator reads an explicit
handoff manifest, checks a closed component inventory, verifies each declared SHA-256 format, and
computes a canonical manifest hash. It reads no network state and executes no external tool.

| Artifact | Deterministic purpose | Not performed |
|---|---|---|
| `compose.reference.yml` | Documents an opt-in local reference profile and hardened defaults. | Pulling, creating, starting, or health-checking a container. |
| `terraform/` | Validates a provider-free handoff and rejects `enable_deployment=true`. | `terraform init`, plan, apply, state access, or cloud provisioning. |
| `otel/collector.reference.yaml` | Documents fields to remove before a hypothetical file-only exporter. | Receiving, exporting, storing, or observing telemetry. |
| Validator | Verifies the local release-reference manifest. | Validating a deployed system, release provenance, or operating condition. |

The platform consumes only declared component identities and hash-shaped references. It does not
recalculate model results, inspect evidence, or create any risk/control decision.
