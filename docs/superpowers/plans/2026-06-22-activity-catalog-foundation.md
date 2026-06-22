# Activity Catalog Foundation (Pipeline Phase A) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the validated catalog foundation for the protocol-driven pipeline — the `PanelObservation` RuleSet proven on a real lab panel, the three catalog CSV schemas with existing data migrated in, and a stdlib `catalog.py` loader + validator with unit tests.

**Architecture:** Additive and non-breaking. The current generator and its two CSVs keep working untouched; this plan adds the new catalog format (`activity-catalog.csv`, `observation-catalog.csv`, `condition-catalog.csv`), a Python validator that guards their integrity, and a `PanelObservation` FSH RuleSet demonstrated by a hand-authored Hematology (CBC) panel using `ObservationDefinition.hasMember`. Phase C later switches the generator onto these catalogs.

**Tech Stack:** FHIR Shorthand / SUSHI 3.20.0, FHIR R6 `6.0.0-ballot3`, Python 3.12 (stdlib only; tests via `python3 scripts/test_catalog.py`).

## Global Constraints

- FHIR R6 `6.0.0-ballot3`; verify elements against `hl7.fhir.r6.core#6.0.0-ballot3`.
- `ObservationDefinition.hasMember` is `Reference(ObservationDefinition | Questionnaire)`; it models a panel/battery grouping its members.
- `observationResultRequirement` (not `observationRequirement`) is the produced-results element; a lab activity references **one panel ObsDef** that groups analytes via `hasMember`.
- Python: **stdlib only**, no third-party deps; tests run with `python3 scripts/test_catalog.py`.
- Additive only: do **not** modify or delete `measurement-activities.csv`, `instrument-activities.csv`, `gen-activities.py`, or generated FSH. The existing generator must keep working.
- Catalog CSV schemas (verbatim headers):
  - `activity-catalog.csv`: `id,oid,oidsys,title,archetype,code_system,code,code_display,unit,result_obsdef_id,questionnaire_id,default_condition`
  - `observation-catalog.csv`: `obsdef_id,kind,member_of,code,code_display,unit,datatype`
  - `condition-catalog.csv`: `condition_id,language,expression,description`
- `archetype` ∈ {`measurement`,`instrument`}; observation `kind` ∈ {`analyte`,`panel`}.
- Fast checks: `sushi .` (expect `0 Errors`); `python3 scripts/test_catalog.py` (expect OK).
- Aliases `LOINC`, `UCUM`, `SCT` are already defined project-wide. UCUM codes with special chars are quoted in RuleSets: `UCUM#"{unit}"`.

---

## File Structure

- `input/fsh/SoA-RuleSets.fsh` *(modify)* — add the `PanelObservation` RuleSet.
- `input/fsh/labs/Hematology-Panel.fsh` *(new)* — panel ObsDef + 3 analyte ObsDefs (real CBC subset), demonstrating `hasMember`.
- `input/data/activity-catalog.csv` *(new)* — all migrated activities + Hematology.
- `input/data/observation-catalog.csv` *(new)* — analytes + the Hematology panel.
- `input/data/condition-catalog.csv` *(new)* — one sample applicability condition.
- `scripts/catalog.py` *(new)* — CSV loader + validators + CLI.
- `scripts/test_catalog.py` *(new)* — unit + integration tests.
- `input/pagecontent/developer.md` *(modify)* — document the catalogs + validator.

---

### Task 1: `PanelObservation` RuleSet + Hematology (CBC) panel demonstrating `hasMember`

**Files:**
- Modify: `input/fsh/SoA-RuleSets.fsh`
- Create: `input/fsh/labs/Hematology-Panel.fsh`

**Interfaces:**
- Produces: `RuleSet: PanelObservation(loinc, lname)` (sets `status` + panel `code`); a panel ObservationDefinition `H2Q-MC-LZZT-Hematology-Panel-Obs` with `hasMember` → three analyte ObsDefs `H2Q-MC-LZZT-Hematology-WBC-Obs`, `-HGB-Obs`, `-PLT-Obs`.

- [ ] **Step 1: Add the `PanelObservation` RuleSet**

Append to `input/fsh/SoA-RuleSets.fsh`:

```fsh

// Panel / battery ObservationDefinition (groups analytes via hasMember).
RuleSet: PanelObservation(loinc, lname)
* status = #active
* code = LOINC#{loinc} "{lname}"
```

- [ ] **Step 2: Author the Hematology panel + analytes**

Create `input/fsh/labs/Hematology-Panel.fsh`:

```fsh
// Hematology (CBC) panel — demonstrates ObservationDefinition.hasMember.
// Analytes are a representative subset; more are added during catalog population.

Instance: H2Q-MC-LZZT-Hematology-WBC-Obs
InstanceOf: ObservationDefinition
Usage: #definition
Title: "Leukocytes (WBC) - Observation"
Description: "White blood cell count, an analyte of the Hematology panel."
* insert VitalSignObservation(6690-2, [[Leukocytes]], 10*3/uL)

Instance: H2Q-MC-LZZT-Hematology-HGB-Obs
InstanceOf: ObservationDefinition
Usage: #definition
Title: "Hemoglobin - Observation"
Description: "Hemoglobin mass concentration, an analyte of the Hematology panel."
* insert VitalSignObservation(718-7, [[Hemoglobin]], g/dL)

Instance: H2Q-MC-LZZT-Hematology-PLT-Obs
InstanceOf: ObservationDefinition
Usage: #definition
Title: "Platelets - Observation"
Description: "Platelet count, an analyte of the Hematology panel."
* insert VitalSignObservation(777-3, [[Platelets]], 10*3/uL)

Instance: H2Q-MC-LZZT-Hematology-Panel-Obs
InstanceOf: ObservationDefinition
Usage: #definition
Title: "Hematology (CBC) panel - Observation"
Description: "Complete blood count panel; groups its analyte ObservationDefinitions."
* insert PanelObservation(58410-2, [[CBC panel]])
* hasMember[+] = Reference(H2Q-MC-LZZT-Hematology-WBC-Obs)
* hasMember[+] = Reference(H2Q-MC-LZZT-Hematology-HGB-Obs)
* hasMember[+] = Reference(H2Q-MC-LZZT-Hematology-PLT-Obs)
```

- [ ] **Step 3: Build and verify the panel serializes `hasMember`**

Run: `sushi . 2>&1 | grep -E "Error" | tail -1`
Expected: `0 Errors`.

Run: `python3 -c "import json;d=json.load(open('fsh-generated/resources/ObservationDefinition-H2Q-MC-LZZT-Hematology-Panel-Obs.json'));print(d['code']['coding'][0]['code'], len(d['hasMember']), [m['reference'] for m in d['hasMember']])"`
Expected: `58410-2 3 ['ObservationDefinition/H2Q-MC-LZZT-Hematology-WBC-Obs', 'ObservationDefinition/H2Q-MC-LZZT-Hematology-HGB-Obs', 'ObservationDefinition/H2Q-MC-LZZT-Hematology-PLT-Obs']`

Run: `python3 -c "import json;d=json.load(open('fsh-generated/resources/ObservationDefinition-H2Q-MC-LZZT-Hematology-WBC-Obs.json'));print(d['permittedUnit'][0]['code'])"`
Expected: `10*3/uL`

- [ ] **Step 4: Commit**

```bash
git add input/fsh/SoA-RuleSets.fsh input/fsh/labs/Hematology-Panel.fsh
git commit -m "feat: PanelObservation RuleSet + Hematology CBC panel via hasMember"
```

---

### Task 2: `catalog.py` — CSV loader + activity validation

**Files:**
- Create: `scripts/catalog.py`
- Test: `scripts/test_catalog.py`

**Interfaces:**
- Produces (consumed by Task 3, 4):
  - `load_csv(path) -> list[dict]`
  - `ARCHETYPES = {"measurement", "instrument"}`
  - `validate_activities(activities, obs_ids: set, cond_ids: set) -> list[str]` — returns a list of human-readable error strings ([] = valid).

- [ ] **Step 1: Write the failing test**

Create `scripts/test_catalog.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 scripts/test_catalog.py`
Expected: FAIL (`AttributeError: module 'catalog' has no attribute 'validate_activities'`).

- [ ] **Step 3: Write the implementation**

Create `scripts/catalog.py`:

```python
#!/usr/bin/env python3
"""Loader + validator for the protocol-pipeline catalogs (stdlib only)."""
import csv
import sys
import pathlib

ARCHETYPES = {"measurement", "instrument"}
OBS_KINDS = {"analyte", "panel"}


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def validate_activities(activities, obs_ids, cond_ids):
    errors = []
    seen = set()
    for a in activities:
        aid = a["id"]
        if aid in seen:
            errors.append(f"duplicate activity id: {aid}")
        seen.add(aid)
        if a["archetype"] not in ARCHETYPES:
            errors.append(f"{aid}: bad archetype {a['archetype']!r}")
        if a["archetype"] == "measurement":
            if not a["result_obsdef_id"]:
                errors.append(f"{aid}: measurement missing result_obsdef_id")
            elif a["result_obsdef_id"] not in obs_ids:
                errors.append(
                    f"{aid}: result_obsdef_id {a['result_obsdef_id']} "
                    f"not in observation catalog")
        if a["archetype"] == "instrument" and not a["questionnaire_id"]:
            errors.append(f"{aid}: instrument missing questionnaire_id")
        if a.get("default_condition") and a["default_condition"] not in cond_ids:
            errors.append(
                f"{aid}: default_condition {a['default_condition']} "
                f"not in condition catalog")
    return errors
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 scripts/test_catalog.py`
Expected: PASS (7 tests OK).

- [ ] **Step 5: Commit**

```bash
git add scripts/catalog.py scripts/test_catalog.py
git commit -m "feat: catalog loader + activity validation"
```

---

### Task 3: `catalog.py` — observation + condition validation, composed validator

**Files:**
- Modify: `scripts/catalog.py`
- Test: `scripts/test_catalog.py`

**Interfaces:**
- Consumes: `validate_activities` (Task 2).
- Produces:
  - `validate_observations(observations) -> list[str]`
  - `validate_conditions(conditions) -> list[str]`
  - `validate_catalogs(activities, observations, conditions) -> list[str]` — composes all three (derives `obs_ids`/`cond_ids` internally).

- [ ] **Step 1: Add the failing tests**

Append to `scripts/test_catalog.py`:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 scripts/test_catalog.py`
Expected: FAIL (`no attribute 'validate_observations'`).

- [ ] **Step 3: Implement**

Add to `scripts/catalog.py` (after `validate_activities`), then add the CLI block:

```python
def validate_observations(observations):
    errors = []
    seen = set()
    panel_ids = {o["obsdef_id"] for o in observations if o["kind"] == "panel"}
    for o in observations:
        oid = o["obsdef_id"]
        if oid in seen:
            errors.append(f"duplicate obsdef_id: {oid}")
        seen.add(oid)
        if o["kind"] not in OBS_KINDS:
            errors.append(f"{oid}: bad kind {o['kind']!r}")
        if o["kind"] == "panel" and not o["code"]:
            errors.append(f"{oid}: panel missing code")
        if o.get("member_of") and o["member_of"] not in panel_ids:
            errors.append(f"{oid}: member_of {o['member_of']} is not a panel")
    return errors


def validate_conditions(conditions):
    errors = []
    seen = set()
    for c in conditions:
        cid = c["condition_id"]
        if cid in seen:
            errors.append(f"duplicate condition_id: {cid}")
        seen.add(cid)
        if not c["language"] or not c["expression"]:
            errors.append(f"{cid}: missing language or expression")
    return errors


def validate_catalogs(activities, observations, conditions):
    obs_ids = {o["obsdef_id"] for o in observations}
    cond_ids = {c["condition_id"] for c in conditions}
    return (validate_activities(activities, obs_ids, cond_ids)
            + validate_observations(observations)
            + validate_conditions(conditions))


def main():
    base = pathlib.Path(__file__).resolve().parent.parent / "input/data"
    errs = validate_catalogs(
        load_csv(base / "activity-catalog.csv"),
        load_csv(base / "observation-catalog.csv"),
        load_csv(base / "condition-catalog.csv"),
    )
    for e in errs:
        print("ERROR:", e)
    print(f"{len(errs)} error(s).")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run to verify it passes**

Run: `python3 scripts/test_catalog.py`
Expected: PASS (all tests OK).

- [ ] **Step 5: Commit**

```bash
git add scripts/catalog.py scripts/test_catalog.py
git commit -m "feat: observation + condition validation and composed validate_catalogs"
```

---

### Task 4: Author the three catalog CSVs (migrate existing data + Hematology + sample condition)

**Files:**
- Create: `input/data/activity-catalog.csv`
- Create: `input/data/observation-catalog.csv`
- Create: `input/data/condition-catalog.csv`
- Modify: `scripts/test_catalog.py`

**Interfaces:**
- Consumes: `load_csv`, `validate_catalogs` (Tasks 2–3).

These carry today's Vital Signs measurements + Temperature + the TTS instrument + the Hematology panel from Task 1 + one sample condition. They are **data for the future generator (Phase C)**; nothing compiles them yet, so ids may match the hand-authored FSH without collision.

- [ ] **Step 1: Create `activity-catalog.csv`**

Create `input/data/activity-catalog.csv`:

```csv
id,oid,oidsys,title,archetype,code_system,code,code_display,unit,result_obsdef_id,questionnaire_id,default_condition
H2Q-MC-LZZT-Vital-Signs-HEIGHT,I.HEIGHT,ItemDef,Height,measurement,LOINC,8302-2,Body height,cm,H2Q-MC-LZZT-Vital-Signs-HEIGHT-Obs,,
H2Q-MC-LZZT-Vital-Signs-WEIGHT,I.WEIGHT,ItemDef,Weight,measurement,LOINC,29463-7,Body weight,kg,H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs,,
H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE,I.PULSE_SUPINE,ItemDef,Supine Pulse,measurement,LOINC,8867-4,Heart rate,/min,H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE-Obs,,
H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING,I.PULSE_STANDING,ItemDef,Standing Pulse,measurement,LOINC,8867-4,Heart rate,/min,H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING-Obs,,
H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE,I.SYSBP_SUPINE,ItemDef,Supine Systolic BP,measurement,LOINC,8461-6,Systolic blood pressure--supine,mm[Hg],H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE-Obs,,
H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING,I.SYSBP_STANDING,ItemDef,Standing Systolic BP,measurement,LOINC,8460-8,Systolic blood pressure--standing,mm[Hg],H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING-Obs,,
H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE,I.DIABP_SUPINE,ItemDef,Supine Diastolic BP,measurement,LOINC,8453-3,Diastolic blood pressure--supine,mm[Hg],H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE-Obs,,
H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING,I.DIABP_STANDING,ItemDef,Standing Diastolic BP,measurement,LOINC,8454-1,Diastolic blood pressure--standing,mm[Hg],H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING-Obs,,
H2Q-MC-LZZT-Vitalsigns-Temperature,I.TEMP,ItemDef,Temperature Measurement,measurement,LOINC,8310-5,Body temperature,Cel,Temperature-Observation-LOINC,,
H2Q-MC-LZZT-Laboratory-Hemat,F.LB_HEM,FormDef,Laboratory (Hematology),measurement,LOINC,58410-2,CBC panel - Blood by Automated count,,H2Q-MC-LZZT-Hematology-Panel-Obs,,
H2Q-MC-LZZT-TTS-Acceptability-Survey,F.TTSACC,FormDef,TTS Acceptability Survey,instrument,LOINC,71969-0,Adverse drug reaction assessment,,,H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey,
```

- [ ] **Step 2: Create `observation-catalog.csv`**

Create `input/data/observation-catalog.csv`:

```csv
obsdef_id,kind,member_of,code,code_display,unit,datatype
H2Q-MC-LZZT-Vital-Signs-HEIGHT-Obs,analyte,,8302-2,Body height,cm,Quantity
H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs,analyte,,29463-7,Body weight,kg,Quantity
H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE-Obs,analyte,,8867-4,Heart rate,/min,Quantity
H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING-Obs,analyte,,8867-4,Heart rate,/min,Quantity
H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE-Obs,analyte,,8461-6,Systolic blood pressure--supine,mm[Hg],Quantity
H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING-Obs,analyte,,8460-8,Systolic blood pressure--standing,mm[Hg],Quantity
H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE-Obs,analyte,,8453-3,Diastolic blood pressure--supine,mm[Hg],Quantity
H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING-Obs,analyte,,8454-1,Diastolic blood pressure--standing,mm[Hg],Quantity
Temperature-Observation-LOINC,analyte,,8310-5,Body temperature,Cel,Quantity
H2Q-MC-LZZT-Hematology-Panel-Obs,panel,,58410-2,CBC panel - Blood by Automated count,,
H2Q-MC-LZZT-Hematology-WBC-Obs,analyte,H2Q-MC-LZZT-Hematology-Panel-Obs,6690-2,Leukocytes,10*3/uL,Quantity
H2Q-MC-LZZT-Hematology-HGB-Obs,analyte,H2Q-MC-LZZT-Hematology-Panel-Obs,718-7,Hemoglobin,g/dL,Quantity
H2Q-MC-LZZT-Hematology-PLT-Obs,analyte,H2Q-MC-LZZT-Hematology-Panel-Obs,777-3,Platelets,10*3/uL,Quantity
```

- [ ] **Step 3: Create `condition-catalog.csv`**

Create `input/data/condition-catalog.csv`:

```csv
condition_id,language,expression,description
type1-diabetes,text/fhirpath,Condition.where(code.coding.where(system='http://snomed.info/sct' and code='46635009').exists()).exists(),Type I diabetics only
```

- [ ] **Step 4: Add the integration test over the real files**

Append to `scripts/test_catalog.py`:

```python
class RealCatalogIntegrationTests(unittest.TestCase):
    def test_authored_catalogs_validate_clean(self):
        base = pathlib.Path(__file__).resolve().parent.parent / "input/data"
        errs = catalog.validate_catalogs(
            catalog.load_csv(base / "activity-catalog.csv"),
            catalog.load_csv(base / "observation-catalog.csv"),
            catalog.load_csv(base / "condition-catalog.csv"),
        )
        self.assertEqual(errs, [], f"catalog validation errors: {errs}")
```

- [ ] **Step 5: Run the validator + tests**

Run: `python3 scripts/catalog.py`
Expected: `0 error(s).` and exit 0.

Run: `python3 scripts/test_catalog.py`
Expected: PASS (all unit + integration tests OK).

- [ ] **Step 6: Confirm the IG still builds (catalogs are data, not compiled)**

Run: `sushi . 2>&1 | grep -E "Error" | tail -1`
Expected: `0 Errors`.

- [ ] **Step 7: Commit**

```bash
git add input/data/activity-catalog.csv input/data/observation-catalog.csv input/data/condition-catalog.csv scripts/test_catalog.py
git commit -m "feat: author activity/observation/condition catalogs (migrated + Hematology)"
```

---

### Task 5: Document the catalogs + final verification

**Files:**
- Modify: `input/pagecontent/developer.md`

- [ ] **Step 1: Document the catalogs and validator**

Append to `input/pagecontent/developer.md`:

```markdown
## Activity catalogs (pipeline)

The protocol-driven pipeline is fed by three editable catalogs under `input/data/`:

- `activity-catalog.csv` — one row per study activity (archetype, codes, result/questionnaire links).
- `observation-catalog.csv` — result ObservationDefinitions; `kind=panel` rows group
  `kind=analyte` rows via `member_of` (rendered as `ObservationDefinition.hasMember`).
- `condition-catalog.csv` — reusable applicability expressions for conditional scheduling.

Validate them before regenerating:

    python3 scripts/catalog.py        # exits non-zero on any error
    python3 scripts/test_catalog.py   # unit + integration tests
```

- [ ] **Step 2: Final verification**

Run: `python3 scripts/catalog.py && python3 scripts/test_catalog.py && sushi . 2>&1 | tail -3`
Expected: `0 error(s).`, tests OK, and `0 Errors` from SUSHI.

- [ ] **Step 3: Commit**

```bash
git add input/pagecontent/developer.md
git commit -m "docs: document the pipeline activity catalogs and validator"
```

---

## Self-Review notes (spec coverage)

- `PanelObservation` RuleSet + `hasMember` panel modeling → Task 1 (proven on real CBC panel).
- `observationResultRequirement` correctness / panel-not-flat-list → demonstrated by the panel ObsDef; activity→panel link recorded in catalog (Task 4), wired by Phase C.
- Three editable sources (activity/observation/condition catalogs) → Tasks 2–4.
- Catalog integrity (archetype enum, dangling result/obsdef/condition refs, panel membership) → validator Tasks 2–3, guarded over real data Task 4.
- Existing data migrated; additive (old CSVs/generator untouched) → Task 4 + Global Constraints.
- Condition catalog schema for conditional scheduling → Task 3–4 (consumed by Phase C generator).

**Out of scope (later phases):** protocol traversal + SoA-matrix bootstrap (Phase B); generating activity resources + visit actions + `action.condition` from the catalogs and retiring stubs (Phase C); `#example→#definition` usage sweep (Phase D); deploy Bundle (Phase E); bulk population of the remaining ~30 activities (repeated catalog edits validated by `catalog.py`).
