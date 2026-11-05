# Integration Gates Before Accepting a Resolution

1. Verify source and evidence records from osint-source-registry and osint-evidence.
2. Authenticate requester and reviewer identities.
3. Evaluate purpose and scope through policy-engine.
4. Confirm emergency-stop state before candidate processing and before acceptance.
5. Obtain compliance/privacy review; reject personal or sensitive data in the initial profile.
6. Record candidate generation, reviewer decision, uncertainty, dispute and withdrawal in audit-provenance.
7. Verify build and artifact provenance through secure-supply-chain.
8. Require a human reviewer to accept/reject; no candidate may be auto-merged.
9. Map accepted records to the knowledge-graph contract only through a versioned adapter and reproducible fixtures.
10. Test false-positive/false-negative rates on a legally approved, non-personal benchmark; do not claim calibrated probabilities without statistical validation.

The current package does not implement these cross-repository integrations or an acceptance workflow.
