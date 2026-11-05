# Contributing

Contributions may improve deterministic normalization, public-entity matching, candidate scoring, uncertainty reporting and synthetic tests. Any person-related matching, automated merging, network ingestion or consequential decision support is out of scope and requires a separate policy and legal review.

## Development

- Python 3.10+
- Install: python -m pip install -r requirements-dev.txt
- Test: python -m unittest discover -s tests -v

Changes to entity types, identifiers, matching thresholds, pair budgets or evidence requirements require positive, negative and boundary tests. Do not include real personal data or actual target dossiers in fixtures.
