# Agent instructions

- Restrict matching to public organizations, software projects, datasets, publications and public registries.
- Never resolve or correlate real people, private individuals, social accounts, personal identifiers or sensitive attributes.
- Never score people, infer protected traits, build dossiers or support targeting, harassment, doxxing or surveillance.
- Candidate scores are heuristic similarity measures, not probabilities or proof of identity.
- Never automatically merge entities or convert a candidate into a resolved identity.
- Every candidate must retain evidence references, source references, reason codes and uncertainty.
- Require human review, authenticated reviewer identity, policy approval, compliance review, audit provenance and emergency-stop clearance before any accepted resolution.
- Fail closed on conflicting stable identifiers, missing evidence or exceeded pair budgets.
- Do not add network access or knowledge-graph writes in this scaffold.
- Run python -m unittest discover -s tests -v before committing.
