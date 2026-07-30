# Phase F: USDM → HL7 Vulcan Schedule of Activities Transform

- **Date:** 2026-06-30
- **Status:** Approved — ready for agent dispatch
- **Branch:** feat/usdm-transform (new branch from current HEAD)
- **IG:** ScheduleOfActivityIG (`fhir.example.brandr.soa`), FHIR R6 `6.0.0-ballot3`, SUSHI 3.20.0
- **Builds on:** Phases A–E (catalog foundation + generation pipeline)
- **Source:** `input/usdm/CDISC_Pilot_Study_v4_FIXED.json` (CDISC Pilot Study H2Q-MC-LZZT, USDM v4)

---

## Problem

The IG currently has hand-authored FSH resources covering the H2Q-MC-LZZT study. The USDM
file covering the same study exists in `input/usdm/` but is not connected to the generation
pipeline. We want **USDM as the sole source of truth**: a re-runnable Python pipeline reads
the USDM JSON and emits all FSH and catalog CSVs that the existing framework knows how
to compile. Hand-authored FSH files are kept as reference but are superseded by generated
equivalents.

---

## Goals

1. Parse the full USDM JSON and emit idempotent FSH for: ResearchStudy, Organization,
   Practitioner, eligibility Groups, per-visit SOAPlanDefinitions, and the master
   ProtocolDesign SOAPlanDefinition.
2. Extract activity, observation, and SoA-matrix catalog CSVs from the USDM so the
   existing Phase A–E generation pipeline can consume them.
3. Enrich activity catalog entries with SNOMED and CPT codes via the healthcare MCP
   at authoring time (one-shot, human-reviewed, then baked into the CSVs).
4. Identify PRO vs clinician-reported instruments via a `respondent_type` column so
   visit actions carry the correct `action.participant.type`.
5. Produce a reconciliation report comparing USDM-derived resources against the
   hand-authored equivalents.
6. Document the pipeline in the published IG.

## Non-goals

- Replacing the Phase A–E pipeline mechanics — Phase F feeds inputs into it, not around it.
- Full Questionnaire item authoring (ADAS-Cog items, MMSE items, etc.) — shells only.
- Runtime MCP calls — MCP is used only during Task F-5b authoring enrichment.
- Automatic promotion of MCP-enriched codes — human review is always required before
  codes enter the live catalog.

---

## Architecture

```
INPUTS                         PHASE F PIPELINE                    OUTPUTS
──────────────────────────────────────────────────────────────────────────────
input/usdm/                    usdm_to_soa.py                      input/fsh/generated/usdm/
  CDISC_Pilot_Study_v4_FIXED     ├── USDMDoc (loader/indexer)        ├── ResearchStudy.gen.fsh
  .json                          ├── TimingResolver                  ├── Eligibility.gen.fsh
                                 ├── emit_research_study()           ├── ProtocolDesign.gen.fsh
                                 ├── emit_eligibility_groups()       └── visits/
                                 ├── emit_visit_plan_definitions()       └── <EncounterName>.gen.fsh
                                 ├── emit_protocol_design()
                                 ├── extract_activity_catalog()      input/data/
                                 ├── extract_observation_catalog()   ├── usdm-activity-catalog.csv
                                 └── extract_soa_matrix()            ├── usdm-observation-catalog.csv
                                                                      └── usdm-soa-matrix.csv

                               enrich_catalog.py (authoring-time,   input/data/
                               agent-interactive, one-shot)          ├── usdm-activity-catalog-enriched.csv
                                 └── healthcare MCP queries          └── usdm-observation-catalog-enriched.csv

                               usdm_reconcile.py                    docs/superpowers/
                                                                      └── usdm-reconciliation.md
```

The pipeline reads **only** the USDM JSON. It never reads compiled FSH or `fsh-generated/`.
All outputs carry a `// DO NOT EDIT` header. The live catalogs (`activity-catalog.csv` etc.)
are updated manually after human review of the enriched/reconciled outputs.

---

## Activity classification decision tree

```
Activity node in USDM
├── has biomedicalConceptIds?          → archetype = measurement
│     BiomedicalConcept → code + unit  → ActivityDefinition + ObservationDefinition
│
├── else has bcSurrogateIds?           → archetype = instrument
│     BiomedicalConceptSurrogate       → Questionnaire shell + scored ObsDef
│     respondent_type column drives action.participant.type (see below)
│
├── else has definedProcedures[0]      → archetype = procedure
│     with a non-null code?            → ActivityDefinition (no observationResultRequirement)
│
└── else                               → WARNING "unclassified:<id>", skip row
```

**Precedence:** `biomedicalConceptIds` wins when both a BC ref and `definedProcedures` are
present on the same Activity (e.g. Activity_7 Physical examination).

---

## Instrument respondent_type lookup

The USDM `BiomedicalConceptSurrogate` carries no machine-readable PRO/ClinRO flag.
Respondent type is therefore encoded in a `respondent_type` column in the activity catalog,
populated from the table below. All instrument activities emit `Questionnaire` resources.
The `respondent_type` value drives `action.participant[+].type` in the visit action and
distinguishes true PROs (patient-completed) from clinician-administered scales.

| Activity label               | USDM surrogate id            | respondent_type  |
|------------------------------|------------------------------|------------------|
| Demographics / Date of Birth | BiomedicalConceptSurrogate_1 | practitioner     |
| Hachinski Ischemic Scale     | BiomedicalConceptSurrogate_2 | practitioner     |
| MMSE                         | BiomedicalConceptSurrogate_3 | practitioner     |
| Apo E Genotype               | BiomedicalConceptSurrogate_4 | practitioner     |
| Placebo TTS test             | BiomedicalConceptSurrogate_5 | patient          |
| ADAS-Cog (hand-authored ref) | —                            | practitioner     |
| CIBIC+  (hand-authored ref)  | —                            | practitioner     |
| DAD     (hand-authored ref)  | —                            | related-person   |
| NPI-X   (hand-authored ref)  | —                            | related-person   |
| TTS Acceptability Survey     | —                            | patient          |

Activities with `respondent_type = patient` are **true PROs** — visit action uses
`definitionCanonical` with `action.participant[+].type = #patient`.

`measurement` and `procedure` rows leave `respondent_type` blank.

---

## Code enrichment policy (Task F-5b)

- The **USDM code is always the primary code**. MCP-derived codes go in supplementary
  columns (`snomed_code`, `snomed_display`, `cpt_code`, `cpt_display`) and are never
  auto-promoted.
- Generated FSH emits both the primary code and any supplementary codes as additional
  `ActivityDefinition.code.coding[]` entries when present in the live catalog.
- `code_enrichment_status` column records: `confirmed` / `enriched` / `supplemented` /
  `manual` / `skipped`.
- Human reviews the enriched CSV and copies accepted columns into the live catalog.

---

## Dependency graph

```
F-0 (audit + mapping spec — no code)
 ├── F-1 (ResearchStudy + Org + Practitioner FSH)   ─┐
 ├── F-2 (Eligibility Groups FSH)                    │
 ├── F-3 (TimingResolver — pure logic, no FSH)        ├── F-8 (orchestration + integration test)
 │     └── F-4 (Visit PlanDefinition FSH)             │     └── F-9 (reconciliation report)
 │           └── F-7 (ProtocolDesign PlanDef FSH) ───┘           └── F-10 (IG documentation)
 └── F-5 (activity + observation catalog extraction)
       ├── F-5b (MCP enrichment — authoring-time, agent-interactive, one-shot)
       └── F-6 (SoA matrix extraction)
```

F-1, F-2, F-3, F-5 are independent and can run in parallel after F-0.
F-5b is a one-shot authoring step that runs after F-5; it is **not** part of the
re-runnable pipeline.

---

## Constraints for all agents

- Python 3, **stdlib only** — no pip installs, no third-party imports.
- All generated FSH files carry `// DO NOT EDIT — generated by scripts/usdm_to_soa.py`
  as the first line. CSV outputs carry `# DO NOT EDIT — generated by scripts/usdm_to_soa.py`.
- Output FSH directory: `input/fsh/generated/usdm/` — a new subdirectory; never touch
  files outside the task's stated output list.
- `sushi .` must build **0 Errors** after every task (pre-existing Warnings are tolerated).
- All functions have `unittest` test coverage. Tests run with
  `python3 -m unittest discover scripts/`.
- Idempotent: running the script twice on unchanged inputs produces byte-identical outputs.
- One commit per task; message starts `feat(F-N):` matching the task number.
- **Never** use `git checkout`, `git clean`, `git stash`, or touch files outside the
  task's stated output list.

---

## Task F-0 — Audit & mapping spec

**Agent writes:** documentation only — no code, no FSH.
**Output:** `docs/superpowers/specs/2026-06-F0-usdm-mapping-audit.md`

The agent must read the full USDM JSON (`input/usdm/CDISC_Pilot_Study_v4_FIXED.json`)
and the existing hand-authored FSH files and produce a mapping spec covering:

1. **USDM instanceType inventory** — every `instanceType` present in the file with count.

2. **Field-level mapping table** — for every USDM path used downstream:

   | USDM path | FHIR resource | FHIR element | Notes |
   |-----------|---------------|--------------|-------|

3. **Encounter ↔ timing resolution logic** — exact algorithm for:
   - `encounter.scheduledAtId` → `Timing` object lookup
   - `Timing.value` (ISO 8601 duration) → `soaPlannedTimePoint` Quantity (days)
   - `Timing.windowLower` / `windowUpper` → `soaPlannedRange`
   - `Timing.relativeFromScheduledInstanceId` → `soaReferenceTimePoint` string
   - Null `scheduledAtId` → anchor visit (no timing extension values)

4. **Visit × activity schedule encoding** — how `ScheduledActivityInstance` records and
   `Activity.timelineId` together determine which activities appear at which encounters.

5. **Gaps** — USDM fields with no current FHIR home in the profiles, with proposed
   disposition (map / extend profile / drop with rationale). In particular: does
   `SoA-Profiles.fsh` have an element for encounter contact mode (IN PERSON /
   TELEPHONE CALL)? If not, propose a workaround.

6. **Timing spot-check table** — for each encounter, the USDM-derived planned day and
   window vs. the values in the hand-authored `H2Q-MC-LZZT-ProtocolDesign.fsh` actions.
   Flag any discrepancies.

**Done when:** document exists and covers all six sections; no code written.

---

## Task F-1 — ResearchStudy + Organization + Practitioner FSH

**Inputs:** F-0 audit, USDM JSON
**New files:**
- `scripts/usdm_reader.py` — started here; `USDMDoc` class + `emit_research_study()`
- `scripts/test_usdm_reader.py` — started here; unit tests for F-1 content
- `input/fsh/generated/usdm/ResearchStudy.gen.fsh`

### USDMDoc class (foundation for all later tasks)

```python
class USDMDoc:
    def __init__(self, path: str): ...
    # Loads JSON; builds a flat id→object index over the entire document
    # so any object can be resolved in O(1) by its "id" field.
    def resolve(self, id: str) -> dict: ...
    def study(self) -> dict: ...
    def study_version(self) -> dict: ...      # versions[0]
    def study_design(self) -> dict: ...       # versions[0].studyDesigns[0]
    def encounters(self) -> list[dict]: ...
    def activities(self) -> list[dict]: ...
    def schedule_timelines(self) -> list[dict]: ...
    def bc_surrogates(self) -> list[dict]: ...
    def biomedical_concepts(self) -> list[dict]: ...
```

### Mapping

| USDM path | FHIR element |
|-----------|--------------|
| `study.name` | `ResearchStudy.title` |
| `study.versions[0].studyIdentifiers[].text` (scopeId → Organization type) | `ResearchStudy.identifier[]` — sponsor id and NCT number |
| `studyDesigns[0].studyPhase.standardCode` | `ResearchStudy.phase` (CDISC → FHIR phase code mapping) |
| `studyDesigns[0].indications[].codes[]` | `ResearchStudy.condition` (ICD-10 / SNOMED) |
| `studyDesigns[0].therapeuticAreas[]` | `ResearchStudy.focus` |
| `studyDesigns[0].arms[].name/label/description/type` | `ResearchStudy.comparisonGroup[]` |
| `studyDesigns[0].epochs[]` (nextId chain) | `ResearchStudy.phase` note or period extension |
| organizations[] scoped to sponsor | `Organization` instance + `ResearchStudy.sponsor` |
| persons[] with PI role | `Practitioner` instance + `ResearchStudy.principalInvestigator` |
| `studyDesigns[0].objectives[]` | `ResearchStudy.objective[]` (primary/secondary per level code) |

Output FSH instance id: `H2Q-MC-LZZT-ResearchStudy-USDM` (the `-USDM` suffix allows
coexistence with the hand-authored original during transition).

**Done when:** `sushi .` 0 errors; tests cover all mapped fields; output is idempotent.

---

## Task F-2 — Eligibility Groups FSH

**Inputs:** F-0 audit, `usdm_reader.py`
**New / modified files:**
- `scripts/usdm_reader.py` — add `emit_eligibility_groups()`
- `scripts/test_usdm_reader.py` — add tests
- `input/fsh/generated/usdm/Eligibility.gen.fsh`

### Mapping

```
studyDesigns[0].population.criterionIds
  → EligibilityCriterion[] (resolved via USDMDoc.resolve())
  → split by criterion.category code:
      C25532 (Inclusion) → Group: H2Q-MC-LZZT-ResearchStudy-Inclusion-USDM
      C25370 (Exclusion) → Group: H2Q-MC-LZZT-ResearchStudy-Exclusion-USDM
  → each criterion → Group.characteristic[+]
      .code = #eligibility
      .valueCodeableConcept.text = criterion.text (strip HTML tags)
      .exclude = false (inclusion) | true (exclusion)
```

Pattern must match `H2Q-MC-LZZT-ResearchStudy-Eligibility.fsh` exactly (same profile,
same characteristic structure).

**Done when:** 31 criteria mapped; inclusion/exclusion split correct; builds 0 errors;
tests pass.

---

## Task F-3 — TimingResolver

**Inputs:** F-0 audit, `usdm_reader.py`
**New / modified files:**
- `scripts/usdm_reader.py` — add `TimingResolver` class and `ResolvedTiming` dataclass
- `scripts/test_usdm_reader.py` — add tests (pure logic, no FSH output)

### TimingResolver contract

```python
@dataclass
class ResolvedTiming:
    planned_day_value: float          # e.g. 14.0
    planned_day_unit: str             # always "d"
    transition_delay_days: float
    window_lower_days: float | None
    window_upper_days: float | None
    reference_encounter_name: str | None  # FHIR id of the reference encounter

class TimingResolver:
    def __init__(self, usdm_doc: USDMDoc): ...
    def resolve(self, scheduled_at_id: str | None) -> ResolvedTiming | None:
        # Returns None for anchor visits (scheduled_at_id is null)
        ...
```

### ISO 8601 duration parser (stdlib only)

Must handle at minimum: `P<n>D` (days) and `P<n>W` (weeks → multiply by 7).
Raise `ValueError` on unsupported formats.

### Required test cases

| Timing id | Expected planned_day_value | Notes |
|-----------|---------------------------|-------|
| null      | None (anchor visit)        | No timing extension values |
| Timing_2  | 2.0                        | P2D |
| Timing_4  | 14.0                       | P14D |
| Timing_5  | 28.0                       | P28D |

**Done when:** all 16 non-null `scheduledAtId` references resolve without error;
known values verified by tests.

---

## Task F-4 — Visit PlanDefinition FSH

**Inputs:** F-3 `TimingResolver`, F-0 audit
**New / modified files:**
- `scripts/usdm_reader.py` — add `emit_visit_plan_definitions()`
- `scripts/test_usdm_reader.py` — add tests
- `input/fsh/generated/usdm/visits/<EncounterName>.gen.fsh` — one file per encounter

### Per-visit FSH structure (visit skeleton only — no activity-action block)

```fsh
Instance: H2Q-MC-LZZT-<encounter.name>-USDM
InstanceOf: SOAPlanDefinition
Usage: #definition
Title: "<encounter.label>"
Description: "<encounter.description>"
* status = #active
* action[+]
  * id = "<encounter.name>"
  * title = "<encounter.label>"
  * extension[soaTimepoint]
      * extension[soaTimePointType].valueCode = "interaction"
      * extension[soaTimePointSubType].valueCode = <derived — see table below>
      * extension[soaPlannedTimePoint].valueQuantity = <planned_day_value> 'd' UCUM
      * extension[soaReferenceTimePoint].valueString = "<reference_encounter_name>"
      * extension[soaPlannedRange].valueRange.low  = <window_lower> 'd' UCUM
      * extension[soaPlannedRange].valueRange.high = <window_upper> 'd' UCUM
      * extension[soaRepeatAllowed].valueBoolean = false   // true for retreatment visits
  * relatedAction[+]
      * targetId = "<prior_encounter.name>"
      * relationship = #after
      * offsetRange.low.value = <window_lower>
      * offsetRange.low.unit = "d"
  * action[+]   // transition sub-action
      * extension[soaTransition]
          * extension[soaTargetId].valueString    = "<prior_encounter.name>"
          * extension[soaTargetName].valueString  = "<prior_encounter.label>"
          * extension[soaTransitionType].valueCode = "scheduled"
          * extension[soaTransitionDelay].valueDuration = <transition_delay_days> 'd'
          * extension[soaTransitionRange].valueRange.low/high = window
      * description = "<transitionStartRule.text> / <transitionEndRule.text>"
```

### soaTimePointSubType derivation

| Encounter label contains | soaTimePointSubType   |
|--------------------------|-----------------------|
| "Screening"              | `"screening"`         |
| "Baseline"               | `"baseline"`          |
| "Early Termination"      | `"early-termination"` |
| "Retreatment"            | `"retreatment"`       |
| Anything else            | `"planned"`           |

### Anchor visit

`Encounter_1` has `scheduledAtId = null` → emit `soaTimepoint` with `soaTimePointType`
and `soaTimePointSubType` only. No timing values, no `relatedAction`.

### Encounter contact modes

`encounter.contactModes[].code.decode` (e.g. `"IN PERSON"`, `"TELEPHONE CALL"`) —
check `SoA-Profiles.fsh` for the correct target element. If no element exists, document
as a gap (per F-0 audit) and encode as `action.code` using a CDISC coded value as a
pragmatic workaround. Note the gap in a FSH comment on the generated action.

**Done when:** 12 regular visits + ET + RT files generated; timing spot-checks pass
against hand-authored ProtocolDesign; `sushi .` 0 errors; tests pass.

---

## Task F-5 — Activity & observation catalog extraction

**Inputs:** F-0 audit, `usdm_reader.py`
**New / modified files:**
- `scripts/usdm_reader.py` — add `extract_activity_catalog()` and `extract_observation_catalog()`
- `scripts/test_usdm_reader.py` — add tests
- `scripts/catalog.py` — update `validate_activities()` to accept `procedure` archetype
- `input/data/usdm-activity-catalog.csv`
- `input/data/usdm-observation-catalog.csv`

### Activity catalog schema

```
id, oid, oidsys, title, archetype, code_system, code, code_display,
unit, result_obsdef_id, questionnaire_id, respondent_type, default_condition
```

- `id`: slugify `activity.label` (lowercase, spaces → hyphens, strip special chars);
  must be unique within the file
- `archetype` ∈ `{measurement, instrument, procedure}`
- `respondent_type` ∈ `{patient, practitioner, related-person, ""}` — blank for
  measurement and procedure rows; populate from the lookup table in this spec for
  instrument rows; `validate_activities()` must error if an instrument row has blank
  `respondent_type`
- `code` / `code_system` / `code_display`: from `BiomedicalConcept.code` (measurement),
  `definedProcedures[0].code` (procedure), or blank for instrument rows without an
  explicit surrogate code
- `unit`: from `BiomedicalConceptProperty` where property carries a unit `AliasCode`
  and `name` matches a result-value property (e.g. `VSORRES`); blank otherwise
- `result_obsdef_id`: `<activity-id>-obs` for measurement rows; blank for all others
- `questionnaire_id`: surrogate id slugified for instrument rows; blank otherwise

### Observation catalog schema

```
obsdef_id, kind, member_of, code, code_display, unit, datatype
```

- One row per `BiomedicalConcept` → `kind = analyte`
- One row per `BiomedicalConceptCategory` that groups BCs → `kind = panel`; the
  analyte rows for member BCs carry `member_of = <panel-obsdef-id>`
- `code` / `code_display`: from `BiomedicalConcept.code` (LOINC where available, else SNOMED)
- `unit`: from the concept's result property
- `datatype`: `Quantity` for numeric analytes; `string` for non-numeric; blank for panels

### catalog.py update

Update `validate_activities()` to:
- Accept `procedure` as a valid archetype
- Validate procedure rows: `code` non-empty, `result_obsdef_id` empty, `questionnaire_id` empty
- Validate instrument rows: `respondent_type` non-empty (error if blank)
- All other existing validations unchanged

**Done when:** 36 leaf activities classified with 0 unclassified warnings;
`python3 scripts/catalog.py` validates both output CSVs without errors; tests pass.

---

## Task F-5b — MCP code enrichment (authoring-time, agent-interactive)

**This task is NOT part of the re-runnable pipeline. It runs once, interactively,
in an agent session that has access to the healthcare MCP tools.**

**Inputs:** `input/data/usdm-activity-catalog.csv`, `input/data/usdm-observation-catalog.csv`
**Outputs:**
- `scripts/enrich_catalog.py` — documents the enrichment logic; `main()` stub records
  the algorithm as executable documentation
- `input/data/usdm-activity-catalog-enriched.csv`
- `input/data/usdm-observation-catalog-enriched.csv`

### Enrichment procedure

For each activity row, the agent calls `healthcare_search_clinical_concepts` with:
- `concept` = `title` (or `code_display` if more specific)
- `sources = ["SNOMEDCT_US", "CPT"]`
- `return_id_type = "code"`
- `max_results = 5`
- `search_type = "words"`

Select the **top result from each source** where `rootSource ∈ {SNOMEDCT_US, CPT}` and
the result name is a reasonable semantic match. For borderline or ambiguous cases, record
`code_enrichment_status = manual`.

For each observation row:
- `sources = ["SNOMEDCT_US", "LNC"]`
- Same logic; LOINC (`LNC`) takes priority for analyte `ObservationDefinition` codes.

### Additional columns written to enriched CSV

```
snomed_code, snomed_display, cpt_code, cpt_display, loinc_code, loinc_display,
code_enrichment_status
```

### code_enrichment_status values

| Value          | Meaning |
|----------------|---------|
| `confirmed`    | Existing USDM code verified — MCP top hit matches the USDM code |
| `supplemented` | USDM had a code; MCP adds a code from a different system |
| `enriched`     | USDM had no code; MCP found a clean match |
| `manual`       | No clean MCP hit; human must supply or verify |
| `skipped`      | Administrative activity; no clinical code expected |

Activities expected to be `skipped`: Patient number assigned, Patient randomised (uses
OMOP in USDM), Study drug record / dispensed / returned, Visit date.

### Code promotion policy

The primary `code` / `code_system` / `code_display` columns remain unchanged from the
USDM extract — the USDM code is always the primary. Enriched columns are supplementary.
A human reviews the enriched CSV and manually promotes accepted codes into the live
`activity-catalog.csv` before the Phase A–E pipeline runs. The `enrich_catalog.py`
script is a reproducible record of the enrichment logic, not an automated promoter.

**Done when:** both enriched CSVs exist; every row has a non-blank
`code_enrichment_status`; `enrich_catalog.py` exists with documented logic.

---

## Task F-6 — SoA matrix extraction

**Inputs:** F-5 activity catalog (activity ids), F-0 audit
**New / modified files:**
- `scripts/usdm_reader.py` — add `extract_soa_matrix()`
- `scripts/test_usdm_reader.py` — add tests
- `input/data/usdm-soa-matrix.csv`

### Algorithm

1. **Primary:** traverse `scheduleTimelines[*].instances[]` (`ScheduledActivityInstance`
   objects). Resolve each instance's encounter membership by following the timeline's
   `entryId` + instance `previousId` / `nextId` chain.
2. **Fallback:** if `Activity.timelineId` is set and no instance links the activity
   to a specific encounter, assign it to all encounters on that timeline.
3. **Header row:** encounter names in encounter-order (follow `nextId` chain from the
   anchor encounter where `previousId = null`).
4. **Data rows:** one per activity id from `usdm-activity-catalog.csv`; cell = `X`
   where scheduled, blank otherwise.
5. Log a WARNING (not an error) for any catalog activity that appears in zero encounters.

### Required spot-check test assertions

- Informed Consent (label "Informed consent") → `X` at Encounter_1 only
- Vital Signs and Temperature (label "Vital Signs and Temperature") → `X` at multiple encounters
- Adverse events (label "Adverse events") → `X` at multiple encounters

**Done when:** matrix CSV parseable; spot-checks pass; tests pass.

---

## Task F-7 — ProtocolDesign PlanDefinition FSH

**Inputs:** F-4 visit files (for encounter ids), F-3 `TimingResolver`
**New / modified files:**
- `scripts/usdm_reader.py` — add `emit_protocol_design()`
- `scripts/test_usdm_reader.py` — add tests
- `input/fsh/generated/usdm/ProtocolDesign.gen.fsh`

### Structure

```fsh
Instance: H2Q-MC-LZZT-ProtocolDesign-USDM
InstanceOf: SOAPlanDefinition
Usage: #definition
Title: "H2Q-MC-LZZT Protocol Design (USDM-derived)"
* status = #active
* version = "<study.versions[0].versionIdentifier>"
* action[+]   // one per encounter, in nextId-chain order
  * id          = "<encounter.name>"
  * title       = "<encounter.label>"
  * description = "<encounter.description>"
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-<encounter.name>-USDM"
  * extension[soaTimepoint] ...    // same values as Task F-4
  * relatedAction[+] ...           // same pattern as Task F-4
  * action[+]                      // transition sub-action
      * extension[soaTransition] ...
```

Encounter order is determined by following the `nextId` linked list starting from the
encounter where `previousId = null`.

**Done when:** all 12+ encounters present as ordered actions; timing values match F-4
spot-checks; `sushi .` 0 errors; tests pass.

---

## Task F-8 — Orchestration script `usdm_to_soa.py`

**Inputs:** all functions in `usdm_reader.py` (F-1 through F-7)
**New files:**
- `scripts/usdm_to_soa.py`
- `scripts/test_usdm_reader.py` — add integration test

### CLI

```
python3 scripts/usdm_to_soa.py <path-to-usdm.json>
```

Exit 0 on success (unclassified activity warnings are logged but do not fail the run).
Exit 1 with a clear message on: unresolved `id` reference, unresolvable `scheduledAtId`.

### Execution order

1. Load + index USDM via `USDMDoc`
2. Build `TimingResolver`
3. `emit_research_study()` → `input/fsh/generated/usdm/ResearchStudy.gen.fsh`
4. `emit_eligibility_groups()` → `input/fsh/generated/usdm/Eligibility.gen.fsh`
5. `emit_visit_plan_definitions()` → `input/fsh/generated/usdm/visits/*.gen.fsh`
6. `emit_protocol_design()` → `input/fsh/generated/usdm/ProtocolDesign.gen.fsh`
7. `extract_activity_catalog()` → `input/data/usdm-activity-catalog.csv`
8. `extract_observation_catalog()` → `input/data/usdm-observation-catalog.csv`
9. `extract_soa_matrix()` → `input/data/usdm-soa-matrix.csv`

All output directories are created if they do not exist.

### Integration test

- Runs the full pipeline against the real USDM file
- Asserts all expected output files exist and are non-empty
- Runs twice and asserts byte-identical output (idempotency)

**Done when:** single command regenerates all outputs; integration test passes;
`sushi .` 0 errors.

---

## Task F-9 — Reconciliation report

**Inputs:** F-8 outputs; existing hand-authored FSH files
**New files:**
- `scripts/usdm_reconcile.py`
- `docs/superpowers/usdm-reconciliation.md`

### Three reconciliation sections

**1. Timing reconciliation** — for each encounter, compare `soaPlannedTimePoint` value
and window between the USDM-derived and hand-authored PlanDefinition. Report as a
markdown table:

| Encounter | USDM day | Hand-authored day | USDM window | Hand-authored window | Match? |
|-----------|----------|-------------------|-------------|----------------------|--------|

**2. Activity reconciliation** — compare `usdm-activity-catalog.csv` ids against the
live `activity-catalog.csv`. Report: Matched / USDM-only / Hand-authored-only.

**3. Schedule reconciliation** — compare `usdm-soa-matrix.csv` assignments against the
current hand-authored visit FSH `definitionUri` / `definitionCanonical` action refs.
Report any cell where USDM and hand-authored disagree.

The script does **not** resolve discrepancies — it surfaces them for human review.

**Done when:** report generated; all 12+ encounters covered; all activities classified.

---

## Task F-10 — IG documentation

**Inputs:** F-9 report
**Modified files:**
- `input/pagecontent/usdm.md` — new page
- `sushi-config.yaml` — add page to navigation
- `input/pagecontent/developer.md` — add USDM pipeline step

### `usdm.md` content outline

1. What is the USDM file?
2. Relationship to hand-authored resources (`-USDM` id suffix; coexistence during transition)
3. Activity archetypes — measurement / instrument / procedure; PRO vs clinician-rated
   via `respondent_type`
4. Code enrichment — role of MCP at authoring time; SNOMED and CPT as supplementary
   `ActivityDefinition.code.coding[]` entries
5. Regenerating resources — `python3 scripts/usdm_to_soa.py input/usdm/...`
6. Known gaps — drawn from F-0 audit and F-9 reconciliation report

### `developer.md` addition

Add a "USDM transform" section after the existing catalog/generation instructions:

```markdown
## USDM transform (Phase F)

To regenerate all USDM-derived FSH and catalog CSVs:

    python3 scripts/usdm_to_soa.py input/usdm/CDISC_Pilot_Study_v4_FIXED.json

Then rerun sushi:

    sushi .

The `usdm-*` catalog files are USDM extracts for review only. To promote codes into
the live pipeline, manually merge reviewed entries into `activity-catalog.csv` and
`observation-catalog.csv`.
```

**Done when:** `sushi .` builds with new page; navigation entry present; no broken links.

---

## Validation / done criteria (Phase F complete)

1. `python3 scripts/usdm_to_soa.py input/usdm/CDISC_Pilot_Study_v4_FIXED.json` exits 0
   with 0 unclassified activity errors.
2. `sushi .` builds **0 Errors** after generation.
3. All expected output files exist under `input/fsh/generated/usdm/` and
   `input/data/usdm-*.csv`.
4. Second run of `usdm_to_soa.py` produces byte-identical outputs (idempotency).
5. Timing values in generated visit PlanDefinitions match USDM `Timing` objects
   (verified by F-9; discrepancies explained in the report).
6. All 36 leaf activities classified; 0 unclassified.
7. Every instrument row in `usdm-activity-catalog.csv` has a non-blank `respondent_type`.
8. `usdm-activity-catalog-enriched.csv` has a non-blank `code_enrichment_status` for
   every row.
9. `python3 -m unittest discover scripts/` passes with 0 failures.
10. `docs/superpowers/usdm-reconciliation.md` exists and covers all 3 sections.
11. Published IG includes the `usdm.md` page with no broken links.

---

## Risks

| Risk | Mitigation |
|------|------------|
| `ScheduledActivityInstance` linkage incomplete for some activities | Fallback to `Activity.timelineId`; remaining unlinked activities logged as warnings |
| No profile element for encounter contact mode | F-0 audit flags it; `action.code` used as workaround with a FSH comment noting the gap |
| MCP returns a poor top hit for some activities | `code_enrichment_status = manual` flags for human review; pipeline is unblocked |
| `-USDM` id suffix conflicts with sushi-config resource groups | Agent checks `sushi-config.yaml`; adds generated resources to a new `H2Q-MC-LZZT-USDM` group or marks them `omit` |
| Timing discrepancies between USDM and hand-authored FSH | Surfaced in F-9; USDM is authoritative; hand-authored values are reference only |
