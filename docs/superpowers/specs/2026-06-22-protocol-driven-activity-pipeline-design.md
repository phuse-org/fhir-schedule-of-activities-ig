# Protocol-Driven Activity Pipeline & Deploy Bundle — Design

- **Date:** 2026-06-22
- **Status:** Approved (pending spec review)
- **Branch:** feat/r6
- **IG:** ScheduleOfActivityIG (`fhir.example.brandr.soa`), FHIR R6 `6.0.0-ballot3`, SUSHI 3.20.0
- **Builds on:** [2026-06-19-vital-signs-activitydefinition-template-design.md](2026-06-19-vital-signs-activitydefinition-template-design.md) (the two activity archetypes and the CSV generator this extends).

## Problem

The IG now has two proven activity archetypes (measurement → `ActivityDefinition` +
`ObservationDefinition`; instrument → `Questionnaire` attached via
`action.definitionCanonical`) and a small CSV-driven generator covering the Vital Signs
family plus one PRO exemplar. The remaining ~40 study activities are still hand-authored
stubs, the visit→activity wiring is hand-maintained, and there is no deployable artifact
for pushing the model into a FHIR EHR server.

We want a **re-runnable pipeline** that reads the protocol structure, builds out **all**
activities (each is measurement or instrument), regenerates the visit→activity wiring,
and produces a **transaction Bundle** for deployment. Editing the protocol or the
schedule and rerunning should regenerate the resources.

## Goals

1. Enumerate every study activity by traversing `ProtocolDesign → visit PlanDefinitions`
   and build out each as the correct archetype.
2. Make generation **re-runnable and idempotent**: edit the schedule/catalog, rerun,
   get updated resources.
3. The pipeline **owns the visit activity-action wiring** (correct `definitionUri` for
   measurements, `definitionCanonical` for instruments).
4. Produce a deployable **transaction Bundle** (PUT-by-id upsert) of all definitional
   resources for a FHIR EHR server.
5. Keep the FSH authoring flow: generated FSH is compiled by SUSHI into the IG; the
   Bundle is a separate deploy artifact.

## Non-goals

- Authoring full instrument **item sets** (ADAS-Cog/MMSE/etc. questions). The pipeline
  emits coded, attached, deployable **Questionnaire shells**; full items are per-instrument
  follow-up.
- Generating visit **timing / relatedAction structure / SOA extensions / Visit-Date**
  actions — these stay hand-authored in the visit files.
- Calling the healthcare MCP at pipeline runtime — the MCP is an **authoring aid** used to
  enrich the catalog; codes are baked in and the Python generator stays offline.
- Aligning the model to CDISC **USDM** (see Future).

## Architecture & data flow

```
INPUTS (editable)                    PIPELINE (python3, stdlib)            OUTPUTS
ProtocolDesign.fsh ─┐                1. sushi build → fsh-generated JSON
visit PlanDefs ─────┤── sushi ──→     2. traverse protocol→visits          → input/fsh/generated/*.gen.fsh
 (skeleton only)    │                   → enumerate activity refs            (ADs, ObsDefs, Questionnaire
activity-catalog.csv ─────────────┐  3. join to catalog (archetype+codes)    shells, per-visit activity
soa-matrix.csv (visit×activity) ──┘  4. emit activity resources +            actions)
                                        visit activity-action blocks
                                     5. rebuild, then assemble Bundle ─────→ dist/soa-deploy-bundle.json
```

The pipeline reads **compiled FHIR JSON** from `fsh-generated/resources/` (already parsed
by SUSHI — robust), never raw FSH. Two new editable inputs join with the protocol graph:
the **catalog** (per-activity content) and the **SoA matrix** (visit×activity schedule).

### Components (each independently testable)

| Unit | Responsibility | Input → Output |
|---|---|---|
| `protocol_graph.py` | Traverse compiled ProtocolDesign + visit PlanDefs, **recursing through grouping PlanDefinitions** (e.g. `Vital-Signs-Height-PD`) to reach leaf activity refs; return the ordered visit list and the set of (visit, activity-ref, ref-kind) tuples, where ref-kind ∈ {`ActivityDefinition`, `Questionnaire`, `PlanDefinition`}. | `fsh-generated/resources/*.json` → graph dict |
| `catalog.py` | Load + validate `activity-catalog.csv`; key by activity id/OID; expose archetype + codes. | CSV → dict |
| `matrix.py` | Load `soa-matrix.csv`; bootstrap-extract it from compiled visits when absent. | CSV (or compiled visits) → visit×activity |
| `render.py` | Render measurement AD+ObsDef, instrument Questionnaire-shell+scored ObsDef, and visit activity-action blocks (reuses existing RuleSets). | row+matrix → FSH |
| `gen_activities.py` (extended) | Orchestrate: graph ∩ matrix ∩ catalog → write `*.gen.fsh`. Idempotent. | all of the above → files |
| `build_bundle.py` | Filter compiled resources to definitional kinds; assemble transaction Bundle (PUT-by-id). | `fsh-generated/resources/*.json` → `dist/soa-deploy-bundle.json` |

## The two editable sources

### `input/data/activity-catalog.csv`

One row per activity. Columns:
`id, oid, oidsys, title, archetype, code_system, code, code_display, unit, obsdef_id, questionnaire_id`.

- `archetype` ∈ {`measurement`, `instrument`}.
- Measurement rows carry LOINC `code` + UCUM `unit` + `obsdef_id`.
- Instrument rows carry an instrument `code` (LOINC survey/SNOMED assessment) + `questionnaire_id`.
- Replaces today's `measurement-activities.csv` + `instrument-activities.csv` (migrated in).
- Codes enriched during authoring via the healthcare MCP (`search_clinical_concepts`
  `sources:["LNC"]` for LOINC, `lookup_icd_code`, UMLS CUI lookups). The MCP returns CUIs +
  long names; the exact code is resolved and **baked into the CSV** — no runtime MCP call.

### `input/data/soa-matrix.csv`

Rows = activity ids, columns = visit ids, cell = `X` when the activity occurs at that
visit (optional `@anchor-id` in a cell to set that action's `relatedAction.targetId`;
default anchor is the visit's hand-authored anchor convention).

- **Bootstrapped once** by `matrix.py` extracting (visit, activity) pairs from the current
  compiled visit PlanDefinitions, so no scheduling information is lost in the transition.
- Thereafter it is the editable schedule of activities; editing a cell + rerunning
  adds/removes that activity from that visit.

## Generation behavior

- **Measurement** → full `ActivityDefinition` (conforms to `StudyActivitySoa`,
  `kind=#ServiceRequest`, `intent=#plan`, LOINC `code`, `participant`) + result
  `ObservationDefinition` (`permittedDataType`, `permittedUnit`, `preferredReportName`).
  Visit action uses `definitionUri = "ActivityDefinition/<id>"`. (Reuses the existing
  `VitalSignActivity`/`VitalSignObservation` RuleSets.)
- **Instrument** → `Questionnaire` **shell**: `status`, ODM `FormDef` identifier, `code`,
  `subjectType = #Patient`, SDC `itemExtractionContext` extension → a scored
  `ObservationDefinition`. Visit action uses
  `definitionCanonical = Canonical(<questionnaire_id>)`. Item authoring is out of scope.
- **Visit activity-actions:** for each visit the pipeline writes
  `input/fsh/generated/visits/<Visit>.actions.gen.fsh` defining a
  `RuleSet: <Visit>Actions` whose body is the activity-action lines from `matrix ∩ catalog`
  (correct `definitionUri`/`definitionCanonical` + title + `relatedAction` anchor). The
  hand-authored visit instance keeps identifiers, status, the Visit-Date action, timing,
  and SOA extensions, and applies the generated block with a single
  `* insert <Visit>Actions`. (Grouping PlanDefinitions like `Vital-Signs-Height-PD` are
  preserved; a visit cell may reference a grouping PD instead of a leaf activity.)
- **Stub retirement:** the ~30 hand-authored stub `ActivityDefinition`s in
  `StudyActivities.fsh` are removed as the catalog takes over (same id, single source).

## Deploy Bundle & usage sweep

- `scripts/build_bundle.py` reads `fsh-generated/resources/*.json`, keeps **definitional**
  resource types (`ResearchStudy`, `PlanDefinition`, `ActivityDefinition`, `Questionnaire`,
  `ObservationDefinition`), and emits a `Bundle`:
  - `type = transaction`
  - one entry per resource: `fullUrl` = the resource's canonical `url` (or
    `urn:uuid` fallback), `request.method = PUT`, `request.url = "<ResourceType>/<id>"`.
  - POSTing the Bundle to `[base]` upserts every resource idempotently.
  - Output: `dist/soa-deploy-bundle.json` (a standalone deploy artifact, **not** compiled
    into the IG).
- **Usage sweep:** generated and hand-authored definitional resources switch
  `Usage:#example → #definition`, so SUSHI assigns canonical `url`s and renders them as
  definitions (not examples). This is a **broad change**; acceptance requires the IG still
  builds **0 errors**. Resources that are genuinely examples (sample data instances, if any)
  stay `#example` and are excluded from the Bundle.

## Re-run workflow

`scripts/build-soa.sh` runs the full loop:
1. `sushi .` (compile current sources)
2. `python3 scripts/gen-activities.py` (regen activity resources + visit actions from
   protocol ∩ matrix ∩ catalog)
3. `sushi .` (compile the regenerated FSH)
4. `python3 scripts/build_bundle.py` (assemble the deploy Bundle from compiled resources)

All generated files carry a `DO NOT EDIT` header and are byte-idempotent on unchanged
inputs.

## Validation / done criteria

1. `sushi .` builds with **0 Errors** after generation.
2. Every activity referenced by a visit resolves to a generated resource of the correct
   archetype; no stub ActivityDefinitions remain for catalogued activities.
3. Instrument visit actions serialize `definitionCanonical`; measurement visit actions
   serialize `definitionUri`.
4. `gen-activities.py` and `build_bundle.py` are idempotent (rerun ⇒ byte-identical output).
5. `dist/soa-deploy-bundle.json` is a valid `transaction` Bundle whose entries are
   PUT-by-id and whose count equals the definitional-resource count.
6. Bootstrapping `soa-matrix.csv` from the current visits reproduces today's visit→activity
   assignments (no schedule drift) before any manual edits.
7. Generator unit tests (stdlib `unittest`) cover protocol traversal, catalog join,
   archetype dispatch, matrix bootstrap, and Bundle assembly.

## Risks

- **Usage sweep breadth** — flipping many resources to `#definition` may surface new
  validation; mitigated by an incremental phase that re-checks 0 errors after each batch.
- **Instrument shells without items** — deployable but clinically incomplete; explicitly
  scoped and documented so consumers know items are pending.
- **Matrix/catalog drift** — an activity in the matrix but missing from the catalog (or
  vice-versa) must be a hard, clear pipeline error, not a silent skip.

## Implementation phasing

Cohesive but large; the plan will sequence:
- **A. Catalog scale-up** — one `activity-catalog.csv` for all ~40 activities, archetype
  classified, codes MCP-enriched; migrate the two existing CSVs in.
- **B. Protocol traversal + SoA-matrix bootstrap** — `protocol_graph.py`, `matrix.py`,
  bootstrap from compiled visits, verify no drift.
- **C. Generate activity resources + visit activity-actions** — extend the generator;
  retire stubs; visits `insert` generated actions.
- **D. Usage sweep** — flip definitional resources to `#definition`, keep 0 errors.
- **E. Deploy Bundle** — `build_bundle.py` + `build-soa.sh` + docs.

Each phase ends green-and-testable.

## Future: USDM alignment

A later effort will align this model with the CDISC **Unified Study Definitions Model
(USDM)**. The catalog and SoA matrix are deliberately the kind of tabular,
structure-vs-content split that maps onto USDM entities — `StudyDesign`,
`ScheduleTimeline`, `ScheduledActivityInstance`, `Activity`, and `BiomedicalConcept`
(which corresponds closely to our coded measurement/instrument catalog rows). Keeping the
clinical content in a catalog (not buried in FSH) makes a future USDM import/export layer
tractable. Out of scope for this pass; noted so the data shapes don't paint us into a
corner.
