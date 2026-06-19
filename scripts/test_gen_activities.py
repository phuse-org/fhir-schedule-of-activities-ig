import unittest
import importlib.util, pathlib

spec = importlib.util.spec_from_file_location(
    "gen", pathlib.Path(__file__).with_name("gen-activities.py"))
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


class RenderMeasurementTests(unittest.TestCase):
    def test_renders_activity_instance_with_insert(self):
        row = {
            "id": "H2Q-MC-LZZT-Vital-Signs-WEIGHT",
            "title": "Weight",
            "description": "Planned Activity [Weight]",
            "oidsys": "ItemDef",
            "oid": "I.WEIGHT",
            "loinc": "29463-7",
            "loinc_display": "Body weight",
            "unit": "kg",
            "obsdef_id": "H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs",
        }
        out = gen.render_measurement(row)
        self.assertIn("Instance: H2Q-MC-LZZT-Vital-Signs-WEIGHT", out)
        self.assertIn("InstanceOf: StudyActivitySoa", out)
        self.assertIn(
            "insert VitalSignActivity(ItemDef, I.WEIGHT, 29463-7, [[Body weight]])",
            out)
        self.assertIn(
            "observationResultRequirement = "
            '"ObservationDefinition/H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs"',
            out)


class RenderMeasurementObsTests(unittest.TestCase):
    def test_renders_obsdef_with_insert(self):
        row = {
            "obsdef_id": "H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs",
            "title": "Weight",
            "loinc": "29463-7",
            "loinc_display": "Body weight",
            "unit": "kg",
        }
        out = gen.render_measurement_obs(row)
        self.assertIn(
            "Instance: H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs", out)
        self.assertIn("InstanceOf: ObservationDefinition", out)
        self.assertIn(
            "insert VitalSignObservation(29463-7, [[Body weight]], kg)", out)


if __name__ == "__main__":
    unittest.main()
