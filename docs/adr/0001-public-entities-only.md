# ADR 0001: Public non-personal entities only

- Status: accepted
- Date: 2026-11-02

## Context

Entity correlation can become identity resolution, personal profiling or surveillance when applied to people and private accounts. The portfolio's initial OSINT scope is public-source research with privacy and compliance gates.

## Decision

The initial resolver supports public organizations, software projects, datasets, publications and public registries only. It generates review-required candidates, not resolved identities. It never auto-merges entities or scores people. Every candidate retains evidence references and uncertainty.

## Consequences

- Person and private-individual matching are explicitly unsupported.
- Candidate scores are heuristic, not probabilities.
- Human review, identity, policy, compliance and audit integrations are required before acceptance.
- Knowledge-graph writes remain a separate adapter and are not implemented here.
