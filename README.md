# OSINT Entity Resolution

Portfolio ID: entity-resolution  
Version: 1.1.0  
Maturity: scaffolding; bounded public-entity candidate matcher only. No identity resolution or graph writes.

Generate bounded, evidence-backed candidate matches among public organizations, software projects, datasets, publications and public registries. Preserve ambiguity and require human review.

## Safety boundary

The initial profile does not resolve real people, private individuals, social accounts, personal identifiers or sensitive attributes. It does not infer identity, build personal profiles, score people or make consequential decisions. It only produces candidate matches between permitted public entity types.

The matcher does not automatically merge entities or assert identity. A score is a heuristic similarity measure, not a calibrated probability. Every candidate remains review-required and must retain evidence references and uncertainty.

## Quick start

Python 3.10+:

    python -m pip install -r requirements-dev.txt
    python -m unittest discover -s tests -v

See docs/RESOLUTION-CONTRACT.md, docs/THREAT-MODEL.md and docs/INTEGRATION-GATES.md.

## Licensing

This repository applies the ecosystem's scoped mixed-license policy: original source code and machine-readable contracts are licensed under Apache-2.0; original human-readable documentation is licensed under CC BY 4.0. Third-party material retains upstream terms. Datasets, evidence, fixtures, sample payloads, media, and material with uncertain provenance are not blanket-licensed and require separate review. See [LICENSE.md](LICENSE.md).
