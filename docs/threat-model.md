# Threat Model

| Threat | Example | Mitigation and boundary |
|---|---|---|
| Accidental infrastructure creation | A reference is mistaken for a deployable module. | Terraform has no provider/resources and rejects `enable_deployment=true`. |
| Accidental exposure | A local Compose port binds publicly. | Reference pattern is profile-gated and loopback-only. |
| Telemetry leakage | Sensitive identity/evidence values pass to an exporter. | Explicit deletion policy; no collector is operated by this release. |
| Secret/state leakage | Credentials or Terraform state are committed. | Ignore rules, contribution policy, and reference checks forbid these files. |
| Operational overclaim | Source files are represented as a deployed platform. | README/release/runbooks distinguish handoff references from operating services. |
| Supply-chain ambiguity | Component identity drifts from a reviewed release. | Closed manifest inventory, hash-shaped references, immutable CI pins, and release gates. |
