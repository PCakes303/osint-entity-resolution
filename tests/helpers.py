from datetime import datetime, timezone
from osint_entity_resolution.models import normalize_name

NOW = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)

def entity(entity_id="org:acme-one", name="Acme Analytics", identifiers=None, aliases=None, entity_type="public_organization", evidence=None):
    return {
        "record_version":"1.0","entity_id":entity_id,"entity_type":entity_type,
        "canonical_name":name,"normalized_name":normalize_name(name),
        "identifiers":identifiers or {},"aliases":aliases or [],
        "evidence_refs":evidence or ["evidence:001"],"source_refs":["source:001"],
        "observed_at":"2026-11-02T12:00:00Z","review_status":"provisional"
    }
