# ActivityDefinition Templates & Acceleration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build out the Vital Signs ActivityDefinition family to a gold-standard, profile-conforming template, add one PRO/instrument exemplar attached via `action.definitionCanonical → Questionnaire`, and stand up archetype-aware acceleration helpers (FSH RuleSets + a CSV-driven generator).

**Architecture:** Two activity archetypes. **Measurements** (Vital Signs) are `ActivityDefinition` instances conforming to `StudyActivitySoa`, carrying coded `code`/`kind`/`intent`/`participant` and an `observationResultRequirement` → a richly-specified `ObservationDefinition`; these are emitted by a CSV-driven generator using a shared `VitalSignActivity` RuleSet (single source of truth, compiled from `input/fsh/generated/`). **Instruments** (PROs) are core-R6 `Questionnaire` resources referenced directly from the visit `PlanDefinition.action.definitionCanonical` — no ActivityDefinition wrapper — with scored results via SDC extraction conventions.

**Tech Stack:** FHIR Shorthand (FSH) / SUSHI v3.20.0, FHIR R6 `6.0.0-ballot3`, Python 3.12 (stdlib only) for the generator and its tests.

## Global Constraints

- FHIR version is **R6 `6.0.0-ballot3`**; verify every element/binding against `hl7.fhir.r6.core#6.0.0-ballot3`.
- `ObservationDefinition.identifier` is **0..1**; `Identifier` has **no `.text`** sub-element (use `.type.text`).
- `ActivityDefinition.kind` required binding = *request-resource-types* (`#ServiceRequest`, `#Task`, … — **not** `Observation`). `intent` = *request-intent* (use `#plan`).
- Measurement activities use **`observationResultRequirement` only**; never `observationRequirement` (that is for prerequisite inputs).
- Instruments do **not** conform to `StudyActivitySoa` and have **no** ActivityDefinition; attach via `action.definitionCanonical`.
- No hard `hl7.fhir.uv.sdc` dependency (no R6 build exists). SDC extension URLs are used by convention; resulting *unresolved-extension* messages are **warnings**, tolerated. The build must report **0 errors**.
- Generator: Python 3.12 **stdlib only**; output files carry a `DO NOT EDIT` header and are **idempotent** (unchanged CSV ⇒ byte-identical output). Hand-authored and generated FSH never share an instance id.
- Fast test loop is `sushi .` (run from repo root). "Green" = `0 Errors`.
- Existing alias `SCT = http://snomed.info/sct` and `UCUM = http://unitsofmeasure.org` are project-global and may be reused.

---

## File Structure

- `input/fsh/SoA-RuleSets.fsh` *(new)* — `LOINC` alias + the four archetype RuleSets.
- `input/fsh/VitalSigns-Observation.fsh` *(fix)* — restore validity (currently breaks the build).
- `input/fsh/H2Q-MC-LZZT-StudyActivities.fsh` *(modify)* — remove the 8 measurement stubs + the TEMP duplicate stub + the TTS-Acceptability-Survey AD.
- `input/fsh/H2Q-MC-LZZT-VitalSigns-Temperature-1.fsh` *(modify)* — canonical Temperature, conformed + de-duplicated.
- `input/fsh/H2Q-MC-LZZT-StudyActivities.fsh` Temperature PD *(modify)* — repoint to canonical Temperature id.
- `input/data/measurement-activities.csv` *(new)* — 8 Vital Signs rows.
- `input/data/instrument-activities.csv` *(new)* — 1 exemplar row.
- `scripts/gen-activities.py` *(new)* — CSV → FSH generator.
- `scripts/test_gen_activities.py` *(new)* — `unittest` tests for the generator.
- `input/fsh/generated/Measurement-Activities.gen.fsh` *(generated, committed)* — the 8 ADs + 8 ObsDefs.
- `input/fsh/questionnaires/Questionnaire-TTS-Acceptability-Survey.fsh` *(new)* — the PRO exemplar Questionnaire (+ scored ObsDef).
- `input/fsh/H2Q-MC-LZZT-Visit-13.fsh`, `input/fsh/H2Q-MC-LZZT-ET-14.fsh` *(modify)* — attach the Questionnaire via `definitionCanonical`.
- `input/pagecontent/developer.md` *(modify)* — document the generator pre-build step.

---

## Phase 0 — Green baseline & foundations

### Task 1: Restore a green baseline (fix `VitalSigns-Observation.fsh`)

**Files:**
- Modify: `input/fsh/VitalSigns-Observation.fsh`

**Interfaces:**
- Produces: a valid `ObservationDefinition` instance `VitalSigns-Observation` (still referenced by the canonical Temperature AD until Task 7).

The file currently sets six `identifier[+]` entries each with `.text`, but `ObservationDefinition.identifier` is `0..1` and `Identifier` has no `.text` — 21 build errors. Collapse to a single valid base ObsDef. The per-measurement pulse/BP ObsDefs are created later by the generator (Task 6), so this file becomes a minimal valid placeholder.

- [ ] **Step 1: Confirm the failing baseline**

Run: `sushi . 2>&1 | tail -3`
Expected: shows `21 Errors` and "went belly up".

- [ ] **Step 2: Replace the file with a valid minimal ObsDef**

Replace the entire contents of `input/fsh/VitalSigns-Observation.fsh` with:

```fsh
Instance: VitalSigns-Observation
InstanceOf: ObservationDefinition
Description: "Planned Observation [Vital Signs] - generic base"
Usage: #example
Title: "VitalSigns-Observation"
* status = #active
* code = SCT#118227000 "Vital signs measurement (procedure)"
```

- [ ] **Step 3: Run the build to verify green**

Run: `sushi . 2>&1 | tail -3`
Expected: `0 Errors` (warnings allowed).

- [ ] **Step 4: Commit**

```bash
git add input/fsh/VitalSigns-Observation.fsh
git commit -m "fix: restore valid VitalSigns-Observation ObservationDefinition (green baseline)"
```

---

### Task 2: Add the `LOINC` alias and archetype RuleSets

**Files:**
- Create: `input/fsh/SoA-RuleSets.fsh`

**Interfaces:**
- Produces (consumed by Tasks 6, 7, 10):
  - `RuleSet: VitalSignActivity(oidsys, oid, loinc, lname)` — sets `status/kind/intent/participant/identifier/code` on a measurement `ActivityDefinition`.
  - `RuleSet: VitalSignObservation(loinc, lname, unit)` — sets `status/code/permittedDataType/permittedUnit/preferredReportName` on a measurement `ObservationDefinition`.
  - `RuleSet: InstrumentAction(qcanonical, title, ptype)` — appends a Questionnaire-attached action to a PlanDefinition.
  - `RuleSet: ScoredInstrumentObservation(loinc, lname)` — a scored-result `ObservationDefinition`.
  - `Alias: LOINC = http://loinc.org`.

- [ ] **Step 1: Create the RuleSets file**

Create `input/fsh/SoA-RuleSets.fsh`:

```fsh
// Archetype helper RuleSets and aliases for Schedule-of-Activities resources.
Alias: LOINC = http://loinc.org

// --- Archetype 1: quantitative measurement -------------------------------

// ActivityDefinition for a vital-sign / simple measurement.
// oidsys: ODM def type (ItemDef|FormDef); oid: ODM OID; loinc: LOINC code; lname: LOINC display.
RuleSet: VitalSignActivity(oidsys, oid, loinc, lname)
* status = #active
* kind = #ServiceRequest
* intent = #plan
* participant[+].type = #practitioner
* identifier[+].value = "{oid}"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/{oidsys}#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* code.coding[+] = LOINC#{loinc} "{lname}"

// ObservationDefinition describing the result a measurement must produce.
RuleSet: VitalSignObservation(loinc, lname, unit)
* status = #active
* code = LOINC#{loinc} "{lname}"
* permittedDataType = #Quantity
* permittedUnit = UCUM#"{unit}"
* preferredReportName = "{lname}"

// --- Archetype 2: PRO / clinician instrument -----------------------------

// Appends a direct Questionnaire attachment to a PlanDefinition action.
// qcanonical: Questionnaire instance id; title: action title; ptype: #patient|#practitioner.
RuleSet: InstrumentAction(qcanonical, title, ptype)
* action[+].title = "{title}"
* action[=].definitionCanonical = Canonical({qcanonical})
* action[=].participant[+].type = {ptype}

// Optional scored-result ObservationDefinition (SDC extraction target).
RuleSet: ScoredInstrumentObservation(loinc, lname)
* status = #active
* code = LOINC#{loinc} "{lname}"
* permittedDataType = #integer
* preferredReportName = "{lname}"
```

- [ ] **Step 2: Verify the build stays green (unused RuleSets are fine)**

Run: `sushi . 2>&1 | tail -3`
Expected: `0 Errors`.

- [ ] **Step 3: Commit**

```bash
git add input/fsh/SoA-RuleSets.fsh
git commit -m "feat: add LOINC alias and archetype RuleSets for SoA activities"
```

---

## Phase 1 — Measurement generator & Vital Signs family

### Task 3: Generator — parse CSV and emit a measurement ActivityDefinition block

**Files:**
- Create: `scripts/gen-activities.py`
- Test: `scripts/test_gen_activities.py`

**Interfaces:**
- Produces (consumed by Tasks 4–6, 10):
  - `render_measurement(row: dict) -> str` — returns the FSH for one measurement AD (Instance + `insert VitalSignActivity`).
  - Row keys: `id, title, description, oidsys, oid, loinc, loinc_display, unit, obsdef_id`.

- [ ] **Step 1: Write the failing test**

Create `scripts/test_gen_activities.py`:

```python
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 scripts/test_gen_activities.py`
Expected: FAIL (`AttributeError: module 'gen' has no attribute 'render_measurement'`).

- [ ] **Step 3: Write the minimal implementation**

Create `scripts/gen-activities.py`:

```python
#!/usr/bin/env python3
"""Generate Schedule-of-Activities FSH from CSV definitions.

stdlib only. Emits idempotent, DO-NOT-EDIT FSH for measurement activities
(archetype 1). See docs/superpowers/specs for the design.
"""
import csv
import sys
import pathlib

HEADER = (
    "// DO NOT EDIT — generated by scripts/gen-activities.py\n"
    "// Source: {source}\n\n"
)


def render_measurement(row):
    """FSH for one measurement ActivityDefinition + its result link."""
    return (
        f"Instance: {row['id']}\n"
        f"InstanceOf: StudyActivitySoa\n"
        f"Usage: #example\n"
        f'Title: "{row["title"]}"\n'
        f'Description: "{row["description"]}"\n'
        f"* insert VitalSignActivity({row['oidsys']}, {row['oid']}, "
        f"{row['loinc']}, [[{row['loinc_display']}]])\n"
        f"* observationResultRequirement = "
        f'"ObservationDefinition/{row["obsdef_id"]}"\n'
    )


if __name__ == "__main__":
    sys.exit(0)
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 scripts/test_gen_activities.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/gen-activities.py scripts/test_gen_activities.py
git commit -m "feat: generator renders measurement ActivityDefinition FSH"
```

---

### Task 4: Generator — emit the paired measurement ObservationDefinition

**Files:**
- Modify: `scripts/gen-activities.py`
- Test: `scripts/test_gen_activities.py`

**Interfaces:**
- Produces: `render_measurement_obs(row: dict) -> str` — FSH for the result ObservationDefinition (Instance + `insert VitalSignObservation`).

- [ ] **Step 1: Add the failing test**

Append to `scripts/test_gen_activities.py` inside a new test class:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 scripts/test_gen_activities.py`
Expected: FAIL (`no attribute 'render_measurement_obs'`).

- [ ] **Step 3: Implement**

Add to `scripts/gen-activities.py` (after `render_measurement`):

```python
def render_measurement_obs(row):
    """FSH for the ObservationDefinition a measurement must produce."""
    return (
        f"Instance: {row['obsdef_id']}\n"
        f"InstanceOf: ObservationDefinition\n"
        f"Usage: #example\n"
        f'Title: "{row["title"]} - Observation"\n'
        f'Description: "Result requirement for {row["title"]}"\n'
        f"* insert VitalSignObservation({row['loinc']}, "
        f"[[{row['loinc_display']}]], {row['unit']})\n"
    )
```

- [ ] **Step 4: Run to verify it passes**

Run: `python3 scripts/test_gen_activities.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/gen-activities.py scripts/test_gen_activities.py
git commit -m "feat: generator renders paired measurement ObservationDefinition"
```

---

### Task 5: Generator — file generation, header, idempotency

**Files:**
- Modify: `scripts/gen-activities.py`
- Test: `scripts/test_gen_activities.py`

**Interfaces:**
- Produces: `generate_measurements(csv_path: str, out_path: str) -> None` — reads the CSV, writes the DO-NOT-EDIT FSH file (AD then ObsDef per row). Idempotent.

- [ ] **Step 1: Add the failing test**

Append to `scripts/test_gen_activities.py`:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 scripts/test_gen_activities.py`
Expected: FAIL (`no attribute 'generate_measurements'`).

- [ ] **Step 3: Implement**

Add to `scripts/gen-activities.py`, and replace the `__main__` block:

```python
def generate_measurements(csv_path, out_path):
    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    parts = [HEADER.format(source=pathlib.Path(csv_path).name)]
    for row in rows:
        parts.append(render_measurement(row))
        parts.append("\n")
        parts.append(render_measurement_obs(row))
        parts.append("\n")
    pathlib.Path(out_path).write_text("".join(parts))


def main():
    base = pathlib.Path(__file__).resolve().parent.parent
    generate_measurements(
        base / "input/data/measurement-activities.csv",
        base / "input/fsh/generated/Measurement-Activities.gen.fsh",
    )
    print("Generated measurement activities.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run to verify it passes**

Run: `python3 scripts/test_gen_activities.py`
Expected: PASS (all 4 tests OK).

- [ ] **Step 5: Commit**

```bash
git add scripts/gen-activities.py scripts/test_gen_activities.py
git commit -m "feat: generator writes idempotent measurement FSH file"
```

---

### Task 6: Generate the 8 Vital Signs measurements; remove stubs; verify in SUSHI

**Files:**
- Create: `input/data/measurement-activities.csv`
- Create (generated): `input/fsh/generated/Measurement-Activities.gen.fsh`
- Modify: `input/fsh/H2Q-MC-LZZT-StudyActivities.fsh` (remove 8 stubs)

**Interfaces:**
- Consumes: `VitalSignActivity` / `VitalSignObservation` RuleSets (Task 2); `generate_measurements` (Task 5).
- Produces: 8 `StudyActivitySoa` ADs + 8 ObsDefs compiled into the IG.

Position-specific BP LOINC codes and metric units per the spec's mapping table.

- [ ] **Step 1: Create the CSV**

Create `input/data/measurement-activities.csv`:

```csv
id,title,description,oidsys,oid,loinc,loinc_display,unit,obsdef_id
H2Q-MC-LZZT-Vital-Signs-HEIGHT,Height,Planned Activity [Height],ItemDef,I.HEIGHT,8302-2,Body height,cm,H2Q-MC-LZZT-Vital-Signs-HEIGHT-Obs
H2Q-MC-LZZT-Vital-Signs-WEIGHT,Weight,Planned Activity [Weight],ItemDef,I.WEIGHT,29463-7,Body weight,kg,H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs
H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE,Supine Pulse,Planned Activity [Supine Pulse],ItemDef,I.PULSE_SUPINE,8867-4,Heart rate,/min,H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE-Obs
H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING,Standing Pulse,Planned Activity [Standing Pulse],ItemDef,I.PULSE_STANDING,8867-4,Heart rate,/min,H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING-Obs
H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE,Supine Systolic BP,Planned Activity [Supine Systolic BP],ItemDef,I.SYSBP_SUPINE,8461-6,Systolic blood pressure--supine,mm[Hg],H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE-Obs
H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING,Standing Systolic BP,Planned Activity [Standing Systolic BP],ItemDef,I.SYSBP_STANDING,8460-8,Systolic blood pressure--standing,mm[Hg],H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING-Obs
H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE,Supine Diastolic BP,Planned Activity [Supine Diastolic BP],ItemDef,I.DIABP_SUPINE,8453-3,Diastolic blood pressure--supine,mm[Hg],H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE-Obs
H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING,Standing Diastolic BP,Planned Activity [Standing Diastolic BP],ItemDef,I.DIABP_STANDING,8454-1,Diastolic blood pressure--standing,mm[Hg],H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING-Obs
```

- [ ] **Step 2: Run the generator**

Run: `python3 scripts/gen-activities.py`
Expected: prints "Generated measurement activities." and creates `input/fsh/generated/Measurement-Activities.gen.fsh`.

- [ ] **Step 3: Remove the now-duplicated stubs from `StudyActivities.fsh`**

Delete these eight `Instance:` blocks (and only these) from `input/fsh/H2Q-MC-LZZT-StudyActivities.fsh`: `H2Q-MC-LZZT-Vital-Signs-HEIGHT`, `H2Q-MC-LZZT-Vital-Signs-WEIGHT`, `H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE`, `H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING`, `H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE`, `H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING`, `H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE`, `H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING`.

Leave the `Vital-Signs-Height-PD`, `Vital-Signs-Weight-PD`, `Vital-Signs-HeartRate-BloodPressure`, and `Vital-Signs-TEMP`/`Temperature-PD` blocks in place (TEMP handled in Task 7).

- [ ] **Step 4: Verify no duplicate ids and a green build**

Run: `grep -c "Instance: H2Q-MC-LZZT-Vital-Signs-WEIGHT$" input/fsh/H2Q-MC-LZZT-StudyActivities.fsh`
Expected: `0` (moved to generated file).

Run: `sushi . 2>&1 | tail -3`
Expected: `0 Errors`.

- [ ] **Step 5: Assert the generated resource is enriched**

Run: `python3 -c "import json;d=json.load(open('fsh-generated/resources/ActivityDefinition-H2Q-MC-LZZT-Vital-Signs-WEIGHT.json'));print(d['kind'],d['intent'],d['code']['coding'][0]['code'],d['observationResultRequirement'][0])"`
Expected: `ServiceRequest plan 29463-7 ObservationDefinition/H2Q-MC-LZZT-Vital-Signs-WEIGHT-Obs`

(`observationResultRequirement` is a **canonical** array of strings in R6 — not a Reference; the relative form mirrors the existing Temperature AD and builds.)

- [ ] **Step 6: Commit**

```bash
git add input/data/measurement-activities.csv input/fsh/generated/Measurement-Activities.gen.fsh input/fsh/H2Q-MC-LZZT-StudyActivities.fsh
git commit -m "feat: generate enriched Vital Signs measurement activities + ObsDefs"
```

---

## Phase 2 — Temperature consolidation

### Task 7: Canonical Temperature — conform, de-duplicate, repoint PD, remove TEMP stub

**Files:**
- Modify: `input/fsh/H2Q-MC-LZZT-VitalSigns-Temperature-1.fsh`
- Modify: `input/fsh/H2Q-MC-LZZT-StudyActivities.fsh` (remove `Vital-Signs-TEMP` stub; repoint `Temperature-PD`)

**Interfaces:**
- Consumes: `Temperature-Observation-LOINC` (existing ObsDef).
- Produces: a single canonical Temperature AD `H2Q-MC-LZZT-Vitalsigns-Temperature` conforming to `StudyActivitySoa`.

- [ ] **Step 1: Conform and de-duplicate the canonical Temperature AD**

In `input/fsh/H2Q-MC-LZZT-VitalSigns-Temperature-1.fsh`, change the second line from `InstanceOf: ActivityDefinition` to `InstanceOf: StudyActivitySoa`, add `kind`/`intent`/`participant`, and replace the trailing requirement lines (the duplicated/inverted `observationRequirement`/`observationResultRequirement` block, current lines 36–42) with a single result requirement. The requirements section becomes exactly:

```fsh
* kind = #ServiceRequest
* intent = #plan
* participant[+].type = #practitioner
* observationResultRequirement = "ObservationDefinition/Temperature-Observation-LOINC"
```

(Insert the `kind`/`intent`/`participant` lines immediately after `* status = #active`; place the single `observationResultRequirement` where the old block was, and delete all other `observationRequirement`/`observationResultRequirement` lines in the file.)

- [ ] **Step 2: Remove the TEMP stub and repoint the Temperature PD**

In `input/fsh/H2Q-MC-LZZT-StudyActivities.fsh`:
- Delete the `Instance: H2Q-MC-LZZT-Vital-Signs-TEMP` block (the stub mis-titled "Weight").
- In `Instance: H2Q-MC-LZZT-Vital-Signs-Temperature-PD`, change
  `* action[+].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-TEMP"`
  to
  `* action[+].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vitalsigns-Temperature"`.

- [ ] **Step 3: Verify green and the PD resolves to the canonical AD**

Run: `sushi . 2>&1 | tail -3`
Expected: `0 Errors`.

Run: `python3 -c "import json;d=json.load(open('fsh-generated/resources/PlanDefinition-H2Q-MC-LZZT-Vital-Signs-Temperature-PD.json'));print(d['action'][0]['definitionUri'])"`
Expected: `ActivityDefinition/H2Q-MC-LZZT-Vitalsigns-Temperature`

Run: `python3 -c "import json;d=json.load(open('fsh-generated/resources/ActivityDefinition-H2Q-MC-LZZT-Vitalsigns-Temperature.json'));print(d['kind'],d['intent']);print('observationRequirement' not in d)"`
Expected: `ServiceRequest plan` then `True` (no input requirement remains).

- [ ] **Step 4: Commit**

```bash
git add input/fsh/H2Q-MC-LZZT-VitalSigns-Temperature-1.fsh input/fsh/H2Q-MC-LZZT-StudyActivities.fsh
git commit -m "refactor: consolidate Temperature to one StudyActivitySoa activity, repoint PD"
```

---

## Phase 3 — PRO exemplar (TTS Acceptability Survey)

### Task 8: Author the TTS Acceptability Survey Questionnaire + scored ObsDef

**Files:**
- Create: `input/fsh/questionnaires/Questionnaire-TTS-Acceptability-Survey.fsh`

**Interfaces:**
- Produces: `Questionnaire` instance `H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey` (referenced by Task 9) and scored ObsDef `H2Q-MC-LZZT-TTS-Acceptability-Score-Obs`.

- [ ] **Step 1: Create the Questionnaire and its scored result ObsDef**

Create `input/fsh/questionnaires/Questionnaire-TTS-Acceptability-Survey.fsh`:

```fsh
// PRO exemplar — core-R6 Questionnaire attached directly from the visit action.
// SDC patterns adopted by convention (no R6 SDC package); extension URLs may
// raise tolerated "unresolved extension" WARNINGS, not errors.
Alias: SDC_EXTRACT = http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemExtractionContext

Instance: H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey
InstanceOf: Questionnaire
Usage: #definition
Title: "TTS Acceptability Survey"
Description: "Patient-reported acceptability survey for the transdermal therapeutic system (TTS)."
* status = #active
* subjectType = #Patient
* identifier[+].value = "F.TTSACC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* code = LOINC#71969-0 "Adverse drug reaction assessment"
* item[+].linkId = "comfort"
  * text = "How comfortable was the patch to wear?"
  * type = #coding
  * answerOption[+].valueString = "Very comfortable"
  * answerOption[+].valueString = "Comfortable"
  * answerOption[+].valueString = "Uncomfortable"
  * answerOption[+].valueString = "Very uncomfortable"
* item[+].linkId = "adhesion"
  * text = "Did the patch stay on for the full wear period?"
  * type = #boolean
* item[+].linkId = "score"
  * text = "Overall acceptability score (0-10)"
  * type = #integer

Instance: H2Q-MC-LZZT-TTS-Acceptability-Score-Obs
InstanceOf: ObservationDefinition
Usage: #example
Title: "TTS Acceptability Score - Observation"
Description: "Scored result extracted from the TTS Acceptability Survey (SDC extraction target)."
* insert ScoredInstrumentObservation(71969-0, [[TTS acceptability score]])
```

- [ ] **Step 2: Verify green (SDC alias unused yet is fine; no errors)**

Run: `sushi . 2>&1 | tail -3`
Expected: `0 Errors`.

Run: `python3 -c "import json;d=json.load(open('fsh-generated/resources/Questionnaire-H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey.json'));print(d['status'],len(d['item']))"`
Expected: `active 3`

- [ ] **Step 3: Commit**

```bash
git add input/fsh/questionnaires/Questionnaire-TTS-Acceptability-Survey.fsh
git commit -m "feat: add TTS Acceptability Survey Questionnaire (PRO exemplar) + scored ObsDef"
```

---

### Task 9: Attach the Questionnaire via `action.definitionCanonical`; remove the TTS AD

**Files:**
- Modify: `input/fsh/H2Q-MC-LZZT-Visit-13.fsh`
- Modify: `input/fsh/H2Q-MC-LZZT-ET-14.fsh`
- Modify: `input/fsh/H2Q-MC-LZZT-StudyActivities.fsh` (remove the TTS AD)

**Interfaces:**
- Consumes: the Questionnaire from Task 8.

- [ ] **Step 1: Repoint the Visit-13 action to the Questionnaire**

In `input/fsh/H2Q-MC-LZZT-Visit-13.fsh`, replace the line
`* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-TTS-Acceptability-Survey"`
with
`* action[=].definitionCanonical = Canonical(H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey)`.

- [ ] **Step 2: Repoint the ET-14 action to the Questionnaire**

In `input/fsh/H2Q-MC-LZZT-ET-14.fsh`, make the same replacement on its
`* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-TTS-Acceptability-Survey"` line.

- [ ] **Step 3: Remove the now-orphaned TTS ActivityDefinition**

In `input/fsh/H2Q-MC-LZZT-StudyActivities.fsh`, delete the
`Instance: H2Q-MC-LZZT-TTS-Acceptability-Survey` block.

- [ ] **Step 4: Verify green and that the action resolves to the Questionnaire**

Run: `sushi . 2>&1 | tail -3`
Expected: `0 Errors` (SDC unresolved-extension warnings tolerated).

Run: `python3 -c "import json;d=json.load(open('fsh-generated/resources/PlanDefinition-H2Q-MC-LZZT-Study-Visit-13.json'));print([a.get('definitionCanonical') for a in d['action'] if a.get('title')=='TTS Acceptability Survey'])"`
Expected: a list containing the Questionnaire canonical (URL ending `...Questionnaire-TTS-Acceptability-Survey`).

Run: `grep -c "H2Q-MC-LZZT-TTS-Acceptability-Survey\b" input/fsh/H2Q-MC-LZZT-StudyActivities.fsh`
Expected: `0`.

- [ ] **Step 5: Commit**

```bash
git add input/fsh/H2Q-MC-LZZT-Visit-13.fsh input/fsh/H2Q-MC-LZZT-ET-14.fsh input/fsh/H2Q-MC-LZZT-StudyActivities.fsh
git commit -m "feat: attach TTS Questionnaire directly via action.definitionCanonical"
```

---

### Task 10: Generator — instrument archetype (seeded for scale)

**Files:**
- Modify: `scripts/gen-activities.py`
- Modify: `scripts/test_gen_activities.py`
- Create: `input/data/instrument-activities.csv`

**Interfaces:**
- Produces: `render_instrument_action(row: dict) -> str` — the `InstrumentAction` insert snippet (proven by test; NOT compiled, since the exemplar action is hand-wired in Task 9 to avoid id/fragment collisions).
- Row keys: `id, title, visit_id, questionnaire_canonical, participant, score_obsdef_id`.

- [ ] **Step 1: Add the failing test**

Append to `scripts/test_gen_activities.py`:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 scripts/test_gen_activities.py`
Expected: FAIL (`no attribute 'render_instrument_action'`).

- [ ] **Step 3: Implement**

Add to `scripts/gen-activities.py`:

```python
def render_instrument_action(row):
    """InstrumentAction insert snippet for a visit PlanDefinition.

    Emitted for reference/scale; the live exemplar action is hand-wired in
    the visit FSH to keep one source of truth per action fragment.
    """
    return (
        f"// Add to PlanDefinition {row['visit_id']}:\n"
        f"* insert InstrumentAction({row['questionnaire_canonical']}, "
        f"[[{row['title']}]], #{row['participant']})\n"
    )
```

- [ ] **Step 4: Run to verify it passes**

Run: `python3 scripts/test_gen_activities.py`
Expected: PASS (all tests OK).

- [ ] **Step 5: Create the seed CSV**

Create `input/data/instrument-activities.csv`:

```csv
id,title,visit_id,questionnaire_canonical,participant,score_obsdef_id
TTS-ACC,TTS Acceptability Survey,H2Q-MC-LZZT-Study-Visit-13,H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey,patient,H2Q-MC-LZZT-TTS-Acceptability-Score-Obs
```

- [ ] **Step 6: Commit**

```bash
git add scripts/gen-activities.py scripts/test_gen_activities.py input/data/instrument-activities.csv
git commit -m "feat: generator instrument-action archetype + seed CSV"
```

---

## Phase 4 — Documentation & final verification

### Task 11: Document the generator workflow; full green verification

**Files:**
- Modify: `input/pagecontent/developer.md`

- [ ] **Step 1: Document the pre-build step**

Append to `input/pagecontent/developer.md`:

```markdown
## Generating activity FSH

Some ActivityDefinitions and their ObservationDefinitions are generated from
CSV definitions. Regenerate before building when the CSVs change:

    python3 scripts/gen-activities.py

This writes `input/fsh/generated/Measurement-Activities.gen.fsh` (DO NOT EDIT).
Run the generator's tests with:

    python3 scripts/test_gen_activities.py
```

- [ ] **Step 2: Regenerate, run generator tests, and confirm idempotency**

Run: `python3 scripts/gen-activities.py && git diff --exit-code input/fsh/generated/`
Expected: exit 0 (no diff — output is idempotent).

Run: `python3 scripts/test_gen_activities.py`
Expected: all tests PASS.

- [ ] **Step 3: Final full build — 0 errors**

Run: `sushi . 2>&1 | tail -4`
Expected: `0 Errors`.

- [ ] **Step 4: Commit**

```bash
git add input/pagecontent/developer.md
git commit -m "docs: document the activity FSH generator workflow"
```

---

## Self-Review notes (coverage map)

- Green baseline (spec: buildable) → Task 1.
- Measurement shape: `code/kind/intent/participant`, `observationResultRequirement` only → RuleSet Task 2; applied Tasks 6, 7.
- Vital Signs family (Height, Weight, Pulse×2, SysBP×2, DiaBP×2) → Task 6; Temperature → Task 7.
- BP position-specific LOINC + metric units → Task 6 CSV.
- Family ObservationDefinitions (code, permittedDataType, permittedUnit, preferredReportName) → RuleSet Task 2; Task 6.
- Temperature consolidation + defect fixes (TEMP title, PULSE-STANDING title, duplicated requirements) → Tasks 6 (PULSE titles via CSV), 7.
- `StudyActivitySoa` conformance → Tasks 6, 7.
- PRO archetype: Questionnaire + `action.definitionCanonical` + scored ObsDef + SDC-by-convention → Tasks 8, 9.
- Acceleration: RuleSets (Task 2) + archetype-driven generator with tests (Tasks 3–5, 10) + idempotency (Tasks 5, 11).
- Developer docs → Task 11.

**Out of scope (per spec):** migrating other 223 `definitionUri` refs to canonical; enriching non-family ObsDef stubs; full PRO family; hard SDC dependency; `StudyActivitySoa` must-support expansion.
