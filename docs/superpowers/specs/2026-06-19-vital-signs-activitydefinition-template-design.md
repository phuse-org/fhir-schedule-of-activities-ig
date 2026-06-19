# Vital Signs ActivityDefinition Family — Template & Acceleration Design

- **Date:** 2026-06-19
- **Status:** Approved (pending spec review)
- **Branch:** feat/r6
- **IG:** ScheduleOfActivityIG (`fhir.example.brandr.soa`), FHIR R6 `6.0.0-ballot3`, SUSHI 3.20.0

## Problem

The IG models the H2Q-MC-LZZT clinical study. The visit framework (13 `Visit`
PlanDefinitions on the `SOAPlanDefinition` profile, plus ET-14/RT-15) is in place
and wires activities together via `action.definitionUri` and `relatedAction`. The
~40 `ActivityDefinition` instances in
[`input/fsh/H2Q-MC-LZZT-StudyActivities.fsh`](../../../input/fsh/H2Q-MC-LZZT-StudyActivities.fsh)
are mostly skeletal: `status`, an ODM `identifier`, and `observationRequirement`
pointers. They lack the coded, machine-usable detail that makes an SoA definitional
resource useful, and they do not conform to the `StudyActivitySoa` profile.

The `Temperature` activity in
[`input/fsh/H2Q-MC-LZZT-VitalSigns-Temperature-1.fsh`](../../../input/fsh/H2Q-MC-LZZT-VitalSigns-Temperature-1.fsh)
is the richest example (real SNOMED `code`, `bodySite`, linked ObservationDefinitions)
and is the de-facto "gold standard," though it has copy/paste defects (duplicated
`observationRequirement`/`observationResultRequirement` lines).

## Goals

1. Establish a **gold-standard template** for a fully built-out `ActivityDefinition`,
   proven on the **Vital Signs family** before scaling to all ~40 activities.
2. Make the family instances **conform to `StudyActivitySoa`**.
3. Stand up **acceleration helpers** (FSH `RuleSet`s now; a CSV-driven generator for the
   full roll-out) so the pattern scales quickly and consistently.
4. Fix the visible copy/paste defects encountered in the family.

## Non-goals

- Building out the other ~30 (non-vital-signs) activities — future work, enabled by
  the generator stood up here.
- Reworking the visit/PlanDefinition framework (already done).
- Enriching ObservationDefinition stubs outside the Vital Signs family.
- Extending the `StudyActivitySoa` profile's must-support flags (conform only; profile
  enrichment is noted as possible future work).

## Target ActivityDefinition shape

Every Vital Signs activity becomes `InstanceOf: StudyActivitySoa` and carries:

| Element | Value approach | Notes |
|---|---|---|
| `status` | `#active` | unchanged |
| `identifier` | existing ODM `ItemDef`/`FormDef` OID; add `PLAC`/`#usual` placer identifier where missing | preserve ODM traceability |
| `code` | real **LOINC** vital-signs code (+ SNOMED where the source uses it, as Temperature does) | the machine-usable concept |
| `kind` | `#ServiceRequest` | required binding is *request-resource-types*; `Observation` is **not** a valid value there. The activity is a **request** that yields observations. |
| `intent` | `#plan` | protocol-planned definition, not yet an order |
| `bodySite` | only where meaningful (Temperature route). BP/Pulse **position** is NOT modelled as `bodySite`. | Height/Weight: none |
| `participant` | `type = #practitioner` | who performs the measurement (required binding *action-participant-type*) |
| `observationResultRequirement` | reference the properly-coded **result** ObservationDefinition(s) | the data the site must **produce** — see next section |
| `observationRequirement` | **empty** for the vital-signs family | reserved for prerequisite *input* observations; no measurement needs one |
| `title`, `description` | corrected, human-readable | fixes copy/paste defects |

All element paths and required bindings verified against
`hl7.fhir.r6.core#6.0.0-ballot3`.

### Why `kind = #ServiceRequest` / `intent = #plan`

`ActivityDefinition.kind` has a *required* binding to `request-resource-types`, which
lists request resources (ServiceRequest, Task, …) — **not** `Observation`. A vital-sign
measurement activity is therefore modelled as a request (`ServiceRequest`) whose result
is captured as observations via `observationResultRequirement`. `intent = #plan`
reflects that these are protocol definitions, not instantiated orders.

## Communicating requirements: `observationRequirement` vs `observationResultRequirement`

This is the sponsor (clinical-trials) side expressing requirements to sites. The two
elements are **not** interchangeable — R6 defines them as opposites:

| Element | R6 definition | Direction | Use in this IG |
|---|---|---|---|
| `observationResultRequirement` | "What observations must be **produced by** this action" | **output** | The data the site must **return**. Every vital-signs measurement uses this. |
| `observationRequirement` | "What observations are **required to perform** this action" | **input / prerequisite** | An observation that must **already exist** before the activity can be done (e.g. body weight to compute a dose). **No vital-sign measurement needs one — leave empty.** |

### The current defect

Today nearly every activity (Temperature included) points **both** elements at the
**same** ObservationDefinition. That asserts "this measurement requires its own output
as an input," which is incorrect. The correction: for data-collection activities, set
**`observationResultRequirement` only** and leave `observationRequirement` empty unless
a genuine prerequisite exists.

### Why the ObservationDefinition is the channel that improves the site experience

The sponsor communicates *what to return* by pointing at a well-formed
ObservationDefinition, not by adding prose to the activity. The ObservationDefinition
carries the machine-validatable spec the site's system can act on:

- `code` (1..1) — the exact coded concept expected
- `permittedDataType` — e.g. `Quantity`, so the field renders as a number, not free text
- `permittedUnit` — UCUM units the site may submit (validate at entry)
- `bodySite` / `method` — where/how, when it qualifies the result
- `preferredReportName` — a clear, consistent label for the field
- `qualifiedValue.range` (+ `.context` for normal vs critical) — reference/critical
  ranges so the site can flag out-of-range values **at the point of entry**
- `multipleResultsAllowed`, `component` — repetition and multi-part results (e.g. BP)

Result: the site's EDC can pre-render exact expected fields, datatypes, units, and
ranges, validate inline, and reduce downstream data queries — the requirement is
expressed once, precisely, and reused across every visit that schedules the activity.

> Note for later (labs, out of family scope): `specimenRequirement` (→ SpecimenDefinition)
> *is* a genuine input requirement — a blood/urine specimen the site must collect to run
> a lab. That one is correctly a "required to perform" element. Captured here so the
> generator handles it correctly when the family pattern scales to laboratory activities.

## Family members & Temperature consolidation

Built out **in place** in `H2Q-MC-LZZT-StudyActivities.fsh`:

| Activity | Existing id | Action |
|---|---|---|
| Temperature | `H2Q-MC-LZZT-Vitalsigns-Temperature` (rich) **and** `H2Q-MC-LZZT-Vital-Signs-TEMP` (stub, mis-titled "Weight") | **Consolidate**: keep the rich one as canonical; **remove its `observationRequirement` lines entirely** and keep a single `observationResultRequirement` → the temperature result ObsDef (drop the duplicated/inverted links); delete the stub; repoint `H2Q-MC-LZZT-Vital-Signs-Temperature-PD` to the canonical id |
| Height | `H2Q-MC-LZZT-Vital-Signs-HEIGHT` | enrich |
| Weight | `H2Q-MC-LZZT-Vital-Signs-WEIGHT` | enrich |
| Pulse (supine) | `H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE` | enrich |
| Pulse (standing) | `H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING` | enrich; fix "Supine Pulse" title/description defect |
| Systolic BP (supine) | `H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE` | enrich |
| Systolic BP (standing) | `H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING` | enrich |
| Diastolic BP (supine) | `H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE` | enrich |
| Diastolic BP (standing) | `H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING` | enrich |

Supine vs. standing is represented by **separate definitions** (distinct ids, titles,
and ObservationDefinitions), not by `bodySite`.

## Proposed code mapping

LOINC primary; SNOMED retained for Temperature (matches existing). Units are UCUM.
Position-specific LOINC codes are used where they exist and are **flagged to confirm**
during review; the CSV carries the exact code per row so a reviewer can verify each.

| Activity | LOINC | Display | Unit (UCUM) | SNOMED | Confirm? |
|---|---|---|---|---|---|
| Temperature | 8310-5 | Body temperature | `Cel` | 56342008 (procedure) | existing |
| Height | 8302-2 | Body height | `cm` | — | unit (cm vs `[in_us]`) |
| Weight | 29463-7 | Body weight | `kg` | — | unit (kg vs `[lb_av]`) |
| Pulse (supine) | 8867-4 | Heart rate | `/min` | — | position-specific code if preferred |
| Pulse (standing) | 8867-4 | Heart rate | `/min` | — | position-specific code if preferred |
| Systolic BP (supine) | 8461-6 | Systolic BP – supine | `mm[Hg]` | — | confirm code |
| Systolic BP (standing) | 8460-8 | Systolic BP – standing | `mm[Hg]` | — | confirm code |
| Diastolic BP (supine) | 8453-3 | Diastolic BP – supine | `mm[Hg]` | — | confirm code |
| Diastolic BP (standing) | 8454-1 | Diastolic BP – standing | `mm[Hg]` | — | confirm code |

Unit choices (cm/kg vs US customary) to be confirmed against the source protocol
during review; the CSV makes a flip a one-cell change.

## ObservationDefinitions for the family

These are the **result requirements** the sponsor communicates to sites, so this is
where the detail that improves the site experience lives. Targets must exist for the
`observationResultRequirement` links to be meaningful. Temperature already has real
ObsDefs (`Temperature-Observation-SNOMED`, `Temperature-Observation-LOINC`,
`VitalSigns-Observation`). For Height, Weight, Pulse, Systolic BP, Diastolic BP,
**enrich the existing stubs** (or add where missing) in
[`input/fsh/H2Q-MC-LZZT-StudyObservations.fsh`](../../../input/fsh/H2Q-MC-LZZT-StudyObservations.fsh)
with:

- `status = #active`
- `code` (1..1) — the LOINC concept matching the activity
- `permittedDataType = #Quantity`
- `permittedUnit` — the UCUM unit(s) the site may submit (validatable at entry)
- `bodySite` / `method` where it qualifies the result (e.g. temperature route)
- `preferredReportName` — a clear field label
- `qualifiedValue.range` (+ `.context` for reference vs critical) where a sensible
  range exists, so sites can flag out-of-range values at entry

Element names verified against `hl7.fhir.r6.core#6.0.0-ballot3` (note: R6 uses
`permittedUnit`, not a `quantitativeDetails` block).

The other ~30 ObsDef stubs are untouched.

## Profile conformance

Instances change to `InstanceOf: StudyActivitySoa`. This sets `meta.profile` and
validates against the profile's must-support set (`url`, `name`, `title`, `status`,
`subject[x]`, `description`, `observationRequirement`). The added elements (`code`,
`kind`, `intent`, `bodySite`, `participant`) are permitted; making any of them
must-support in the profile is **out of scope** here (future).

## Acceleration — staged

### Stage 1 (now): FSH `RuleSet`s

Introduce parameterized rule sets (no existing RuleSets in the repo; SUSHI 3.20.0
supports them). Collapse each activity from ~15 lines to ~3 and enforce consistency.
Sketch:

```fsh
RuleSet: VitalSignActivity(oidsys, oid, loinc, lname, unit)
* status = #active
* kind = #ServiceRequest
* intent = #plan
* participant[+].type = #practitioner
* identifier[+].value = "{oid}"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/{oidsys}#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* code.coding[+] = $LOINC#{loinc} "{lname}"
* observationResultRequirement = Reference(obsdef-{loinc})
// NOTE: no observationRequirement here — these activities produce results, not consume them

Instance: H2Q-MC-LZZT-Vital-Signs-WEIGHT
InstanceOf: StudyActivitySoa
Usage: #example
Title: "Weight"
Description: "Planned Activity [Weight]"
* insert VitalSignActivity(ItemDef, I.WEIGHT, 29463-7, "Body weight", kg)
```

A companion `VitalSignObservation(...)` RuleSet covers the paired ObservationDefinitions
and carries the result-spec detail (`permittedDataType`, `permittedUnit`,
`preferredReportName`, `qualifiedValue` ranges). The activity references it via
`observationResultRequirement` only; `observationRequirement` is never emitted for this
family. `title`/`description`/`bodySite` that vary stay on the instance.

### Stage 2 (now, seeded; scales later): CSV-driven generator

- **Data:** `input/data/vital-signs-activities.csv` — one row per activity. Columns:
  `id, title, description, loinc, loinc_display, snomed, oid, oidsys, unit, bodysite,
  obsdef_id`. Seeded with the 9 family rows so the generator is proven before scaling.
- **Script:** `scripts/gen-activities.py` (Python 3.12, stdlib only) reads the CSV and
  emits FSH `insert` blocks (or full instances) for ActivityDefinitions and their
  paired ObservationDefinitions.
- **Output contract:** writes to a clearly-marked generated file (e.g.
  `input/fsh/generated/VitalSigns-Generated.fsh`) with a "DO NOT EDIT — generated by
  scripts/gen-activities.py" header. Idempotent: re-running with an unchanged CSV
  produces byte-identical output. Hand-authored FSH and generated FSH never overlap on
  the same instance id.
- **Workflow:** `python3 scripts/gen-activities.py` is a pre-build step (documented in
  the developer page / README); SUSHI then compiles the generated FSH like any other.
- **Scale path:** rolling out the remaining ~30 activities is adding rows to a CSV +
  rerun, not hand-authoring FSH.

The RuleSet (Stage 1) is the unit of reuse the generator emits, so the two stages share
one definition of "what a built-out activity looks like."

## Validation / done criteria

1. `sushi` (or `_genonce`) builds the family with **no errors** and no new warnings
   attributable to the changed instances.
2. The 9 family instances are `StudyActivitySoa` and validate against it.
3. No duplicate Temperature definition remains; `Vital-Signs-Temperature-PD` points to
   the canonical id; the visit PlanDefinitions still resolve their `definitionUri`s.
4. Copy/paste defects fixed (TEMP title, PULSE-STANDING title/description, duplicated
   Temperature requirement lines).
5. `python3 scripts/gen-activities.py` regenerates the generated file byte-identically
   (idempotent), and the generated FSH compiles.
6. Family ObservationDefinitions carry real LOINC codes + `permittedDataType` +
   `permittedUnit` (and `preferredReportName`/`qualifiedValue` where sensible).
7. Every family activity uses **`observationResultRequirement` only**; no
   `observationRequirement` remains on any vital-signs activity.

## Open items to confirm during review

- Height/Weight units (metric vs US customary).
- Position-specific BP LOINC codes (8461-6 / 8460-8 / 8453-3 / 8454-1) vs base codes.
- Whether Pulse should use position-specific LOINC or base 8867-4 + ObsDef distinction.

## Out of scope / future

- The other ~30 activities and their ObservationDefinitions (enabled by the generator).
  Note: the same `observationRequirement`/`observationResultRequirement` misuse (both
  pointing at one ObsDef) exists repo-wide; the generator's correct emission fixes it as
  each family is rolled out. The non-family activities are **not** corrected in this pass.
- Making `code`/`kind`/`bodySite` must-support in `StudyActivitySoa`.
- Wiring `subject[x]` on activities (profile marks it MS but it is optional cardinality).
