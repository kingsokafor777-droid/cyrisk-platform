# Release Governance

## Candidate: v0.1.0

| Item | Verified local value |
|---|---|
| Package | `cyrisk-platform` v0.1.0 |
| Core compatibility pin | `cyrisk-core` commit `4d68f385ef382a6420466dff0196244a2c915f1f` |
| Handoff schema | `cyrisk.platform/v1` |
| Synthetic handoff SHA-256 | `98b8502866059b18415e2807245c8afb14440d10640b14f9a4e561b92271d292` |
| Expected validation SHA-256 | `5e1a1308a440d886458d8bbbd46eb9fad542e4cdecbc9166e60839624311d31e` |
| Local behavioral result | `make check` passed: fixture reproducibility, Ruff, strict mypy, 11 tests, 96.64% branch-aware coverage, and local source-reference checks |
| Wheel SHA-256 | `b3725a029bbd03e402bfb1522b420d7461413cd935417dbfebfed81d907b7307` |

Publication remains approval-gated. After explicit approval, the procedure must create the public
repository, tag the reviewed commit, attach the verified wheel, wait for successful hosted
`Quality`, Python 3.10–3.13, and `Analyze Python` checks, retrieve exact check contexts, apply the
protected-main policy, and synchronize the profile and program ledger.

This candidate validates local source references and a fictional closed-inventory manifest. It does
not execute Docker, Compose, Terraform, OpenTelemetry, a runtime process, a deployment, or any
cloud/credential/network integration. It does not verify a deployed environment, component
provenance, security posture, telemetry behavior, service health, authorization, or a risk decision.
A successful CodeQL workflow must not be used to claim a code-scanning-alert count without an
accessible platform result.
