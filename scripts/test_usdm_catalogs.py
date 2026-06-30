#!/usr/bin/env python3
"""
test_usdm_catalogs.py — Unit tests for usdm_catalogs.py (Task F-5).

Run with:
    python3 -m unittest discover scripts/
or:
    python3 -m unittest scripts.test_usdm_catalogs
"""

import csv
import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest

# ---------------------------------------------------------------------------
# Load the module under test via importlib so the test runner can find it
# regardless of sys.path configuration.
# ---------------------------------------------------------------------------
_HERE = pathlib.Path(__file__).resolve().parent
_MOD_PATH = _HERE / "usdm_catalogs.py"
_spec = importlib.util.spec_from_file_location("usdm_catalogs", _MOD_PATH)
usdm_catalogs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(usdm_catalogs)

# Real USDM file path (used for integration tests)
_USDM_PATH = str(
    pathlib.Path(__file__).resolve().parent.parent
    / "input/usdm/CDISC_Pilot_Study_v4_FIXED.json"
)

# ---------------------------------------------------------------------------
# Minimal USDM fixture builder
# ---------------------------------------------------------------------------

def _make_usdm(activities=None, bcs=None, bcc=None, bcs_surrogates=None):
    """
    Build a minimal USDM JSON dict suitable for writing to a temp file.

    USDM v4 nesting (mirrors the real CDISC Pilot Study JSON):
      study.versions[0]
        .studyDesigns[0]   → activities (and encounters, etc.)
        .biomedicalConcepts[]   → BCs (at versions[0] level, NOT studyDesigns[0])
        .bcCategories[]         → BCCategories (at versions[0] level)
        .bcSurrogates[]         → BCSurrogates (at versions[0] level)
    """
    return {
        "study": {
            "id": "Study_1",
            "name": "TEST",
            "versions": [
                {
                    "id": "StudyVersion_1",
                    # BCs, BCCategories, BCSurrogates at versions[0] level
                    "biomedicalConcepts": bcs or [],
                    "bcCategories": bcc or [],
                    "bcSurrogates": bcs_surrogates or [],
                    "studyDesigns": [
                        {
                            "id": "StudyDesign_1",
                            "activities": activities or [],
                        }
                    ],
                }
            ],
        }
    }


def _write_usdm(data: dict) -> str:
    """Write USDM dict to a temp file and return the path."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump(data, tmp)
    tmp.close()
    return tmp.name


# ---------------------------------------------------------------------------
# Helper: minimal BC object
# ---------------------------------------------------------------------------

def _bc(bc_id, label, code="C001", code_system="http://www.cdisc.org",
        decode="Test BC", unit_decode="", datatype="float"):
    """Build a minimal BiomedicalConcept dict."""
    props = []
    if datatype:
        props.append({
            "id": f"Prop_{bc_id}_ORRES",
            "name": "VSORRES_x",
            "label": "VSORRES",
            "isRequired": True,
            "isEnabled": True,
            "datatype": datatype,
            "responseCodes": [],
            "code": {
                "id": f"AC_{bc_id}_ORRES",
                "standardCode": {
                    "id": f"Code_{bc_id}_ORRES",
                    "code": "C70856",
                    "codeSystem": "http://www.cdisc.org",
                    "decode": "Observation Result",
                    "instanceType": "Code",
                },
                "standardCodeAliases": [],
                "instanceType": "AliasCode",
            },
            "notes": [],
            "instanceType": "BiomedicalConceptProperty",
        })
    if unit_decode:
        props.append({
            "id": f"Prop_{bc_id}_ORRESU",
            "name": "VSORRESU_x",
            "label": "VSORRESU",
            "isRequired": True,
            "isEnabled": True,
            "datatype": "",
            "responseCodes": [
                {
                    "id": f"RC_{bc_id}_unit",
                    "name": "RC_unit",
                    "label": "",
                    "isEnabled": True,
                    "code": {
                        "id": f"Code_{bc_id}_unit",
                        "code": "C_UNIT",
                        "codeSystem": "http://www.cdisc.org",
                        "decode": unit_decode,
                        "instanceType": "Code",
                    },
                    "instanceType": "ResponseCode",
                }
            ],
            "code": {
                "id": f"AC_{bc_id}_ORRESU",
                "standardCode": {
                    "id": f"Code_{bc_id}_ORRESU",
                    "code": "C_UNIT_TYPE",
                    "codeSystem": "http://www.cdisc.org",
                    "decode": "Unit",
                    "instanceType": "Code",
                },
                "standardCodeAliases": [],
                "instanceType": "AliasCode",
            },
            "notes": [],
            "instanceType": "BiomedicalConceptProperty",
        })
    return {
        "id": bc_id,
        "name": label,
        "label": label,
        "synonyms": [],
        "reference": "",
        "properties": props,
        "code": {
            "id": f"AC_{bc_id}",
            "standardCode": {
                "id": f"Code_{bc_id}",
                "code": code,
                "codeSystem": code_system,
                "decode": decode,
                "instanceType": "Code",
            },
            "standardCodeAliases": [],
            "instanceType": "AliasCode",
        },
        "notes": [],
        "instanceType": "BiomedicalConcept",
    }


def _activity(act_id, label, bc_ids=None, bcs_ids=None, bcc_ids=None, procs=None):
    """Build a minimal Activity dict."""
    return {
        "id": act_id,
        "name": f"ACT_{act_id}",
        "label": label,
        "description": "",
        "previousId": None,
        "nextId": None,
        "childIds": [],
        "definedProcedures": procs or [],
        "biomedicalConceptIds": bc_ids or [],
        "bcCategoryIds": bcc_ids or [],
        "bcSurrogateIds": bcs_ids or [],
        "timelineId": None,
        "notes": [],
        "instanceType": "Activity",
    }


def _procedure(proc_id, code, code_system="SNOMED", decode="Test procedure"):
    return {
        "id": proc_id,
        "name": f"PR_{proc_id}",
        "label": decode,
        "description": "",
        "procedureType": "Test",
        "code": {
            "id": f"Code_{proc_id}",
            "code": code,
            "codeSystem": code_system,
            "decode": decode,
            "instanceType": "Code",
        },
        "studyInterventionId": None,
        "notes": [],
        "instanceType": "Procedure",
    }


def _surrogate(surr_id, label):
    return {
        "id": surr_id,
        "name": label,
        "label": label,
        "description": "",
        "reference": "None set",
        "notes": [],
        "instanceType": "BiomedicalConceptSurrogate",
    }


# ===========================================================================
# Tests: _slugify
# ===========================================================================

class TestSlugify(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(usdm_catalogs._slugify("Hello World"), "hello-world")

    def test_spaces_to_hyphens(self):
        self.assertEqual(usdm_catalogs._slugify("Vital Signs"), "vital-signs")

    def test_special_chars_stripped(self):
        self.assertEqual(usdm_catalogs._slugify("ADAS-Cog"), "adas-cog")

    def test_slash_to_hyphen(self):
        self.assertEqual(usdm_catalogs._slugify("Supine/Standing"), "supine-standing")

    def test_comma_to_hyphen(self):
        # " , " (space-comma-space) collapses to a single hyphen
        result = usdm_catalogs._slugify("Study drug record , Medications dispensed")
        self.assertEqual(result, "study-drug-record-medications-dispensed")

    def test_multiple_hyphens_collapsed(self):
        result = usdm_catalogs._slugify("A  B")
        self.assertNotIn("--", result)


# ===========================================================================
# Tests: _extract_unit
# ===========================================================================

class TestExtractUnit(unittest.TestCase):
    def test_unit_from_response_code(self):
        bc = _bc("BC_1", "Temperature", unit_decode="Degree Celsius")
        self.assertEqual(usdm_catalogs._extract_unit(bc), "Degree Celsius")

    def test_no_unit_returns_empty(self):
        bc = _bc("BC_2", "Sex", unit_decode="", datatype="string")
        self.assertEqual(usdm_catalogs._extract_unit(bc), "")

    def test_unit_from_kilogram(self):
        bc = _bc("BC_3", "Weight", unit_decode="Kilogram")
        self.assertEqual(usdm_catalogs._extract_unit(bc), "Kilogram")


# ===========================================================================
# Tests: _extract_datatype
# ===========================================================================

class TestExtractDatatype(unittest.TestCase):
    def test_float_is_quantity(self):
        bc = _bc("BC_1", "Temp", datatype="float")
        self.assertEqual(usdm_catalogs._extract_datatype(bc), "Quantity")

    def test_integer_is_quantity(self):
        bc = _bc("BC_2", "SBP", datatype="integer")
        self.assertEqual(usdm_catalogs._extract_datatype(bc), "Quantity")

    def test_string_is_string(self):
        bc = _bc("BC_3", "Sex", datatype="string")
        self.assertEqual(usdm_catalogs._extract_datatype(bc), "string")

    def test_no_datatype_defaults_string(self):
        bc = _bc("BC_4", "Unknown", datatype="")
        # No VSORRES property → defaults to "string"
        self.assertEqual(usdm_catalogs._extract_datatype(bc), "string")


# ===========================================================================
# Tests: extract_activity_catalog (unit / fixture-based)
# ===========================================================================

class TestExtractActivityCatalogUnit(unittest.TestCase):
    def _run(self, activities, bcs=None, bcc=None, bcs_surrogates=None):
        data = _make_usdm(activities, bcs, bcc, bcs_surrogates)
        path = _write_usdm(data)
        return usdm_catalogs.extract_activity_catalog(path)

    def test_measurement_activity(self):
        bc = _bc("BC_1", "Temperature", code="C174446",
                 decode="TEMP", unit_decode="Degree Celsius")
        act = _activity("Act_1", "Temperature", bc_ids=["BC_1"])
        rows = self._run([act], bcs=[bc])
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["archetype"], "measurement")
        self.assertEqual(r["code"], "C174446")
        self.assertEqual(r["unit"], "Degree Celsius")
        self.assertEqual(r["result_obsdef_id"], "temperature-obs")
        self.assertEqual(r["questionnaire_id"], "")
        self.assertEqual(r["respondent_type"], "")

    def test_procedure_activity(self):
        proc = _procedure("Proc_1", "383371000119108", "SNOMED", "CT of head")
        act = _activity("Act_2", "CT scan", procs=[proc])
        rows = self._run([act])
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["archetype"], "procedure")
        self.assertEqual(r["code"], "383371000119108")
        self.assertEqual(r["code_system"], "SNOMED")
        self.assertEqual(r["result_obsdef_id"], "")
        self.assertEqual(r["questionnaire_id"], "")

    def test_instrument_activity_known_surrogate(self):
        surr = _surrogate("BiomedicalConceptSurrogate_3", "MMSE")
        act = _activity("Act_3", "MMSE", bcs_ids=["BiomedicalConceptSurrogate_3"])
        rows = self._run([act], bcs_surrogates=[surr])
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["archetype"], "instrument")
        self.assertEqual(r["respondent_type"], "practitioner")
        self.assertEqual(r["questionnaire_id"], "mmse")
        self.assertEqual(r["result_obsdef_id"], "")

    def test_instrument_patient_respondent(self):
        surr = _surrogate("BiomedicalConceptSurrogate_5", "Placebo TTS test")
        act = _activity("Act_4", "Placebo TTS test",
                        bcs_ids=["BiomedicalConceptSurrogate_5"])
        rows = self._run([act], bcs_surrogates=[surr])
        self.assertEqual(rows[0]["respondent_type"], "patient")

    def test_bc_wins_over_procedure(self):
        """biomedicalConceptIds takes precedence over definedProcedures."""
        bc = _bc("BC_7", "Physical Exam", code="C83119", decode="Physical Examination")
        proc = _procedure("Proc_5", "5880005", "SNOMED", "Physical examination")
        act = _activity("Act_7", "Physical examination",
                        bc_ids=["BC_7"], procs=[proc])
        rows = self._run([act], bcs=[bc])
        self.assertEqual(rows[0]["archetype"], "measurement")

    def test_unclassified_activity_skipped(self):
        """Activity with no BC/surrogate/procedure is skipped (not in output)."""
        act = _activity("Act_0", "")  # empty label, no refs
        rows = self._run([act])
        self.assertEqual(len(rows), 0)

    def test_duplicate_label_gets_unique_id(self):
        """Two activities with the same label get unique slugified ids."""
        bc1 = _bc("BC_1", "ECG", code="C001", decode="ECG")
        bc2 = _bc("BC_2", "ECG", code="C002", decode="ECG2")
        act1 = _activity("Act_1", "ECG", bc_ids=["BC_1"])
        act2 = _activity("Act_2", "ECG", bc_ids=["BC_2"])
        rows = self._run([act1, act2], bcs=[bc1, bc2])
        ids = [r["id"] for r in rows]
        self.assertEqual(len(set(ids)), 2, f"Expected unique ids, got: {ids}")

    def test_oid_and_oidsys_empty(self):
        bc = _bc("BC_1", "Test", code="C001", decode="Test")
        act = _activity("Act_1", "Test", bc_ids=["BC_1"])
        rows = self._run([act], bcs=[bc])
        self.assertEqual(rows[0]["oid"], "")
        self.assertEqual(rows[0]["oidsys"], "")

    def test_default_condition_empty(self):
        bc = _bc("BC_1", "Test", code="C001", decode="Test")
        act = _activity("Act_1", "Test", bc_ids=["BC_1"])
        rows = self._run([act], bcs=[bc])
        self.assertEqual(rows[0]["default_condition"], "")

    def test_category_activity_is_measurement(self):
        """Activity with bcCategoryIds → archetype = measurement."""
        cat = {
            "id": "BCCat_1",
            "name": "VS_Cat1",
            "label": "Vital Signs Category",
            "description": "",
            "code": None,
            "childIds": [],
            "memberIds": ["BC_1"],
            "instanceType": "BiomedicalConceptCategory",
            "notes": [],
        }
        bc = _bc("BC_1", "SBP", code="C25298", decode="SYSBP")
        act = _activity("Act_13", "Vital Signs and Temperature", bcc_ids=["BCCat_1"])
        rows = self._run([act], bcs=[bc], bcc=[cat])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["archetype"], "measurement")


# ===========================================================================
# Tests: extract_observation_catalog (unit / fixture-based)
# ===========================================================================

class TestExtractObservationCatalogUnit(unittest.TestCase):
    def _run(self, activities=None, bcs=None, bcc=None, bcs_surrogates=None):
        data = _make_usdm(activities=activities, bcs=bcs, bcc=bcc,
                          bcs_surrogates=bcs_surrogates)
        path = _write_usdm(data)
        return usdm_catalogs.extract_observation_catalog(path)

    def test_analyte_row_created(self):
        bc = _bc("BC_1", "Temperature", code="C174446",
                 decode="TEMP", unit_decode="Degree Celsius")
        act = _activity("Act_1", "Temperature", bc_ids=["BC_1"])
        rows = self._run(activities=[act], bcs=[bc])
        analytes = [r for r in rows if r["kind"] == "analyte"]
        self.assertEqual(len(analytes), 1)
        r = analytes[0]
        self.assertEqual(r["obsdef_id"], "temperature-obs")
        self.assertEqual(r["code"], "C174446")
        self.assertEqual(r["unit"], "Degree Celsius")
        self.assertEqual(r["datatype"], "Quantity")

    def test_panel_row_created(self):
        cat = {
            "id": "BCCat_1",
            "name": "VS_Cat1",
            "label": "Vital Signs Category",
            "description": "",
            "code": None,
            "childIds": [],
            "memberIds": ["BC_1"],
            "instanceType": "BiomedicalConceptCategory",
            "notes": [],
        }
        bc = _bc("BC_1", "SBP", code="C25298", decode="SYSBP")
        act = _activity("Act_13", "Vital Signs and Temperature", bcc_ids=["BCCat_1"])
        rows = self._run(activities=[act], bcs=[bc], bcc=[cat])
        panels = [r for r in rows if r["kind"] == "panel"]
        self.assertEqual(len(panels), 1)
        self.assertEqual(panels[0]["datatype"], "")
        self.assertEqual(panels[0]["unit"], "")

    def test_member_of_links_analyte_to_panel(self):
        """Activity with bcCategoryIds gets analyte row with member_of = panel."""
        cat = {
            "id": "BCCat_1",
            "name": "VS_Cat1",
            "label": "Vital Signs Category",
            "description": "",
            "code": None,
            "childIds": [],
            "memberIds": ["BC_1"],
            "instanceType": "BiomedicalConceptCategory",
            "notes": [],
        }
        bc = _bc("BC_1", "SBP", code="C25298", decode="SYSBP")
        act = _activity("Act_13", "Vital Signs and Temperature", bcc_ids=["BCCat_1"])
        rows = self._run(activities=[act], bcs=[bc], bcc=[cat])
        panel = next(r for r in rows if r["kind"] == "panel")
        analyte = next(r for r in rows if r["kind"] == "analyte")
        self.assertEqual(analyte["member_of"], panel["obsdef_id"])

    def test_analyte_not_in_panel_has_empty_member_of(self):
        bc = _bc("BC_1", "ECG", code="C62085", decode="ECG Measurement")
        act = _activity("Act_1", "ECG", bc_ids=["BC_1"])
        rows = self._run(activities=[act], bcs=[bc])
        analyte = next(r for r in rows if r["kind"] == "analyte")
        self.assertEqual(analyte["member_of"], "")

    def test_string_datatype_for_non_numeric(self):
        bc = _bc("BC_1", "Sex", code="C28421", decode="Sex", datatype="string")
        act = _activity("Act_1", "Sex", bc_ids=["BC_1"])
        rows = self._run(activities=[act], bcs=[bc])
        analyte = next(r for r in rows if r["kind"] == "analyte")
        self.assertEqual(analyte["datatype"], "string")

    def test_obsdef_id_uniqueness(self):
        bc1 = _bc("BC_1", "ECG", code="C001", decode="ECG")
        bc2 = _bc("BC_2", "ECG", code="C002", decode="ECG2")
        act1 = _activity("Act_1", "ECG", bc_ids=["BC_1"])
        act2 = _activity("Act_2", "ECG", bc_ids=["BC_2"])
        rows = self._run(activities=[act1, act2], bcs=[bc1, bc2])
        ids = [r["obsdef_id"] for r in rows]
        self.assertEqual(len(set(ids)), len(ids), f"Duplicate obsdef_ids: {ids}")

    def test_instrument_activity_has_no_observation_row(self):
        """Instrument activities should not produce observation rows."""
        surr = _surrogate("BiomedicalConceptSurrogate_3", "MMSE")
        act = _activity("Act_3", "MMSE", bcs_ids=["BiomedicalConceptSurrogate_3"])
        rows = self._run(activities=[act], bcs_surrogates=[surr])
        analytes = [r for r in rows if r["kind"] == "analyte"]
        self.assertEqual(len(analytes), 0)

    def test_procedure_activity_has_no_observation_row(self):
        """Procedure activities should not produce observation rows."""
        proc = _procedure("Proc_1", "383371000119108", "SNOMED", "CT of head")
        act = _activity("Act_1", "CT scan", procs=[proc])
        rows = self._run(activities=[act])
        analytes = [r for r in rows if r["kind"] == "analyte"]
        self.assertEqual(len(analytes), 0)


# ===========================================================================
# Tests: write_activity_catalog / write_observation_catalog
# ===========================================================================

class TestWriteCatalogs(unittest.TestCase):
    def test_activity_csv_has_comment_header(self):
        rows = [{f: "" for f in usdm_catalogs.ACTIVITY_FIELDS}]
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".csv", delete=False
        ) as tmp:
            path = tmp.name
        usdm_catalogs.write_activity_catalog(rows, path)
        with open(path, encoding="utf-8") as f:
            first_line = f.readline().strip()
        self.assertEqual(
            first_line,
            "# DO NOT EDIT — generated by scripts/usdm_to_soa.py",
        )

    def test_observation_csv_has_comment_header(self):
        rows = [{f: "" for f in usdm_catalogs.OBSERVATION_FIELDS}]
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".csv", delete=False
        ) as tmp:
            path = tmp.name
        usdm_catalogs.write_observation_catalog(rows, path)
        with open(path, encoding="utf-8") as f:
            first_line = f.readline().strip()
        self.assertEqual(
            first_line,
            "# DO NOT EDIT — generated by scripts/usdm_to_soa.py",
        )

    def test_activity_csv_columns_match_schema(self):
        rows = [{f: "x" for f in usdm_catalogs.ACTIVITY_FIELDS}]
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".csv", delete=False
        ) as tmp:
            path = tmp.name
        usdm_catalogs.write_activity_catalog(rows, path)
        with open(path, encoding="utf-8") as f:
            f.readline()  # skip comment
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
        self.assertEqual(list(fieldnames), usdm_catalogs.ACTIVITY_FIELDS)

    def test_observation_csv_columns_match_schema(self):
        rows = [{f: "x" for f in usdm_catalogs.OBSERVATION_FIELDS}]
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".csv", delete=False
        ) as tmp:
            path = tmp.name
        usdm_catalogs.write_observation_catalog(rows, path)
        with open(path, encoding="utf-8") as f:
            f.readline()  # skip comment
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
        self.assertEqual(list(fieldnames), usdm_catalogs.OBSERVATION_FIELDS)


# ===========================================================================
# Integration tests: real USDM file
# ===========================================================================

@unittest.skipUnless(
    pathlib.Path(_USDM_PATH).exists(),
    "Real USDM file not found — skipping integration tests",
)
class TestRealUSDMIntegration(unittest.TestCase):
    """Integration tests against the real CDISC Pilot Study USDM JSON."""

    @classmethod
    def setUpClass(cls):
        cls.act_rows = usdm_catalogs.extract_activity_catalog(_USDM_PATH)
        cls.obs_rows = usdm_catalogs.extract_observation_catalog(_USDM_PATH)

    # --- Activity catalog ---

    def test_36_leaf_activities_classified(self):
        """Exactly 36 leaf activities must be classified (4 header rows skipped)."""
        self.assertEqual(len(self.act_rows), 36,
                         f"Expected 36 rows, got {len(self.act_rows)}: "
                         f"{[r['id'] for r in self.act_rows]}")

    def test_no_duplicate_activity_ids(self):
        ids = [r["id"] for r in self.act_rows]
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate ids: {ids}")

    def test_all_archetypes_valid(self):
        valid = {"measurement", "instrument", "procedure"}
        for r in self.act_rows:
            self.assertIn(r["archetype"], valid,
                          f"Bad archetype on {r['id']}: {r['archetype']!r}")

    def test_measurement_has_result_obsdef_id(self):
        for r in self.act_rows:
            if r["archetype"] == "measurement":
                self.assertTrue(
                    r["result_obsdef_id"],
                    f"Measurement {r['id']} missing result_obsdef_id",
                )

    def test_procedure_has_empty_result_obsdef_id(self):
        for r in self.act_rows:
            if r["archetype"] == "procedure":
                self.assertEqual(
                    r["result_obsdef_id"], "",
                    f"Procedure {r['id']} should have empty result_obsdef_id",
                )

    def test_procedure_has_non_empty_code(self):
        for r in self.act_rows:
            if r["archetype"] == "procedure":
                self.assertTrue(
                    r["code"],
                    f"Procedure {r['id']} missing code",
                )

    def test_instrument_has_questionnaire_id(self):
        for r in self.act_rows:
            if r["archetype"] == "instrument":
                self.assertTrue(
                    r["questionnaire_id"],
                    f"Instrument {r['id']} missing questionnaire_id",
                )

    def test_instrument_has_respondent_type(self):
        for r in self.act_rows:
            if r["archetype"] == "instrument":
                self.assertTrue(
                    r["respondent_type"],
                    f"Instrument {r['id']} missing respondent_type",
                )

    def test_measurement_has_empty_respondent_type(self):
        for r in self.act_rows:
            if r["archetype"] == "measurement":
                self.assertEqual(
                    r["respondent_type"], "",
                    f"Measurement {r['id']} should have empty respondent_type",
                )

    def test_procedure_has_empty_respondent_type(self):
        for r in self.act_rows:
            if r["archetype"] == "procedure":
                self.assertEqual(
                    r["respondent_type"], "",
                    f"Procedure {r['id']} should have empty respondent_type",
                )

    def test_informed_consent_is_measurement(self):
        row = next((r for r in self.act_rows if "informed-consent" in r["id"]), None)
        self.assertIsNotNone(row, "informed-consent activity not found")
        self.assertEqual(row["archetype"], "measurement")

    def test_mmse_is_instrument_practitioner(self):
        row = next((r for r in self.act_rows if r["id"] == "mmse"), None)
        self.assertIsNotNone(row, "mmse activity not found")
        self.assertEqual(row["archetype"], "instrument")
        self.assertEqual(row["respondent_type"], "practitioner")

    def test_placebo_tts_test_is_instrument_patient(self):
        row = next((r for r in self.act_rows if "placebo-tts-test" in r["id"]), None)
        self.assertIsNotNone(row, "placebo-tts-test activity not found")
        self.assertEqual(row["archetype"], "instrument")
        self.assertEqual(row["respondent_type"], "patient")

    def test_ct_scan_is_procedure(self):
        row = next((r for r in self.act_rows if "ct-scan" in r["id"]), None)
        self.assertIsNotNone(row, "ct-scan activity not found")
        self.assertEqual(row["archetype"], "procedure")

    def test_physical_examination_is_measurement_bc_wins(self):
        """Physical examination has both BC and procedure — BC must win."""
        row = next(
            (r for r in self.act_rows if "physical-examination" in r["id"]), None
        )
        self.assertIsNotNone(row, "physical-examination activity not found")
        self.assertEqual(row["archetype"], "measurement",
                         "BC should win over procedure for physical examination")

    def test_vital_signs_and_temperature_is_measurement(self):
        row = next(
            (r for r in self.act_rows if "vital-signs-and-temperature" in r["id"]),
            None,
        )
        self.assertIsNotNone(row, "vital-signs-and-temperature activity not found")
        self.assertEqual(row["archetype"], "measurement")

    def test_archetype_counts(self):
        from collections import Counter
        counts = Counter(r["archetype"] for r in self.act_rows)
        # Verify we have all three archetypes present
        self.assertIn("measurement", counts)
        self.assertIn("instrument", counts)
        self.assertIn("procedure", counts)
        # 5 instruments (one per BCSurrogate)
        self.assertEqual(counts["instrument"], 5,
                         f"Expected 5 instruments, got {counts['instrument']}")

    # --- Observation catalog ---

    def test_observation_catalog_non_empty(self):
        self.assertGreater(len(self.obs_rows), 0)

    def test_observation_catalog_has_panels(self):
        panels = [r for r in self.obs_rows if r["kind"] == "panel"]
        self.assertGreater(len(panels), 0, "Expected at least one panel row")

    def test_observation_catalog_has_analytes(self):
        analytes = [r for r in self.obs_rows if r["kind"] == "analyte"]
        self.assertGreater(len(analytes), 0, "Expected at least one analyte row")

    def test_no_duplicate_obsdef_ids(self):
        ids = [r["obsdef_id"] for r in self.obs_rows]
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate obsdef_ids: {ids}")

    def test_all_kinds_valid(self):
        valid = {"analyte", "panel"}
        for r in self.obs_rows:
            self.assertIn(r["kind"], valid,
                          f"Bad kind on {r['obsdef_id']}: {r['kind']!r}")

    def test_panel_member_of_is_empty(self):
        for r in self.obs_rows:
            if r["kind"] == "panel":
                self.assertEqual(
                    r["member_of"], "",
                    f"Panel {r['obsdef_id']} should have empty member_of",
                )

    def test_member_of_references_valid_panel(self):
        panel_ids = {r["obsdef_id"] for r in self.obs_rows if r["kind"] == "panel"}
        for r in self.obs_rows:
            if r["member_of"]:
                self.assertIn(
                    r["member_of"], panel_ids,
                    f"{r['obsdef_id']} member_of {r['member_of']!r} is not a panel",
                )

    def test_category_activities_have_member_of(self):
        """Activities with bcCategoryIds should have analyte rows with member_of set."""
        # Vital Signs and Temperature, Chemistry, Urinalysis reference BCCategories
        category_act_ids = {"vital-signs-and-temperature", "chemistry", "uninalysis"}
        obs_by_id = {r["obsdef_id"]: r for r in self.obs_rows}
        for act in self.act_rows:
            if act["id"] in category_act_ids:
                obsdef_id = act["result_obsdef_id"]
                self.assertIn(obsdef_id, obs_by_id,
                              f"No obs row for {act['id']}")
                obs_row = obs_by_id[obsdef_id]
                self.assertTrue(
                    obs_row["member_of"],
                    f"Category activity {act['id']} obs row should have member_of set",
                )

    def test_panel_datatype_is_blank(self):
        for r in self.obs_rows:
            if r["kind"] == "panel":
                self.assertEqual(
                    r["datatype"], "",
                    f"Panel {r['obsdef_id']} should have blank datatype",
                )

    def test_4_bccat_panels(self):
        """There are 4 BiomedicalConceptCategories → 4 panel rows."""
        panels = [r for r in self.obs_rows if r["kind"] == "panel"]
        self.assertEqual(len(panels), 4,
                         f"Expected 4 panels, got {len(panels)}: "
                         f"{[p['obsdef_id'] for p in panels]}")

    def test_measurement_activities_have_analyte_rows(self):
        """Each measurement activity should have a corresponding analyte row."""
        obs_ids = {r["obsdef_id"] for r in self.obs_rows}
        for r in self.act_rows:
            if r["archetype"] == "measurement":
                self.assertIn(
                    r["result_obsdef_id"], obs_ids,
                    f"Activity {r['id']} result_obsdef_id {r['result_obsdef_id']!r} "
                    f"not in observation catalog",
                )

    # --- Idempotency ---

    def test_activity_catalog_idempotent(self):
        """Running extraction twice produces identical results."""
        rows1 = usdm_catalogs.extract_activity_catalog(_USDM_PATH)
        rows2 = usdm_catalogs.extract_activity_catalog(_USDM_PATH)
        self.assertEqual(rows1, rows2, "Activity catalog extraction is not idempotent")

    def test_observation_catalog_idempotent(self):
        """Running extraction twice produces identical results."""
        rows1 = usdm_catalogs.extract_observation_catalog(_USDM_PATH)
        rows2 = usdm_catalogs.extract_observation_catalog(_USDM_PATH)
        self.assertEqual(rows1, rows2,
                         "Observation catalog extraction is not idempotent")

    def test_csv_write_idempotent(self):
        """Writing the same rows twice produces byte-identical files."""
        act_rows = usdm_catalogs.extract_activity_catalog(_USDM_PATH)
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".csv", delete=False
        ) as tmp1, tempfile.NamedTemporaryFile(
            mode="r", suffix=".csv", delete=False
        ) as tmp2:
            path1, path2 = tmp1.name, tmp2.name
        usdm_catalogs.write_activity_catalog(act_rows, path1)
        usdm_catalogs.write_activity_catalog(act_rows, path2)
        with open(path1, "rb") as f1, open(path2, "rb") as f2:
            self.assertEqual(f1.read(), f2.read(),
                             "CSV write is not idempotent")


if __name__ == "__main__":
    unittest.main()
