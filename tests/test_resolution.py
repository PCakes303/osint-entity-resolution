import unittest
from datetime import datetime
from osint_entity_resolution.models import EntityError, normalize_name, validate_entity_record
from osint_entity_resolution.resolver import ResolutionError, match_pair, match_records
from tests.helpers import NOW, entity

class EntityModelTests(unittest.TestCase):
    def test_name_normalization_is_unicode_and_punctuation_stable(self):
        self.assertEqual(normalize_name("  ACME, Inc.  "), "acme inc")
        self.assertEqual(normalize_name("Café—Systems"), "café systems")

    def test_valid_public_organization_record(self):
        self.assertEqual(validate_entity_record(entity())["entity_type"], "public_organization")

    def test_person_entity_type_is_rejected(self):
        with self.assertRaises(EntityError):
            validate_entity_record(entity(entity_type="person"))

    def test_entity_id_namespace_must_match_type(self):
        with self.assertRaisesRegex(EntityError, "namespace"):
            validate_entity_record(entity(entity_id="project:acme"))

    def test_normalized_name_must_match_canonical_name(self):
        value = entity()
        value["normalized_name"] = "not the same"
        with self.assertRaisesRegex(EntityError, "does not match"):
            validate_entity_record(value)

    def test_evidence_reference_is_required(self):
        value = entity()
        value["evidence_refs"] = []
        with self.assertRaises(EntityError):
            validate_entity_record(value)

class ResolverTests(unittest.TestCase):
    def test_exact_public_identifier_creates_review_candidate(self):
        a = entity("org:a","Acme Analytics",{"domain":"acme.example"})
        b = entity("org:b","Different Trading Name",{"domain":"acme.example"},evidence=["evidence:002"])
        candidate = match_pair(a,b,now=NOW)
        self.assertEqual(candidate["score"],1.0)
        self.assertIn("exact_public_identifier",candidate["reason_codes"])
        self.assertEqual(candidate["review_status"],"review_required")
        self.assertEqual(candidate["score_kind"],"heuristic_similarity_not_probability")

    def test_conflicting_stable_identifier_blocks_name_match(self):
        a = entity("org:a","Acme Analytics",{"domain":"acme.example"})
        b = entity("org:b","Acme Analytics",{"domain":"other.example"})
        self.assertIsNone(match_pair(a,b,now=NOW))

    def test_name_similarity_creates_candidate_without_auto_merge(self):
        a = entity("org:a","Acme Analytics")
        b = entity("org:b","Acme Analytic")
        candidate = match_pair(a,b,now=NOW,threshold=0.90)
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate["review_status"],"review_required")

    def test_shared_alias_creates_candidate(self):
        a = entity("org:a","Alpha Holdings",aliases=["Alpha Group"])
        b = entity("org:b","Beta Holdings",aliases=["Alpha Group"])
        candidate = match_pair(a,b,now=NOW)
        self.assertIn("shared_alias",candidate["reason_codes"])

    def test_cross_type_entities_do_not_match(self):
        a = entity("org:a","Acme Analytics",entity_type="public_organization")
        b = entity("project:b","Acme Analytics",entity_type="public_software_project")
        self.assertIsNone(match_pair(a,b,now=NOW))

    def test_match_results_are_deterministic_and_sorted(self):
        a = entity("org:a","Acme Analytics",{"domain":"acme.example"})
        b = entity("org:b","Different Name",{"domain":"acme.example"},evidence=["evidence:002"])
        first = match_records([b,a],now=NOW)
        second = match_records([a,b],now=NOW)
        self.assertEqual(first,second)
        self.assertEqual(first[0]["left_entity_id"],"org:a")

    def test_duplicate_entity_ids_rejected(self):
        a = entity("org:a")
        b = entity("org:a","Acme Analytics")
        with self.assertRaisesRegex(ResolutionError,"duplicate"):
            match_records([a,b],now=NOW)

    def test_pair_comparison_budget_is_enforced(self):
        records=[entity("org:a","Alpha Company"),entity("org:b","Beta Company"),entity("org:c","Gamma Company")]
        with self.assertRaisesRegex(ResolutionError,"budget"):
            match_records(records,now=NOW,max_pairs=2)

    def test_record_count_is_bounded(self):
        records=[entity(f"org:id-{i}",f"Organization {i}") for i in range(1001)]
        with self.assertRaisesRegex(ResolutionError,"record count"):
            match_records(records,now=NOW)

    def test_threshold_and_clock_are_validated_even_for_empty_input(self):
        with self.assertRaisesRegex(ResolutionError,"threshold"):
            match_records([],now=NOW,threshold=0.5)
        with self.assertRaisesRegex(ResolutionError,"timezone-aware"):
            match_records([],now=datetime(2026,11,2,12,0))

if __name__ == "__main__":
    unittest.main()
