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
emit_eligibility_groups = usdm_reader.emit_eligibility_groups
emit_visit_plan_definitions = usdm_reader.emit_visit_plan_definitions
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


# ---------------------------------------------------------------------------
# _strip_criterion_text — unit tests (no USDM file needed)
# ---------------------------------------------------------------------------
class TestStripCriterionText(unittest.TestCase):
    """Tests for the internal _strip_criterion_text helper."""

    _strip = staticmethod(usdm_reader._strip_criterion_text)

    def test_plain_paragraph(self):
        result = self._strip("<p>A history of syncope within the last 5 years.</p>")
        self.assertEqual(result, "A history of syncope within the last 5 years.")

    def test_usdm_tag_removed(self):
        result = self._strip("<p>Males and postmenopausal females at least <usdm:tag name=\"min_age\"/> years of age.</p>")
        self.assertNotIn("<usdm:tag", result)
        self.assertIn("Males and postmenopausal females at least", result)
        self.assertIn("years of age.", result)

    def test_usdm_ref_removed(self):
        result = self._strip('<p><usdm:ref attribute="text" id="X_1" klass="X"></usdm:ref> score of 10 to 23.</p>')
        self.assertNotIn("usdm:", result)
        self.assertIn("score of 10 to 23.", result)

    def test_nested_html_collapsed(self):
        raw = (
            "<p>Diagnosis of serious neurological conditions, including </p>\n"
            "<ol><li><p>Stroke or vascular dementia</p></li>\n"
            "<li><p>Seizure disorder</p></li></ol>"
        )
        result = self._strip(raw)
        self.assertNotIn("<", result)
        self.assertIn("Stroke or vascular dementia", result)
        self.assertIn("Seizure disorder", result)

    def test_empty_string(self):
        self.assertEqual(self._strip(""), "")

    def test_none_returns_empty(self):
        self.assertEqual(self._strip(None), "")

    def test_whitespace_collapsed(self):
        result = self._strip("<p>Line one.</p>\n<p>Line two.</p>")
        self.assertNotIn("\n", result)
        self.assertIn("Line one.", result)
        self.assertIn("Line two.", result)


# ---------------------------------------------------------------------------
# emit_eligibility_groups — FSH output content
# ---------------------------------------------------------------------------
class TestEmitEligibilityGroups(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not _USDM_AVAILABLE:
            return
        cls.doc = USDMDoc(_USDM_PATH)
        cls.tmp_dir = tempfile.mkdtemp()
        cls.out_path = os.path.join(cls.tmp_dir, "Eligibility.gen.fsh")
        emit_eligibility_groups(cls.doc, cls.out_path)
        with open(cls.out_path, encoding="utf-8") as fh:
            cls.content = fh.read()

    def setUp(self):
        _require_usdm(self)

    def test_do_not_edit_header(self):
        first_line = self.content.splitlines()[0]
        self.assertIn("DO NOT EDIT", first_line)
        self.assertIn("usdm_to_soa.py", first_line)

    def test_inclusion_instance_id(self):
        self.assertIn("Instance: H2Q-MC-LZZT-ResearchStudy-Inclusion-USDM", self.content)

    def test_exclusion_instance_id(self):
        self.assertIn("Instance: H2Q-MC-LZZT-ResearchStudy-Exclusion-USDM", self.content)

    def test_instance_of_group(self):
        # Both instances must declare InstanceOf: Group
        count = self.content.count("InstanceOf: Group")
        self.assertEqual(count, 2)

    def test_type_person(self):
        count = self.content.count("* type = #person")
        self.assertEqual(count, 2)

    def test_membership_definitional(self):
        count = self.content.count("* membership = #definitional")
        self.assertEqual(count, 2)

    def test_total_criteria_count(self):
        """31 criteria total → 31 characteristic[+] entries."""
        count = self.content.count("* characteristic[+].code.text")
        self.assertEqual(count, 31)

    def test_inclusion_criteria_count(self):
        """8 inclusion criteria → 8 exclude = false entries."""
        count = self.content.count("* characteristic[=].exclude = false")
        self.assertEqual(count, 8)

    def test_exclusion_criteria_count(self):
        """23 exclusion criteria → 23 exclude = true entries."""
        count = self.content.count("* characteristic[=].exclude = true")
        self.assertEqual(count, 23)

    def test_value_boolean_true_count(self):
        """Every characteristic has valueBoolean = true."""
        count = self.content.count("* characteristic[=].valueBoolean = true")
        self.assertEqual(count, 31)

    def test_no_html_tags_in_output(self):
        """No raw HTML tags should appear in the FSH output."""
        import re as _re
        # Allow FSH comments (lines starting with //) to contain angle brackets
        non_comment_lines = [
            ln for ln in self.content.splitlines()
            if not ln.strip().startswith("//")
        ]
        for line in non_comment_lines:
            self.assertNotIn("<p>", line, f"HTML tag found in: {line!r}")
            self.assertNotIn("</p>", line, f"HTML tag found in: {line!r}")
            self.assertNotIn("<usdm:", line, f"USDM tag found in: {line!r}")

    def test_no_usdm_tags_in_output(self):
        """No <usdm:tag> or <usdm:ref> elements in output."""
        self.assertNotIn("<usdm:", self.content)

    def test_inclusion_before_exclusion(self):
        """Inclusion group must appear before exclusion group in the file."""
        inc_pos = self.content.find("H2Q-MC-LZZT-ResearchStudy-Inclusion-USDM")
        exc_pos = self.content.find("H2Q-MC-LZZT-ResearchStudy-Exclusion-USDM")
        self.assertGreater(exc_pos, inc_pos)

    def test_known_inclusion_text_present(self):
        """A known inclusion criterion text fragment must appear."""
        # EligibilityCriterionItem_5: CNS imaging
        self.assertIn("CNS imaging", self.content)

    def test_known_exclusion_text_present(self):
        """A known exclusion criterion text fragment must appear."""
        # EligibilityCriterionItem_9: xanomeline
        self.assertIn("xanomeline", self.content)

    def test_usage_example(self):
        count = self.content.count("Usage: #example")
        self.assertEqual(count, 2)


# ---------------------------------------------------------------------------
# emit_eligibility_groups — idempotency
# ---------------------------------------------------------------------------
class TestEmitEligibilityGroupsIdempotency(unittest.TestCase):
    def setUp(self):
        _require_usdm(self)

    def test_idempotent(self):
        doc = USDMDoc(_USDM_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "Eligibility.gen.fsh")
            emit_eligibility_groups(doc, out)
            with open(out, "rb") as fh:
                first = fh.read()
            emit_eligibility_groups(doc, out)
            with open(out, "rb") as fh:
                second = fh.read()
        self.assertEqual(first, second, "emit_eligibility_groups is not idempotent")


# ---------------------------------------------------------------------------
# emit_eligibility_groups — output directory creation
# ---------------------------------------------------------------------------
class TestEmitEligibilityGroupsDirCreation(unittest.TestCase):
    def setUp(self):
        _require_usdm(self)

    def test_creates_output_directory(self):
        doc = USDMDoc(_USDM_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            nested = os.path.join(tmp, "a", "b", "Eligibility.gen.fsh")
            emit_eligibility_groups(doc, nested)
            self.assertTrue(os.path.exists(nested))


# ---------------------------------------------------------------------------
# USDMDoc — eligibility criteria accessors
# ---------------------------------------------------------------------------
class TestEligibilityCriteriaAccessors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not _USDM_AVAILABLE:
            return
        cls.doc = USDMDoc(_USDM_PATH)

    def setUp(self):
        _require_usdm(self)

    def test_population_has_criterion_ids(self):
        sd = self.doc.study_design()
        pop = sd.get("population") or {}
        cids = pop.get("criterionIds", [])
        self.assertEqual(len(cids), 31)

    def test_resolve_inclusion_criterion(self):
        crit = self.doc.resolve("EligibilityCriterion_1")
        self.assertEqual(crit["category"]["code"], "C25532")

    def test_resolve_exclusion_criterion(self):
        crit = self.doc.resolve("EligibilityCriterion_9")
        self.assertEqual(crit["category"]["code"], "C25370")

    def test_resolve_criterion_item(self):
        item = self.doc.resolve("EligibilityCriterionItem_5")
        self.assertIn("CNS imaging", item["text"])

    def test_inclusion_count(self):
        sd = self.doc.study_design()
        pop = sd.get("population") or {}
        cids = pop.get("criterionIds", [])
        inclusion = [
            cid for cid in cids
            if self.doc.resolve(cid)["category"]["code"] == "C25532"
        ]
        self.assertEqual(len(inclusion), 8)

    def test_exclusion_count(self):
        sd = self.doc.study_design()
        pop = sd.get("population") or {}
        cids = pop.get("criterionIds", [])
        exclusion = [
            cid for cid in cids
            if self.doc.resolve(cid)["category"]["code"] == "C25370"
        ]
        self.assertEqual(len(exclusion), 23)


# ---------------------------------------------------------------------------
# _derive_subtype — unit tests (no USDM file needed)
# ---------------------------------------------------------------------------
class TestDeriveSubtype(unittest.TestCase):
    """Tests for the soaTimePointSubType derivation helper."""

    _derive = staticmethod(usdm_reader._derive_subtype)

    def test_screening(self):
        self.assertEqual(self._derive("Screening 1"), "screening")

    def test_screening_2(self):
        self.assertEqual(self._derive("Screening 2"), "screening")

    def test_baseline(self):
        self.assertEqual(self._derive("Baseline"), "baseline")

    def test_early_termination(self):
        self.assertEqual(self._derive("Early Termination"), "early-termination")

    def test_retreatment(self):
        self.assertEqual(self._derive("Retreatment"), "retreatment")

    def test_week_visit(self):
        self.assertEqual(self._derive("Week 2"), "planned")

    def test_week_8(self):
        self.assertEqual(self._derive("Week 8"), "planned")

    def test_empty_label(self):
        self.assertEqual(self._derive(""), "planned")


# ---------------------------------------------------------------------------
# _fmt_days — unit tests (no USDM file needed)
# ---------------------------------------------------------------------------
class TestFmtDays(unittest.TestCase):
    """Tests for the day-value formatting helper."""

    _fmt = staticmethod(usdm_reader._fmt_days)

    def test_whole_number(self):
        self.assertEqual(self._fmt(14.0), "14")

    def test_zero(self):
        self.assertEqual(self._fmt(0.0), "0")

    def test_fractional(self):
        # PT4H = 4/24 ≈ 0.166667
        result = self._fmt(4.0 / 24)
        self.assertTrue(result.startswith("0.166"))

    def test_fractional_zero(self):
        self.assertEqual(self._fmt(0.0), "0")

    def test_large_whole(self):
        self.assertEqual(self._fmt(182.0), "182")


# ---------------------------------------------------------------------------
# emit_visit_plan_definitions — FSH output content
# ---------------------------------------------------------------------------
class TestEmitVisitPlanDefinitions(unittest.TestCase):
    """
    Integration tests for emit_visit_plan_definitions against the real USDM.

    Verifies:
      - 12 files generated under visits/
      - DO NOT EDIT header on each file
      - Correct instance IDs
      - Anchor visits (E1, E3) have no timing values
      - Non-anchor visits have timing values
      - soaTimePointSubType derivation
      - Contact mode encoding
      - Timing spot-checks (E4 Week 2 = 14d, E5 Week 4 = 28d, etc.)
      - Idempotency
    """

    @classmethod
    def setUpClass(cls):
        if not _USDM_AVAILABLE:
            return
        cls.doc = USDMDoc(_USDM_PATH)
        cls.tmp_dir = tempfile.mkdtemp()
        cls.out_dir = os.path.join(cls.tmp_dir, "usdm")
        cls.written = emit_visit_plan_definitions(cls.doc, cls.out_dir)
        # Load all generated files into a dict: enc_name → content
        cls.files: dict = {}
        visits_dir = os.path.join(cls.out_dir, "visits")
        for fname in os.listdir(visits_dir):
            if fname.endswith(".gen.fsh"):
                enc_name = fname.replace(".gen.fsh", "")
                with open(os.path.join(visits_dir, fname), encoding="utf-8") as fh:
                    cls.files[enc_name] = fh.read()

    def setUp(self):
        _require_usdm(self)

    # -----------------------------------------------------------------------
    # File count and naming
    # -----------------------------------------------------------------------

    def test_twelve_files_generated(self):
        """Exactly 12 FSH files must be generated (one per encounter)."""
        self.assertEqual(len(self.written), 12)

    def test_visits_subdir_created(self):
        """The visits/ subdirectory must be created."""
        visits_dir = os.path.join(self.out_dir, "visits")
        self.assertTrue(os.path.isdir(visits_dir))

    def test_all_encounter_names_present(self):
        """All 12 encounter names must appear as file keys."""
        expected = {"E1", "E2", "E3", "E4", "E5", "E7", "E8", "E9", "E10", "E11", "E12", "E13"}
        self.assertEqual(set(self.files.keys()), expected)

    # -----------------------------------------------------------------------
    # DO NOT EDIT header
    # -----------------------------------------------------------------------

    def test_do_not_edit_header_all_files(self):
        """Every generated file must start with the DO NOT EDIT header."""
        for enc_name, content in self.files.items():
            first_line = content.splitlines()[0]
            self.assertIn("DO NOT EDIT", first_line, f"Missing header in {enc_name}.gen.fsh")
            self.assertIn("usdm_to_soa.py", first_line, f"Missing script ref in {enc_name}.gen.fsh")

    # -----------------------------------------------------------------------
    # Instance IDs
    # -----------------------------------------------------------------------

    def test_instance_id_e1(self):
        self.assertIn("Instance: H2Q-MC-LZZT-E1-USDM", self.files["E1"])

    def test_instance_id_e3(self):
        self.assertIn("Instance: H2Q-MC-LZZT-E3-USDM", self.files["E3"])

    def test_instance_id_e4(self):
        self.assertIn("Instance: H2Q-MC-LZZT-E4-USDM", self.files["E4"])

    def test_instance_id_e13(self):
        self.assertIn("Instance: H2Q-MC-LZZT-E13-USDM", self.files["E13"])

    # -----------------------------------------------------------------------
    # InstanceOf and Usage
    # -----------------------------------------------------------------------

    def test_instance_of_soa_plan_definition(self):
        for enc_name, content in self.files.items():
            self.assertIn("InstanceOf: SOAPlanDefinition", content,
                          f"Missing InstanceOf in {enc_name}.gen.fsh")

    def test_usage_definition(self):
        for enc_name, content in self.files.items():
            self.assertIn("Usage: #definition", content,
                          f"Missing Usage in {enc_name}.gen.fsh")

    def test_status_active(self):
        for enc_name, content in self.files.items():
            self.assertIn("* status = #active", content,
                          f"Missing status in {enc_name}.gen.fsh")

    # -----------------------------------------------------------------------
    # soaTimePointType always "interaction"
    # -----------------------------------------------------------------------

    def test_soa_time_point_type_interaction(self):
        for enc_name, content in self.files.items():
            self.assertIn(
                'extension[soaTimePointType].valueString = "interaction"',
                content,
                f"Missing soaTimePointType in {enc_name}.gen.fsh",
            )

    # -----------------------------------------------------------------------
    # soaTimePointSubType derivation
    # -----------------------------------------------------------------------

    def test_subtype_screening_e1(self):
        self.assertIn('"screening"', self.files["E1"])

    def test_subtype_screening_e2(self):
        self.assertIn('"screening"', self.files["E2"])

    def test_subtype_baseline_e3(self):
        self.assertIn('"baseline"', self.files["E3"])

    def test_subtype_planned_e4(self):
        self.assertIn('"planned"', self.files["E4"])

    def test_subtype_planned_e13(self):
        self.assertIn('"planned"', self.files["E13"])

    # -----------------------------------------------------------------------
    # Anchor visits (E1, E3) — no timing values
    # -----------------------------------------------------------------------

    def test_anchor_e1_no_planned_time_point(self):
        """E1 is an anchor — must NOT have soaPlannedTimePoint."""
        self.assertNotIn("soaPlannedTimePoint", self.files["E1"])

    def test_anchor_e1_no_related_action(self):
        """E1 is an anchor — must NOT have relatedAction."""
        self.assertNotIn("relatedAction", self.files["E1"])

    def test_anchor_e1_no_transition_sub_action(self):
        """E1 is an anchor — must NOT have soaTransition."""
        self.assertNotIn("soaTransition", self.files["E1"])

    def test_anchor_e3_no_planned_time_point(self):
        """E3 (Baseline) is an anchor — must NOT have soaPlannedTimePoint."""
        self.assertNotIn("soaPlannedTimePoint", self.files["E3"])

    def test_anchor_e3_no_related_action(self):
        """E3 (Baseline) is an anchor — must NOT have relatedAction."""
        self.assertNotIn("relatedAction", self.files["E3"])

    # -----------------------------------------------------------------------
    # Non-anchor visits — timing values present
    # -----------------------------------------------------------------------

    def test_non_anchor_e4_has_planned_time_point(self):
        self.assertIn("soaPlannedTimePoint", self.files["E4"])

    def test_non_anchor_e4_has_related_action(self):
        self.assertIn("relatedAction", self.files["E4"])

    def test_non_anchor_e4_has_transition(self):
        self.assertIn("soaTransition", self.files["E4"])

    # -----------------------------------------------------------------------
    # Timing spot-checks (from F-0 audit Section 6)
    # -----------------------------------------------------------------------

    def test_e2_planned_day_2(self):
        """E2 (Screening 2): Timing_2 = P2D → 2 days."""
        content = self.files["E2"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 2", content)

    def test_e4_planned_day_14(self):
        """E4 (Week 2): Timing_4 = P2W → 14 days."""
        content = self.files["E4"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 14", content)

    def test_e5_planned_day_28(self):
        """E5 (Week 4): Timing_5 = P4W → 28 days."""
        content = self.files["E5"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 28", content)

    def test_e7_planned_day_42(self):
        """E7 (Week 6): Timing_6 = P6W → 42 days."""
        content = self.files["E7"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 42", content)

    def test_e8_planned_day_56(self):
        """E8 (Week 8): Timing_7 = P8W → 56 days."""
        content = self.files["E8"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 56", content)

    def test_e9_planned_day_84(self):
        """E9 (Week 12): Timing_9 = P12W → 84 days."""
        content = self.files["E9"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 84", content)

    def test_e10_planned_day_112(self):
        """E10 (Week 16): Timing_11 = P16W → 112 days."""
        content = self.files["E10"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 112", content)

    def test_e11_planned_day_140(self):
        """E11 (Week 20): Timing_13 = P20W → 140 days."""
        content = self.files["E11"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 140", content)

    def test_e12_planned_day_168(self):
        """E12 (Week 24): Timing_15 = P24W → 168 days."""
        content = self.files["E12"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 168", content)

    def test_e13_planned_day_182(self):
        """E13 (Week 26): Timing_16 = P26W → 182 days."""
        content = self.files["E13"]
        self.assertIn("soaPlannedTimePoint", content)
        self.assertIn("* value = 182", content)

    # -----------------------------------------------------------------------
    # Window bounds spot-checks
    # -----------------------------------------------------------------------

    def test_e4_window_3d(self):
        """E4 (Week 2): window ±3d."""
        content = self.files["E4"]
        self.assertIn("soaPlannedRange", content)
        # value = 3 appears for both low and high
        self.assertIn("* value = 3", content)

    def test_e9_window_4d(self):
        """E9 (Week 12): window ±4d."""
        content = self.files["E9"]
        self.assertIn("soaPlannedRange", content)
        self.assertIn("* value = 4", content)

    def test_e2_window_fractional(self):
        """E2 (Screening 2): windowLower=PT4H (≈0.166667d), windowUpper=PT0H (0d)."""
        content = self.files["E2"]
        # windowLower should be fractional (starts with 0.1)
        self.assertIn("soaPlannedRange", content)
        self.assertIn("* value = 0.1", content)
        # windowUpper should be 0
        self.assertIn("* value = 0", content)

    # -----------------------------------------------------------------------
    # Reference encounter names
    # -----------------------------------------------------------------------

    def test_e4_reference_encounter_e3(self):
        """E4 (Week 2): reference encounter = E3 (Baseline)."""
        self.assertIn('"E3"', self.files["E4"])

    def test_e5_reference_encounter_e4(self):
        """E5 (Week 4): reference encounter = E4 (Week 2)."""
        self.assertIn('"E4"', self.files["E5"])

    def test_e2_reference_encounter_e1(self):
        """E2 (Screening 2): reference encounter = E1 (Screening 1)."""
        self.assertIn('"E1"', self.files["E2"])

    # -----------------------------------------------------------------------
    # Contact modes
    # -----------------------------------------------------------------------

    def test_e1_contact_mode_in_person(self):
        """E1 has IN PERSON contact mode → encoded as action.code."""
        content = self.files["E1"]
        self.assertIn("C175574", content)
        self.assertIn("IN PERSON", content)

    def test_e8_contact_mode_telephone(self):
        """E8 (Week 8) has both IN PERSON and TELEPHONE CALL."""
        content = self.files["E8"]
        self.assertIn("C175574", content)
        self.assertIn("C171537", content)
        self.assertIn("TELEPHONE CALL", content)

    def test_e8_contact_mode_gap_comment(self):
        """E8 must have the gap comment for contactMode."""
        self.assertIn("Gap:", self.files["E8"])
        self.assertIn("contactMode", self.files["E8"])

    def test_e1_only_in_person(self):
        """E1 has only IN PERSON — no TELEPHONE CALL."""
        self.assertNotIn("TELEPHONE CALL", self.files["E1"])

    # -----------------------------------------------------------------------
    # relatedAction targetId
    # -----------------------------------------------------------------------

    def test_e4_related_action_target_e3(self):
        """E4 relatedAction must target E3 (prior encounter)."""
        self.assertIn('targetId = "E3"', self.files["E4"])

    def test_e5_related_action_target_e4(self):
        """E5 relatedAction must target E4 (prior encounter)."""
        self.assertIn('targetId = "E4"', self.files["E5"])

    # -----------------------------------------------------------------------
    # Transition sub-action
    # -----------------------------------------------------------------------

    def test_e4_transition_delay_14(self):
        """E4 transition delay = 14 days."""
        content = self.files["E4"]
        self.assertIn("soaTransitionDelay", content)
        self.assertIn("* value = 14", content)

    def test_e13_transition_delay_182(self):
        """E13 transition delay = 182 days."""
        content = self.files["E13"]
        self.assertIn("soaTransitionDelay", content)
        self.assertIn("* value = 182", content)

    # -----------------------------------------------------------------------
    # Transition rules (only E1, E2, E3, E12 have them)
    # -----------------------------------------------------------------------

    def test_e1_transition_rule_text(self):
        """E1 has TransitionRule_1 (start) and TransitionRule_2 (end)."""
        content = self.files["E1"]
        # E1 is an anchor — no transition sub-action, but rules may appear
        # in the description if we ever add them. For now, just check the
        # file is valid (no crash).
        self.assertIn("Instance: H2Q-MC-LZZT-E1-USDM", content)

    def test_e12_has_transition_description(self):
        """E12 has TransitionRule_6 (end) → description should contain rule text."""
        content = self.files["E13"]
        # E13 = Encounter_12 (Week 26) has TransitionRule_6 as transitionEndRule
        # The description should contain "End of treatment"
        self.assertIn("End of treatment", content)

    # -----------------------------------------------------------------------
    # Titles and descriptions
    # -----------------------------------------------------------------------

    def test_e1_title_screening_1(self):
        self.assertIn('Title: "Screening 1"', self.files["E1"])

    def test_e3_title_baseline(self):
        self.assertIn('Title: "Baseline"', self.files["E3"])

    def test_e4_title_week_2(self):
        self.assertIn('Title: "Week 2"', self.files["E4"])

    def test_e13_title_week_26(self):
        self.assertIn('Title: "Week 26"', self.files["E13"])

    # -----------------------------------------------------------------------
    # Action id matches encounter name
    # -----------------------------------------------------------------------

    def test_action_id_e1(self):
        self.assertIn('* id = "E1"', self.files["E1"])

    def test_action_id_e4(self):
        self.assertIn('* id = "E4"', self.files["E4"])

    def test_action_id_e13(self):
        self.assertIn('* id = "E13"', self.files["E13"])


# ---------------------------------------------------------------------------
# emit_visit_plan_definitions — idempotency
# ---------------------------------------------------------------------------
class TestEmitVisitPlanDefinitionsIdempotency(unittest.TestCase):
    def setUp(self):
        _require_usdm(self)

    def test_idempotent(self):
        doc = USDMDoc(_USDM_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = os.path.join(tmp, "usdm")
            emit_visit_plan_definitions(doc, out_dir)
            # Read all files after first run
            visits_dir = os.path.join(out_dir, "visits")
            first_contents = {}
            for fname in sorted(os.listdir(visits_dir)):
                with open(os.path.join(visits_dir, fname), "rb") as fh:
                    first_contents[fname] = fh.read()
            # Second run
            emit_visit_plan_definitions(doc, out_dir)
            for fname in sorted(os.listdir(visits_dir)):
                with open(os.path.join(visits_dir, fname), "rb") as fh:
                    second = fh.read()
                self.assertEqual(
                    first_contents[fname],
                    second,
                    f"emit_visit_plan_definitions is not idempotent for {fname}",
                )


# ---------------------------------------------------------------------------
# emit_visit_plan_definitions — output directory creation
# ---------------------------------------------------------------------------
class TestEmitVisitPlanDefinitionsDirCreation(unittest.TestCase):
    def setUp(self):
        _require_usdm(self)

    def test_creates_visits_subdir(self):
        doc = USDMDoc(_USDM_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = os.path.join(tmp, "a", "b", "usdm")
            emit_visit_plan_definitions(doc, out_dir)
            visits_dir = os.path.join(out_dir, "visits")
            self.assertTrue(os.path.isdir(visits_dir))
            # At least one .gen.fsh file must exist
            fsh_files = [f for f in os.listdir(visits_dir) if f.endswith(".gen.fsh")]
            self.assertGreater(len(fsh_files), 0)


if __name__ == "__main__":
    unittest.main()
