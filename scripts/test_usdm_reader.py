#!/usr/bin/env python3
"""
Unit tests for usdm_reader.py — Task F-1 coverage.

Run with:
    python3 -m unittest discover scripts/
"""

import importlib.util
import os
import pathlib
import tempfile
import unittest

# ---------------------------------------------------------------------------
# Load usdm_reader module from sibling file (avoids sys.path manipulation)
# ---------------------------------------------------------------------------
_HERE = pathlib.Path(__file__).parent
_READER_PATH = _HERE / "usdm_reader.py"

spec = importlib.util.spec_from_file_location("usdm_reader", _READER_PATH)
usdm_reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usdm_reader)

USDMDoc = usdm_reader.USDMDoc
emit_research_study = usdm_reader.emit_research_study
parse_iso8601_duration_to_days = usdm_reader.parse_iso8601_duration_to_days
strip_html = usdm_reader.strip_html

# Path to the real USDM file (relative to repo root)
_REPO_ROOT = _HERE.parent
_USDM_PATH = str(_REPO_ROOT / "input" / "usdm" / "CDISC_Pilot_Study_v4_FIXED.json")
_USDM_AVAILABLE = os.path.exists(_USDM_PATH)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _require_usdm(test_case):
    """Skip test if the USDM file is not present."""
    if not _USDM_AVAILABLE:
        test_case.skipTest(f"USDM file not found: {_USDM_PATH}")


# ---------------------------------------------------------------------------
# parse_iso8601_duration_to_days
# ---------------------------------------------------------------------------
class TestParseISO8601Duration(unittest.TestCase):
    def test_none_returns_none(self):
        self.assertIsNone(parse_iso8601_duration_to_days(None))

    def test_days(self):
        self.assertEqual(parse_iso8601_duration_to_days("P2D"), 2.0)
        self.assertEqual(parse_iso8601_duration_to_days("P14D"), 14.0)
        self.assertEqual(parse_iso8601_duration_to_days("P182D"), 182.0)

    def test_weeks(self):
        self.assertEqual(parse_iso8601_duration_to_days("P2W"), 14.0)
        self.assertEqual(parse_iso8601_duration_to_days("P4W"), 28.0)
        self.assertEqual(parse_iso8601_duration_to_days("P26W"), 182.0)

    def test_hours(self):
        self.assertAlmostEqual(parse_iso8601_duration_to_days("PT4H"), 4 / 24)
        self.assertEqual(parse_iso8601_duration_to_days("PT0H"), 0.0)

    def test_minutes(self):
        self.assertAlmostEqual(parse_iso8601_duration_to_days("PT5M"), 5 / 1440)
        self.assertEqual(parse_iso8601_duration_to_days("PT0M"), 0.0)

    def test_unsupported_raises(self):
        with self.assertRaises(ValueError):
            parse_iso8601_duration_to_days("P1Y")
        with self.assertRaises(ValueError):
            parse_iso8601_duration_to_days("P1M")
        with self.assertRaises(ValueError):
            parse_iso8601_duration_to_days("garbage")


# ---------------------------------------------------------------------------
# strip_html
# ---------------------------------------------------------------------------
class TestStripHtml(unittest.TestCase):
    def test_removes_tags(self):
        self.assertEqual(strip_html("<p>Hello</p>"), "Hello")

    def test_unescapes_entities(self):
        self.assertEqual(strip_html("&amp;"), "&")
        self.assertEqual(strip_html("&lt;p&gt;"), "<p>")

    def test_empty_string(self):
        self.assertEqual(strip_html(""), "")

    def test_none_returns_empty(self):
        self.assertEqual(strip_html(None), "")

    def test_nested_tags(self):
        result = strip_html("<p>To assess the <em>dose</em>-dependent improvement.</p>")
        self.assertEqual(result, "To assess the dose-dependent improvement.")


# ---------------------------------------------------------------------------
# USDMDoc — index and accessors (requires real USDM file)
# ---------------------------------------------------------------------------
class TestUSDMDocIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not _USDM_AVAILABLE:
            return
        cls.doc = USDMDoc(_USDM_PATH)

    def setUp(self):
        _require_usdm(self)

    def test_study_name(self):
        self.assertEqual(self.doc.study()["name"], "CDISC PILOT - LZZT")

    def test_study_version_identifier(self):
        self.assertEqual(self.doc.study_version()["versionIdentifier"], "2")

    def test_study_design_exists(self):
        sd = self.doc.study_design()
        self.assertIsNotNone(sd)
        self.assertIn("id", sd)

    def test_resolve_known_id(self):
        # Organization_1 must be resolvable
        org = self.doc.resolve("Organization_1")
        self.assertEqual(org["name"], "LILLY")

    def test_resolve_unknown_id_raises(self):
        with self.assertRaises(KeyError):
            self.doc.resolve("NonExistentId_999")

    def test_encounters_count(self):
        encounters = self.doc.encounters()
        self.assertEqual(len(encounters), 12)

    def test_organizations_count(self):
        orgs = self.doc.organizations()
        self.assertEqual(len(orgs), 3)

    def test_sponsor_org(self):
        sponsor = self.doc.sponsor_org()
        self.assertIsNotNone(sponsor)
        self.assertEqual(sponsor["name"], "LILLY")

    def test_investigator_persons(self):
        persons = self.doc.investigator_persons()
        self.assertGreater(len(persons), 0)
        pi = persons[0]
        self.assertEqual(pi["id"], "Pers_001")

    def test_pi_name(self):
        pi = self.doc.investigator_persons()[0]
        pn = pi["personName"]
        self.assertEqual(pn["familyName"], "X")
        self.assertIn("Ab", pn["givenNames"])


# ---------------------------------------------------------------------------
# USDMDoc — study identifiers
# ---------------------------------------------------------------------------
class TestStudyIdentifiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not _USDM_AVAILABLE:
            return
        cls.doc = USDMDoc(_USDM_PATH)

    def setUp(self):
        _require_usdm(self)

    def test_two_identifiers(self):
        ids = self.doc.study_version()["studyIdentifiers"]
        self.assertEqual(len(ids), 2)

    def test_sponsor_identifier(self):
        ids = self.doc.study_version()["studyIdentifiers"]
        sponsor_id = next(i for i in ids if i["scopeId"] == "Organization_1")
        self.assertEqual(sponsor_id["text"], "H2Q-MC-LZZT")

    def test_registry_identifier(self):
        ids = self.doc.study_version()["studyIdentifiers"]
        reg_id = next(i for i in ids if i["scopeId"] == "Organization_2")
        self.assertEqual(reg_id["text"], "NCT12345678")


# ---------------------------------------------------------------------------
# USDMDoc — study design fields
# ---------------------------------------------------------------------------
class TestStudyDesignFields(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not _USDM_AVAILABLE:
            return
        cls.doc = USDMDoc(_USDM_PATH)

    def setUp(self):
        _require_usdm(self)

    def test_phase_code(self):
        sd = self.doc.study_design()
        phase_code = sd["studyPhase"]["standardCode"]["code"]
        self.assertEqual(phase_code, "C15601")

    def test_phase_maps_to_fhir(self):
        phase_code = self.doc.study_design()["studyPhase"]["standardCode"]["code"]
        fhir_phase = usdm_reader.CDISC_PHASE_MAP.get(phase_code)
        self.assertEqual(fhir_phase, "phase-2")

    def test_indications_count(self):
        inds = self.doc.study_design()["indications"]
        self.assertEqual(len(inds), 2)

    def test_indication_icd10(self):
        inds = self.doc.study_design()["indications"]
        icd = next(
            c for ind in inds for c in ind["codes"]
            if c["codeSystem"] == "ICD-10-CM"
        )
        self.assertEqual(icd["code"], "G30.9")

    def test_indication_snomed(self):
        inds = self.doc.study_design()["indications"]
        sct = next(
            c for ind in inds for c in ind["codes"]
            if c["codeSystem"] == "SNOMED"
        )
        self.assertEqual(sct["code"], "26929004")

    def test_therapeutic_areas_count(self):
        tas = self.doc.study_design()["therapeuticAreas"]
        self.assertEqual(len(tas), 2)

    def test_arms_count(self):
        arms = self.doc.study_design()["arms"]
        self.assertEqual(len(arms), 3)

    def test_arm_names(self):
        arms = self.doc.study_design()["arms"]
        names = [a["name"] for a in arms]
        self.assertIn("Placebo", names)
        self.assertIn("Xanomeline Low Dose", names)
        self.assertIn("Xanomeline High Dose", names)

    def test_objectives_count(self):
        objs = self.doc.study_design()["objectives"]
        self.assertEqual(len(objs), 6)

    def test_primary_objective(self):
        objs = self.doc.study_design()["objectives"]
        primary = next(
            o for o in objs if o["level"]["code"] == "C85826"
        )
        self.assertIsNotNone(primary)

    def test_secondary_objectives(self):
        objs = self.doc.study_design()["objectives"]
        secondary = [o for o in objs if o["level"]["code"] == "C85827"]
        self.assertEqual(len(secondary), 5)


# ---------------------------------------------------------------------------
# emit_research_study — FSH output content
# ---------------------------------------------------------------------------
class TestEmitResearchStudy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not _USDM_AVAILABLE:
            return
        cls.doc = USDMDoc(_USDM_PATH)
        cls.tmp_dir = tempfile.mkdtemp()
        cls.out_path = os.path.join(cls.tmp_dir, "ResearchStudy.gen.fsh")
        emit_research_study(cls.doc, cls.out_path)
        with open(cls.out_path, encoding="utf-8") as fh:
            cls.content = fh.read()

    def setUp(self):
        _require_usdm(self)

    def test_do_not_edit_header(self):
        first_line = self.content.splitlines()[0]
        self.assertIn("DO NOT EDIT", first_line)
        self.assertIn("usdm_to_soa.py", first_line)

    def test_research_study_instance_id(self):
        self.assertIn("Instance: H2Q-MC-LZZT-ResearchStudy-USDM", self.content)

    def test_title_mapped(self):
        self.assertIn("CDISC PILOT - LZZT", self.content)

    def test_phase_mapped(self):
        self.assertIn("#phase-2", self.content)

    def test_sponsor_org_instance(self):
        self.assertIn("Instance: LILLY-USDM", self.content)
        self.assertIn("InstanceOf: Organization", self.content)

    def test_sponsor_name(self):
        self.assertIn('"LILLY"', self.content)

    def test_sponsor_reference(self):
        self.assertIn("Reference(Organization/LILLY-USDM)", self.content)

    def test_practitioner_instance(self):
        self.assertIn("Instance: Pers_001", self.content)
        self.assertIn("InstanceOf: Practitioner", self.content)

    def test_pi_family_name(self):
        self.assertIn('"X"', self.content)

    def test_pi_reference(self):
        self.assertIn("Reference(Practitioner/Pers_001)", self.content)

    def test_sponsor_identifier(self):
        self.assertIn("H2Q-MC-LZZT", self.content)

    def test_nct_identifier(self):
        self.assertIn("NCT12345678", self.content)

    def test_nct_system(self):
        self.assertIn("clinicaltrials.gov", self.content)

    def test_icd10_condition(self):
        self.assertIn("G30.9", self.content)
        self.assertIn("icd-10-cm", self.content)

    def test_snomed_condition(self):
        self.assertIn("26929004", self.content)
        self.assertIn("snomed.info", self.content)

    def test_therapeutic_areas(self):
        self.assertIn("MILD_MOD_ALZ", self.content)

    def test_arms_present(self):
        self.assertIn("Placebo", self.content)
        self.assertIn("Xanomeline Low Dose", self.content)
        self.assertIn("Xanomeline High Dose", self.content)

    def test_arm_type_placebo(self):
        self.assertIn("C174268", self.content)

    def test_arm_type_active(self):
        self.assertIn("C174267", self.content)

    def test_objectives_present(self):
        self.assertIn("#primary", self.content)
        self.assertIn("#secondary", self.content)

    def test_primary_objective_text(self):
        # The primary objective text (HTML-stripped) should appear
        self.assertIn("ADAS-Cog", self.content)

    def test_version_present(self):
        self.assertIn('"2"', self.content)

    def test_lead_sponsor_role(self):
        self.assertIn("#lead-sponsor", self.content)

    def test_primary_investigator_role(self):
        self.assertIn("#primary-investigator", self.content)


# ---------------------------------------------------------------------------
# emit_research_study — idempotency
# ---------------------------------------------------------------------------
class TestEmitResearchStudyIdempotency(unittest.TestCase):
    def setUp(self):
        _require_usdm(self)

    def test_idempotent(self):
        doc = USDMDoc(_USDM_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "ResearchStudy.gen.fsh")
            emit_research_study(doc, out)
            with open(out, "rb") as fh:
                first = fh.read()
            emit_research_study(doc, out)
            with open(out, "rb") as fh:
                second = fh.read()
        self.assertEqual(first, second, "emit_research_study is not idempotent")


# ---------------------------------------------------------------------------
# emit_research_study — output directory creation
# ---------------------------------------------------------------------------
class TestEmitResearchStudyDirCreation(unittest.TestCase):
    def setUp(self):
        _require_usdm(self)

    def test_creates_output_directory(self):
        doc = USDMDoc(_USDM_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            nested = os.path.join(tmp, "a", "b", "c", "ResearchStudy.gen.fsh")
            emit_research_study(doc, nested)
            self.assertTrue(os.path.exists(nested))


if __name__ == "__main__":
    unittest.main()
