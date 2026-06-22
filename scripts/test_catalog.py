import unittest
import importlib.util, pathlib

spec = importlib.util.spec_from_file_location(
    "catalog", pathlib.Path(__file__).with_name("catalog.py"))
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class ValidateActivitiesTests(unittest.TestCase):
    def _row(self, **kw):
        base = {"id": "A", "archetype": "measurement", "result_obsdef_id": "O",
                "questionnaire_id": "", "default_condition": ""}
        base.update(kw)
        return base

    def test_valid_measurement_passes(self):
        rows = [self._row()]
        self.assertEqual(catalog.validate_activities(rows, {"O"}, set()), [])

    def test_bad_archetype_flagged(self):
        rows = [self._row(archetype="lab")]
        errs = catalog.validate_activities(rows, {"O"}, set())
        self.assertTrue(any("archetype" in e for e in errs))

    def test_measurement_missing_result_obsdef_flagged(self):
        rows = [self._row(result_obsdef_id="")]
        errs = catalog.validate_activities(rows, set(), set())
        self.assertTrue(any("result_obsdef_id" in e for e in errs))

    def test_measurement_dangling_result_obsdef_flagged(self):
        rows = [self._row(result_obsdef_id="MISSING")]
        errs = catalog.validate_activities(rows, {"O"}, set())
        self.assertTrue(any("MISSING" in e for e in errs))

    def test_instrument_missing_questionnaire_flagged(self):
        rows = [self._row(archetype="instrument", result_obsdef_id="",
                          questionnaire_id="")]
        errs = catalog.validate_activities(rows, set(), set())
        self.assertTrue(any("questionnaire_id" in e for e in errs))

    def test_duplicate_id_flagged(self):
        rows = [self._row(), self._row()]
        errs = catalog.validate_activities(rows, {"O"}, set())
        self.assertTrue(any("duplicate" in e for e in errs))

    def test_dangling_default_condition_flagged(self):
        rows = [self._row(default_condition="C")]
        errs = catalog.validate_activities(rows, {"O"}, set())
        self.assertTrue(any("default_condition" in e for e in errs))


class ValidateObservationsTests(unittest.TestCase):
    def test_valid_panel_and_analyte_pass(self):
        rows = [
            {"obsdef_id": "P", "kind": "panel", "member_of": "",
             "code": "58410-2", "unit": "", "datatype": ""},
            {"obsdef_id": "A", "kind": "analyte", "member_of": "P",
             "code": "718-7", "unit": "g/dL", "datatype": "Quantity"},
        ]
        self.assertEqual(catalog.validate_observations(rows), [])

    def test_bad_kind_flagged(self):
        rows = [{"obsdef_id": "X", "kind": "blob", "member_of": "",
                 "code": "1", "unit": "", "datatype": ""}]
        self.assertTrue(any("kind" in e for e in catalog.validate_observations(rows)))

    def test_panel_missing_code_flagged(self):
        rows = [{"obsdef_id": "P", "kind": "panel", "member_of": "",
                 "code": "", "unit": "", "datatype": ""}]
        self.assertTrue(any("code" in e for e in catalog.validate_observations(rows)))

    def test_member_of_non_panel_flagged(self):
        rows = [{"obsdef_id": "A", "kind": "analyte", "member_of": "NOPE",
                 "code": "1", "unit": "x", "datatype": "Quantity"}]
        self.assertTrue(any("member_of" in e for e in catalog.validate_observations(rows)))


class ValidateConditionsTests(unittest.TestCase):
    def test_valid_condition_passes(self):
        rows = [{"condition_id": "c1", "language": "text/fhirpath",
                 "expression": "true", "description": "d"}]
        self.assertEqual(catalog.validate_conditions(rows), [])

    def test_missing_expression_flagged(self):
        rows = [{"condition_id": "c1", "language": "text/fhirpath",
                 "expression": "", "description": "d"}]
        self.assertTrue(any("expression" in e for e in catalog.validate_conditions(rows)))


class ValidateCatalogsTests(unittest.TestCase):
    def test_composes_and_resolves_cross_refs(self):
        activities = [{"id": "A", "archetype": "measurement",
                       "result_obsdef_id": "P", "questionnaire_id": "",
                       "default_condition": "c1"}]
        observations = [{"obsdef_id": "P", "kind": "panel", "member_of": "",
                         "code": "58410-2", "unit": "", "datatype": ""}]
        conditions = [{"condition_id": "c1", "language": "text/fhirpath",
                       "expression": "true", "description": "d"}]
        self.assertEqual(
            catalog.validate_catalogs(activities, observations, conditions), [])


if __name__ == "__main__":
    unittest.main()
