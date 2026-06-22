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


if __name__ == "__main__":
    unittest.main()
