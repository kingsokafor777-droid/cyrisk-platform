# ADR 0001: Ship a reference-only platform handoff

**Status:** Accepted

The v0.1.0 platform owns reproducible handoff references and validation, not runtime operation. It
intentionally avoids cloud providers, state backends, deployment credentials, container execution,
background services, and managed telemetry. This makes its operational boundary reviewable while
leaving real environment design, authorization, network controls, secret management, and lifecycle
ownership with the deployer.
