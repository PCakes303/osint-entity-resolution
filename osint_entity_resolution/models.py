"""Strict public-entity record validation and deterministic name normalization."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "entity-record.schema.json"
_SCHEMA = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
_VALIDATOR = Draft202012Validator(_SCHEMA, format_checker=FormatChecker())
PREFIX_BY_TYPE = {
    "public_organization":"org",
    "public_software_project":"project",
    "public_dataset":"dataset",
    "public_publication":"publication",
    "public_registry":"registry",
}

class EntityError(ValueError):
    """Raised for malformed or out-of-scope public entity records."""

def normalize_name(value: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 256:
        raise EntityError("entity name must be a non-empty bounded string")
    normalized = unicodedata.normalize("NFKC", value).casefold()
    tokens = []
    current = []
    for char in normalized:
        if char.isalnum():
            current.append(char)
        elif current:
            tokens.append("".join(current))
            current = []
    if current:
        tokens.append("".join(current))
    result = " ".join(tokens)
    if len(result) < 2:
        raise EntityError("normalized entity name is too short")
    return result

def validate_entity_record(raw: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise EntityError("entity record must be an object")
    errors = sorted(_VALIDATOR.iter_errors(raw), key=lambda e: (list(e.absolute_path), e.message))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise EntityError(f"entity schema error at {location}: {first.message}")
    expected_prefix = PREFIX_BY_TYPE[raw["entity_type"]] + ":"
    if not raw["entity_id"].startswith(expected_prefix):
        raise EntityError("entity_id namespace does not match entity_type")
    expected_normalized = normalize_name(raw["canonical_name"])
    if raw["normalized_name"] != expected_normalized:
        raise EntityError("normalized_name does not match canonical_name")
    if raw["review_status"] != "provisional":
        raise EntityError("input entities must remain provisional; no automatic resolution")
    return dict(raw)
