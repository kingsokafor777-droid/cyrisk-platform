# ADR 0002: Minimize telemetry before any export

**Status:** Accepted

The reference collector configuration removes end-user identifiers, authorization headers, and a
named evidence-payload field before a hypothetical file-only exporter. This is a policy example,
not evidence that a collector removes every sensitive attribute or that any telemetry has been
processed. Deployers must assess their own attribute set, exporter, retention, encryption, access,
and lawful basis.
