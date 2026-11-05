# Security Policy

This repository produces candidate matches among permitted public non-personal entity types only. It does not resolve people, infer identity, score individuals, automatically merge entities or write to a graph.

## Reporting

Do not publish exploitable vulnerability details, credentials, personal data or confidential operational information in public issues. Use GitHub private vulnerability reporting or a private security advisory only if enabled for this repository. No dedicated private reporting address is published here; configure an owner-approved private channel if GitHub private reporting is unavailable.

## Security invariants

- Reject unsupported or person-related entity types.
- Require evidence references and preserve uncertainty.
- Treat candidate scores as heuristic, never as identity proof.
- No auto-merge or consequential decision output.
- Bound record counts and pair comparisons.
- No network or graph persistence is implemented.
