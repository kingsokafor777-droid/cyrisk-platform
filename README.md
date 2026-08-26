# Cyrisk Platform

> **A deterministic source-release handoff for Cyrisk platform references—not a live deployment, infrastructure provisioner, managed service, persistent runtime, container registry, cloud integration, telemetry collector, or operational authorization system.**

`cyrisk-platform` validates a narrow repository-local handoff manifest and ships reference-only
Compose, provider-free Terraform, telemetry-minimization, CI/release, security, and operator
documentation. It is designed to make a source release reviewable without implying that containers,
Terraform, databases, identities, cloud resources, or services have been started or configured.

| Handoff surface | Included reference | Explicit boundary |
|---|---|---|
| Compose | A disabled-by-default local profile and loopback-only port pattern. | No image is pulled, container started, credential injected, or service exposed. |
| Terraform | Provider-free validation module with no resources and an explicit deployment guard. | No cloud account, state backend, plan, or apply is included. |
| Telemetry | Data-minimization policy and local file-only example. | No collector is operated and no event data is exported. |
| CI/CD | Immutable workflow pins, release checks, and source-release policy. | No credentialed deployment or environment promotion exists. |
| Operator material | Threat model, ADRs, verification and incident handoff runbooks. | Deployers own operating procedures and all actions in real environments. |

The release pins [`cyrisk-core` v0.1.0](https://github.com/kingsokafor777-droid/cyrisk-core/releases/tag/v0.1.0)
commit `4d68f385ef382a6420466dff0196244a2c915f1f` only for canonical deterministic
manifest hashing. No production service or risk-decision capability is implemented or claimed.
