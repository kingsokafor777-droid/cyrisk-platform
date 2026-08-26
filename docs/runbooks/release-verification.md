# Runbook: Source-release verification

The maintainer begins by checking the reviewed source commit, sealed fixture hash, wheel digest, and
the required hosted CI/CodeQL conclusions. The maintainer then retrieves the exact check contexts,
applies the branch-protection policy, verifies the public release target and asset, and synchronizes
the portfolio only after all of those steps succeed.

This runbook does not authorize a production deployment. A deployer must separately assess runtime
identity, credentials, images, network, state, monitoring, recovery, and change management.
