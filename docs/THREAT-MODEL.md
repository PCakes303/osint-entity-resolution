# Threat Model

## Assets

- Public entity record integrity and provenance.
- Correct separation of entity types and namespaces.
- Candidate score and reason-code reproducibility.
- Human review, dispute and withdrawal history.

## Threats and controls

| Threat | Reference control | Remaining requirement |
|---|---|---|
| Private-person targeting | Person entity type absent from schema | Policy enforcement and abuse monitoring |
| False positive merge | Candidate-only output; no auto-merge | Independent human review |
| Identifier collision | Conflicting stable identifiers block candidate | Source-specific identifier validation |
| Name ambiguity | Heuristic score and uncertainty statement | Calibrated domain-specific evaluation |
| Evidence laundering | Evidence/source references required | Authenticated provenance and audit integration |
| Work exhaustion | 1,000-record and 10,000-pair ceilings | Service-level quotas and rate limiting |
| Data poisoning | Schema and provenance references | Trusted source validation and reviewer controls |
| Sensitive-data inference | No personal/sensitive entity types | Content classification at ingestion |

## Non-goals

No person resolution, personal profiling, protected-trait inference, automatic merge, graph persistence, external lookup, network ingestion or consequential decision-making.
