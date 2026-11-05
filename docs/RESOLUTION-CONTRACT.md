# Public Entity Resolution Contract v1.0

## Scope

The initial contract matches only public organizations, software projects, datasets, publications and public registries. Person, private-individual, social-account and sensitive-attribute entity types are not supported.

## Input record

Each provisional entity includes a typed namespace ID, entity type, canonical and normalized names, public identifiers, aliases, evidence references, source references and an observation timestamp. Stable identifiers are limited to public domains, public registry IDs, repository URLs, publication DOIs, dataset IDs and organization IDs.

## Candidate generation

- Exact matching public identifiers produce a candidate with heuristic score 1.0.
- Conflicting values for the same stable identifier key block a match.
- Shared aliases or normalized-name similarity can produce a candidate.
- Candidate comparisons are bounded by record and pair budgets.
- Results are deterministically sorted and candidate IDs are content-derived.

## Interpretation

A score is a heuristic similarity measure, not a calibrated probability. A candidate is not an identity assertion. Every output has review_status=review_required, reason codes, evidence references and an uncertainty statement. The engine does not accept or merge candidates.

## Human review

A separate trusted workflow must authenticate the reviewer, verify evidence, apply policy and compliance requirements, record the decision in audit provenance and preserve any dispute or withdrawal. The current scaffold does not implement that workflow or write to the knowledge graph.
