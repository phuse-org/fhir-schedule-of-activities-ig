# USDM Transform (Phase F)

The IG includes a re-runnable Python pipeline that reads the CDISC Unified Study
Definitions Model (USDM) JSON for the H2Q-MC-LZZT study and emits FHIR Shorthand
and catalog CSVs consumed by the existing generation pipeline.

## What is the USDM file?

`input/usdm/CDISC_Pilot_Study_v4_FIXED.json` is a CDISC USDM v4 representation of
the H2Q-MC-LZZT (CDISC Pilot) study. It encodes the full study structure — encounters,
activities, timing, eligibility criteria, and schedule — in a vendor-neutral
machine-readable format.

## Relationship to hand-authored resources

Generated resources carry a `-USDM` id suffix (e.g. `H2Q-MC-LZZT-E4-USDM`) so they
coexist with hand-authored equivalents during the migration period. Hand-authored files
remain in `input/fsh/` as reference; generated files live under
`input/fsh/generated/usdm/` and carry a `// DO NOT EDIT` header.

| Hand-authored | USDM-generated equivalent |
|---|---|
| `H2Q-MC-LZZT-ProtocolDesign.fsh` | `input/fsh/generated/usdm/ProtocolDesign.gen.fsh` |
| `H2Q-MC-LZZT-Visit-N.fsh` | `input/fsh/generated/usdm/visits/E<N>.gen.fsh` |
| `H2Q-MC-LZZT-ResearchStudy-*.fsh` | `input/fsh/generated/usdm/ResearchStudy.gen.fsh` |
| `H2Q-MC-LZZT-ResearchStudy-Eligibility.fsh` | `input/fsh/generated/usdm/Eligibility.gen.fsh` |

## Activity archetypes

Each USDM `Activity` is classified using the following decision tree:

| Condition | Archetype | FHIR resources |
|---|---|---|
| Has `biomedicalConceptIds` | `measurement` | `ActivityDefinition` + `ObservationDefinition` |
| Has `bcSurrogateIds` | `instrument` | `Questionnaire` shell + scored `ObservationDefinition` |
| Has `definedProcedures[0].code` | `procedure` | `ActivityDefinition` (no result requirement) |
| None of the above | WARNING — skipped | — |

When both `biomedicalConceptIds` and `definedProcedures` are present, `biomedicalConceptIds`
takes precedence.

### PRO vs clinician-rated instruments

The USDM `BiomedicalConceptSurrogate` carries no machine-readable PRO/ClinRO flag.
Respondent type is encoded in a `respondent_type` column in the activity catalog
and drives `action.participant[+].type` in the visit action:

| Activity | respondent_type |
|---|---|
| ADAS-Cog, CIBIC+, MMSE, Hachinski, Demographics | `practitioner` |
| DAD, NPI-X | `related-person` |
| Placebo TTS test, TTS Acceptability Survey | `patient` |

## Code enrichment

USDM codes (CDISC codes) are the **primary codes** in the activity catalog.
Supplementary SNOMED and CPT codes are recorded in separate columns
(`snomed_code`, `cpt_code`) via a one-shot MCP enrichment step and are never
auto-promoted. Human review is required before codes enter the live catalog.

`code_enrichment_status` values:
- `confirmed` — existing USDM code verified against MCP top hit
- `supplemented` — USDM had a code; MCP adds a code from a different system
- `enriched` — USDM had no code; MCP found a clean match
- `manual` — no clean MCP hit; human must supply or verify
- `skipped` — administrative activity; no clinical code expected

## Regenerating resources

To regenerate all USDM-derived FSH and catalog CSVs from the USDM source:

    python3 scripts/usdm_to_soa.py input/usdm/CDISC_Pilot_Study_v4_FIXED.json

Then recompile with SUSHI:

    sushi .

The script is idempotent — running it twice on unchanged input produces
byte-identical outputs. All generated FSH carries a `// DO NOT EDIT` header.

To regenerate the reconciliation report:

    python3 scripts/usdm_reconcile.py

## Known gaps

The following USDM constructs have no direct mapping in the current SoA profiles:

| USDM concept | Disposition |
|---|---|
| `encounter.contactModes[]` (IN PERSON, TELEPHONE CALL) | Encoded as `action.code` with CDISC codes; flagged in FSH comment. Profile gap — propose `soaContactMode` sub-extension in future version. |
| ET (Early Termination) encounter | No `Encounter` object in USDM; synthesized from `ScheduleTimeline_2`. |
| RT (Retreatment) encounter | No USDM data; kept as hand-authored only. |
| `ScheduledDecisionInstance` | Skipped in timeline traversal; NPI-X at Week 16 is captured via SAI_20. |
| `StudyEpoch` chain | Dropped from FSH; documented in `ResearchStudy.description`. |
| Intra-visit sub-timings (Timing_17–24) | Out of scope for Phase F; belong in sub-PlanDefinitions. |

See [`docs/superpowers/usdm-reconciliation.md`](../docs/superpowers/usdm-reconciliation.md)
for a full reconciliation comparing USDM-derived and hand-authored values.

## Mapping methodology

For the underlying mapping rules, algorithms, and profile conformance targets — written
as a stack-independent reference for anyone implementing a similar transform — see
[USDM to FHIR SoA Mapping](usdm-mapping.html).
