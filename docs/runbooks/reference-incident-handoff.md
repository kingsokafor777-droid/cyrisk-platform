# Runbook: Reference-incident handoff

If a deployer identifies a suspected issue while adapting these references, they should first stop
using the affected reference in their environment, preserve only permitted operational metadata,
rotate deployer-owned credentials if exposure is possible, and use their own incident process. The
source-release maintainer can receive a minimized report through private vulnerability reporting.

No repository file can validate the deployer’s environment, determine incident severity, authorize
containment, or prove remediation. Those decisions remain with the deployer and relevant incident
authority.
