"""Bounded public-entity candidate matching; no auto-merge or identity assertion."""
from __future__ import annotations

import hashlib
import json
from difflib import SequenceMatcher
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker

from .models import EntityError, normalize_name, validate_entity_record

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "resolution-candidate.schema.json"
_SCHEMA = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
_VALIDATOR = Draft202012Validator(_SCHEMA, format_checker=FormatChecker())
MAX_ENTITY_RECORDS = 1000
MAX_PAIR_COMPARISONS = 10_000

class ResolutionError(ValueError):
    """Raised when candidate generation exceeds scope or work limits."""

def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def _validate_run(now: datetime, threshold: float) -> None:
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ResolutionError("now must be timezone-aware")
    if isinstance(threshold, bool) or not isinstance(threshold, (int,float)) or not 0.80 <= threshold <= 1.0:
        raise ResolutionError("threshold must be in [0.80, 1.0]")

def _candidate(left: Mapping[str, Any], right: Mapping[str, Any], *, score: float, reasons: list[str], now: datetime) -> dict[str, Any]:
    left_id, right_id = sorted((left["entity_id"], right["entity_id"]))
    evidence_refs = sorted(set(left["evidence_refs"]) | set(right["evidence_refs"]))
    identity = {"left":left_id,"right":right_id,"score":round(float(score), 6),"reasons":sorted(set(reasons)),"evidence":evidence_refs}
    candidate_id = "cand:" + hashlib.sha256(_canonical(identity)).hexdigest()
    result = {
        "candidate_id":candidate_id,"left_entity_id":left_id,"right_entity_id":right_id,
        "score":round(float(score), 6),"score_kind":"heuristic_similarity_not_probability",
        "reason_codes":sorted(set(reasons)),"evidence_refs":evidence_refs,
        "uncertainty":"Candidate only; this heuristic score is not a probability or proof of identity. Independent human review is required.",
        "review_status":"review_required","created_at":now.astimezone(timezone.utc).isoformat().replace("+00:00","Z"),
    }
    errors = list(_VALIDATOR.iter_errors(result))
    if errors:
        raise ResolutionError(f"candidate schema error: {errors[0].message}")
    return result

def match_pair(left: Mapping[str, Any], right: Mapping[str, Any], *, now: datetime, threshold: float = 0.92) -> dict[str, Any] | None:
    _validate_run(now, threshold)
    a = validate_entity_record(left)
    b = validate_entity_record(right)
    if a["entity_id"] == b["entity_id"] or a["entity_type"] != b["entity_type"]:
        return None
    common_keys = set(a["identifiers"]) & set(b["identifiers"])
    conflicts = [key for key in common_keys if a["identifiers"][key] != b["identifiers"][key]]
    if conflicts:
        return None
    exact = sorted(key for key in common_keys if a["identifiers"][key] == b["identifiers"][key])
    if exact:
        return _candidate(a,b,score=1.0,reasons=["exact_public_identifier"],now=now)
    aliases_a = {normalize_name(item) for item in a["aliases"]}
    aliases_b = {normalize_name(item) for item in b["aliases"]}
    if aliases_a & aliases_b:
        return _candidate(a,b,score=0.95,reasons=["shared_alias"],now=now)
    similarity = SequenceMatcher(None,a["normalized_name"],b["normalized_name"],autojunk=False).ratio()
    if similarity >= threshold:
        return _candidate(a,b,score=similarity,reasons=["normalized_name_similarity"],now=now)
    return None

def match_records(
    records: Sequence[Mapping[str, Any]], *, now: datetime, threshold: float = 0.92,
    max_pairs: int = MAX_PAIR_COMPARISONS
) -> tuple[dict[str, Any], ...]:
    _validate_run(now, threshold)
    if not isinstance(records, (list, tuple)) or len(records) > MAX_ENTITY_RECORDS:
        raise ResolutionError("entity record count exceeds limit")
    if isinstance(max_pairs, bool) or not isinstance(max_pairs, int) or not 1 <= max_pairs <= MAX_PAIR_COMPARISONS:
        raise ResolutionError("max_pairs must be in [1, 10000]")
    parsed = [validate_entity_record(item) for item in records]
    ids = [item["entity_id"] for item in parsed]
    if len(ids) != len(set(ids)):
        raise ResolutionError("duplicate entity_id")
    ordered = sorted(parsed, key=lambda item:item["entity_id"])
    candidates = []
    comparisons = 0
    for index, left in enumerate(ordered):
        for right in ordered[index+1:]:
            comparisons += 1
            if comparisons > max_pairs:
                raise ResolutionError("pair comparison budget exceeded")
            candidate = match_pair(left,right,now=now,threshold=threshold)
            if candidate is not None:
                candidates.append(candidate)
    return tuple(sorted(candidates,key=lambda item:item["candidate_id"]))
