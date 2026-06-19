# ActivityDefinition Templates & Acceleration Design

> Builds two activity archetypes this pass — the **Vital Signs** family (quantitative
> measurement) and one **PRO/instrument** exemplar (Questionnaire-based) — plus
> archetype-aware helpers to scale to the rest.

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

1. Establish **gold-standard templates** for fully built-out `ActivityDefinition`s,
   recognising that the study has **more than one activity archetype** (see below).
2. Prove the **quantitative-measurement** archetype on the **Vital Signs family**, and
   prove the **PRO / instrument** archetype on **one exemplar**, before scaling to all
   ~40 activities.
3. Make the built-out instances **conform to `StudyActivitySoa`**.
4. Stand up **archetype-aware acceleration helpers** (FSH `RuleSet`s now; a CSV-driven
   generator for the full roll-out) so the pattern scales quickly and consistently.
5. Fix the visible copy/paste defects encountered along the way.

## Non-goals

- Building out the other ~30 activities — future work, enabled by the generator.
- Building the **full** PRO/instrument family (ADAS-Cog, MMSE, CIBIC+, DAD, NPI-X,
  Hachinski, …). Only one PRO exemplar is built this pass; authoring real instruments
  at scale is substantial follow-up work.
- Reworking the visit/PlanDefinition framework (already done).
- Enriching ObservationDefinition stubs outside the built families.
- Extending the `StudyActivitySoa` profile's must-support flags (conform only; profile
  enrichment is noted as possible future work).
- Adding a hard `hl7.fhir.uv.sdc` package dependency (no R6 build exists — see PRO
  archetype section); SDC patterns are adopted by convention now.

## Activity archetypes

SoA activities are not uniform. This design recognises distinct archetypes, each with
its own template and its own generator row-type. Two are built this pass; the rest are
catalogued for the roll-out.

| Archetype | Example activities | `kind` | Collection defined by | Result expressed by | Built now? |
|---|---|---|---|---|---|
| **Quantitative measurement** | Vital signs, simple labs | `#ServiceRequest` | `code` + ObservationDefinition | `observationResultRequirement` | **Yes — Vital Signs family** |
| **PRO / clinician instrument** | ADAS-Cog, MMSE, CIBIC+, DAD, NPI-X, Hachinski, TTS Survey, Habits | `#Task` | `relatedArtifact` → **Questionnaire** | `QuestionnaireResponse` (+ optional scored `observationResultRequirement`) | **Yes — one exemplar** |
| Specimen-based lab | Chemistry, Hematology, Urinalysis, Apo-E | `#ServiceRequest` | `specimenRequirement` → SpecimenDefinition (+ result ObsDef) | `observationResultRequirement` | No (future) |
| Procedure / imaging | Chest x-ray, CT, ECG, TTS placement | `#ServiceRequest` / `#Task` | `code` (+ result ObsDef) | `observationResultRequirement` | No (future) |
| Administrative / milestone | Informed consent, randomization, patient number | `#Task` | `code` | (event/status, no observation) | No (future) |

The two built archetypes share the same `StudyActivitySoa` conformance, identifier
handling, and `intent = #plan`; they differ in `kind`, how *what to collect* is defined,
and how *results* are expressed.

## Archetype 1 — Quantitative measurement (Vital Signs) shape

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

## Archetype 2 — PRO / clinician instrument (Questionnaire-based)

Instrument-based activities (PROs and clinician-rated scales) do **not** fit the
quantitative-measurement shape: what they collect is a structured set of items, not a
single coded `Quantity`. They use a `Questionnaire`.

### ActivityDefinition shape (instrument)

| Element | Value | Notes |
|---|---|---|
| `InstanceOf` | `StudyActivitySoa` | same conformance as archetype 1 |
| `status` / `identifier` / `intent` | `#active` / ODM OID (`FormDef`) / `#plan` | as archetype 1 |
| `kind` | `#Task` | completing an instrument is a task, not a service request that yields a measurement |
| `code` | the instrument concept (LOINC panel/survey code where one exists, else SNOMED assessment code) | e.g. a survey-instrument code |
| `relatedArtifact` | `type = #depends-on`, `resource = Canonical(Questionnaire/…)` | **the link to the instrument** — `ActivityDefinition` has no native questionnaire element, so this is the standard way to reference it |
| `observationResultRequirement` | **optional** → ObservationDefinition for a **scored** result (e.g. total score) | only when the instrument yields a reportable derived value |
| `participant` | `type = #patient` (PRO) or `#practitioner` (clinician-rated) | distinguishes self-report vs. rater |

### Result model

- **Raw answers** → a `QuestionnaireResponse`. There is no "QuestionnaireResponseDefinition";
  the **Questionnaire is the definition** of what's collected, so no ObsDef is needed for
  the raw response.
- **Scored outcome** (e.g. ADAS-Cog/MMSE total) → an `Observation`, expressed via
  `observationResultRequirement` exactly as in archetype 1. The score `Observation` is
  `derivedFrom` the `QuestionnaireResponse` at runtime.

`observationRequirement` (input) stays empty here too, unless the instrument genuinely
requires a prior observation to be administered.

### SDC patterns — adopted by convention, package deferred

There is **no R6 build of `hl7.fhir.uv.sdc`** (latest published is R4 `4.0.0`). To keep
the R6 build clean we **do not** add it as a hard dependency this pass. Instead we follow
SDC patterns on a core-R6 `Questionnaire`, using SDC canonical extension URLs where they
add value:

- **Task-based form-filling** — the runtime enactment of the `#Task` activity is an SDC
  "complete-questionnaire" Task whose input is the referenced `Questionnaire`.
- **`sdc-questionnaire-itemExtractionContext`** — defines extraction of the scored
  `Observation` from the `QuestionnaireResponse`, wiring the result back to the
  `observationResultRequirement` target.
- **`sdc-questionnaire-launchContext`** — supplies patient/encounter context at launch.
- **Answer constraints / `enableWhen` skip logic / required items / units** — authored on
  the Questionnaire items.

Caveat: because the SDC extension definitions are not loaded (no R6 package), the
publisher will emit *unresolved-extension* warnings on these URLs. Accepted for now;
resolved when an R6 SDC package exists (tracked as a follow-up). The build must still
**succeed** — these are warnings, not errors.

### Why this improves the site experience

The `Questionnaire` is precisely the resource that drives a good data-entry UX: it
defines items, answer value sets, required-ness, units, and `enableWhen` skip logic, so
the site renders a **validated form** with branching instead of free text. SDC extraction
then produces the scored `Observation` automatically, removing manual transcription and
the queries it generates.

### Exemplar (build one)

Build a single instrument end-to-end: ActivityDefinition (`#Task`) + a real core-R6
`Questionnaire` + (if the instrument scores) a scored ObservationDefinition + the
`observationResultRequirement` link.

**Recommended exemplar: TTS Acceptability Survey** (`F.TTSACC`) — a genuine *patient-reported*
survey, small enough to author fully, and it exercises items + answer options. If a clean
numeric-score extraction is preferred for the demo, **CIBIC+** (single 7-point ordinal,
clinician-rated) or **Hachinski** (summed ischemic score) are alternatives. Final choice
is an open item for spec review.

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

A **second** RuleSet, `InstrumentActivity(...)`, expresses archetype 2 (PRO/instrument):
sets `kind = #Task`, `code`, the `relatedArtifact[depends-on]` → `Questionnaire` link,
and an optional scored `observationResultRequirement`. Both RuleSets emit
`StudyActivitySoa` instances, so the archetypes share conformance and differ only where
they must.

### Stage 2 (now, seeded; scales later): archetype-driven CSV generator

- **Data:** one CSV per archetype (or one CSV with an `archetype` column):
  - `input/data/measurement-activities.csv` — `id, title, description, loinc,
    loinc_display, snomed, oid, oidsys, unit, bodysite, obsdef_id` (seeded with the 9
    Vital Signs rows).
  - `input/data/instrument-activities.csv` — `id, title, description, code, code_system,
    oid, questionnaire_canonical, score_obsdef_id, participant` (seeded with the one
    exemplar row).
- **Script:** `scripts/gen-activities.py` (Python 3.12, stdlib only) dispatches on
  archetype and emits the matching `insert` block — measurement → `VitalSignActivity` +
  ObsDef; instrument → `InstrumentActivity` (+ scored ObsDef when `score_obsdef_id` is
  set). It does **not** generate the Questionnaire bodies themselves (those are authored,
  not tabular); it only emits the activity and its links.
- **Output contract:** writes to clearly-marked generated files (e.g.
  `input/fsh/generated/*-Generated.fsh`) with a "DO NOT EDIT — generated by
  scripts/gen-activities.py" header. Idempotent: an unchanged CSV produces byte-identical
  output. Hand-authored FSH (including Questionnaires) and generated FSH never overlap on
  the same instance id.
- **Workflow:** `python3 scripts/gen-activities.py` is a pre-build step (documented in the
  developer page / README); SUSHI then compiles the generated FSH like any other.
- **Scale path:** rolling out the remaining ~30 activities is adding rows to the right
  CSV (and authoring Questionnaires for new instruments), not hand-authoring activity FSH.

The RuleSets (Stage 1) are the units of reuse the generator emits, so the two stages
share one definition of "what a built-out activity looks like" per archetype.

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
8. The PRO exemplar exists end-to-end: a `StudyActivitySoa` activity with `kind = #Task`,
   a `relatedArtifact[depends-on]` → the authored core-R6 `Questionnaire`, and (if scored)
   an `observationResultRequirement` → scored ObsDef. The build **succeeds** (SDC
   unresolved-extension warnings tolerated; no errors).
9. `gen-activities.py` handles both archetypes from their CSVs and regenerates
   byte-identically.

## Open items to confirm during review

- Height/Weight units (metric vs US customary).
- Position-specific BP LOINC codes (8461-6 / 8460-8 / 8453-3 / 8454-1) vs base codes.
- Whether Pulse should use position-specific LOINC or base 8867-4 + ObsDef distinction.
- **PRO exemplar choice**: TTS Acceptability Survey (recommended) vs CIBIC+ vs Hachinski.
- Whether the chosen exemplar warrants a **scored ObservationDefinition**, or just the
  `QuestionnaireResponse`.
- Which SDC extension URLs to apply now vs leave for the R6-package follow-up.

## Out of scope / future

- The other ~30 activities and their ObservationDefinitions (enabled by the generator).
  Note: the same `observationRequirement`/`observationResultRequirement` misuse (both
  pointing at one ObsDef) exists repo-wide; the generator's correct emission fixes it as
  each family is rolled out. The non-family activities are **not** corrected in this pass.
- Making `code`/`kind`/`bodySite` must-support in `StudyActivitySoa`.
- Wiring `subject[x]` on activities (profile marks it MS but it is optional cardinality).
- Adding `hl7.fhir.uv.sdc` as a hard dependency once an **R6 build exists**, and replacing
  the convention-only SDC usage with validated extensions (resolves the
  unresolved-extension warnings). Tracked as a follow-up.
- The remaining PRO/instrument family and the specimen-based, procedure, and
  administrative archetypes (catalogued in *Activity archetypes*).
