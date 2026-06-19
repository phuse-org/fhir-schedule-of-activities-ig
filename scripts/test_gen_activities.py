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


import tempfile, os


class GenerateMeasurementsFileTests(unittest.TestCase):
    CSV = (
        "id,title,description,oidsys,oid,loinc,loinc_display,unit,obsdef_id\n"
        "H2Q-MC-LZZT-Vital-Signs-WEIGHT,Weight,Planned Activity [Weight],"
        "ItemDef,I.WEIGHT,29463-7,Body weight,kg,"
        "H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs\n"
    )

    def _run(self):
        d = tempfile.mkdtemp()
        csv_p = os.path.join(d, "m.csv")
        out_p = os.path.join(d, "out.fsh")
        with open(csv_p, "w") as f:
            f.write(self.CSV)
        gen.generate_measurements(csv_p, out_p)
        with open(out_p) as f:
            return out_p, csv_p, f.read()

    def test_has_header_and_both_resources(self):
        _, _, text = self._run()
        self.assertTrue(text.startswith("// DO NOT EDIT"))
        self.assertIn("Instance: H2Q-MC-LZZT-Vital-Signs-WEIGHT\n", text)
        self.assertIn("Instance: H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs\n", text)

    def test_idempotent(self):
        out_p, csv_p, first = self._run()
        gen.generate_measurements(csv_p, out_p)
        with open(out_p) as f:
            self.assertEqual(first, f.read())


class RenderInstrumentActionTests(unittest.TestCase):
    def test_renders_instrument_action_insert(self):
        row = {
            "id": "TTS-ACC",
            "title": "TTS Acceptability Survey",
            "visit_id": "H2Q-MC-LZZT-Study-Visit-13",
            "questionnaire_canonical":
                "H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey",
            "participant": "patient",
            "score_obsdef_id": "",
        }
        out = gen.render_instrument_action(row)
        self.assertIn(
            "insert InstrumentAction("
            "H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey, "
            "[[TTS Acceptability Survey]], #patient)",
            out)


if __name__ == "__main__":
    unittest.main()
