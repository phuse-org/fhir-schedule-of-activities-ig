# Task F-0 — USDM Mapping Audit

- **Date:** 2026-06-30
- **Status:** Complete
- **Source:** `input/usdm/CDISC_Pilot_Study_v4_FIXED.json` (CDISC Pilot Study H2Q-MC-LZZT, USDM v4)
- **USDM system:** CDISC USDM E2J v0.62.0
- **Feeds:** Tasks F-1 through F-7

---

## Section 1 — USDM instanceType Inventory

Total objects with an `instanceType` field: **1,966**

| instanceType | Count | Notes |
|---|---|---|
| Code | 711 | Coded values throughout; every AliasCode.standardCode is a Code |
| AliasCode | 259 | Wrapper around Code with optional aliases; used for BC codes, timing, etc. |
| ResponseCode | 226 | Enumerated response values on BiomedicalConceptProperty |
| BiomedicalConceptProperty | 186 | CDASH/SDTM variable-level properties on each BC |
| NarrativeContentItem | 85 | Leaf text nodes inside NarrativeContent sections |
| NarrativeContent | 83 | Protocol narrative sections (background, objectives, etc.) |
| BiomedicalConcept | 40 | Clinical measurement / observation concepts |
| Activity | 40 | Leaf activities in the SoA matrix |
| EligibilityCriterionItem | 31 | Sub-items within each EligibilityCriterion |
| EligibilityCriterion | 31 | Inclusion/exclusion criteria (8 inclusion, 23 exclusion) |
| Timing | 25 | Timing objects referenced by encounters and SAIs |
| ScheduledActivityInstance | 24 | Nodes in the schedule timeline linked lists |
| Quantity | 22 | Numeric values with optional units |
| TransitionRule | 15 | Start/end rules for timeline transitions |
| StudyCell | 15 | Arm × epoch matrix cells |
| Procedure | 15 | Coded procedures on Activity.definedProcedures |
| Encounter | 12 | Study visits (no ET or RT encounter in USDM — see Section 5) |
| Endpoint | 11 | Study endpoints linked to objectives |
| Abbreviation | 11 | Protocol abbreviation definitions |
| StudyElement | 7 | Treatment elements within study cells |
| Objective | 6 | Study objectives (1 primary, 5 secondary) |
| GeographicScope | 6 | Geographic applicability scopes |
| StudyEpoch | 5 | Screening, Treatment 1–3, Follow-Up |
| ParameterMap | 5 | Template parameter mappings |
| Duration | 5 | Duration values |
| BiomedicalConceptSurrogate | 5 | Instrument surrogates (no BC code; used for questionnaires) |
| ScheduleTimelineExit | 4 | Exit conditions from timelines |
| ScheduleTimeline | 4 | Timeline containers (Main, AE, ET, VS-BP) |
| GovernanceDate | 4 | Protocol governance dates |
| BiomedicalConceptCategory | 4 | BC groupings (Vital Signs, Chemistry, Urinalysis, Hematology) |
| Administration | 4 | Drug administration records |
| StudyTitle | 3 | Study title variants |
| StudyIntervention | 3 | Intervention definitions |
| StudyArm | 3 | Placebo, Low Dose, High Dose |
| Range | 3 | Range values |
| Organization | 3 | Sponsor (Lilly), Registry (CT.gov), Site |
| Address | 3 | Organization addresses |
| SyntaxTemplateDictionary | 2 | Template dictionaries |
| Substance | 2 | Drug substances |
| StudyRole | 2 | Sponsor role, Investigator role |
| StudyIdentifier | 2 | H2Q-MC-LZZT (sponsor) + NCT12345678 (registry) |
| StudyDefinitionDocumentVersion | 2 | Document versions (Lilly template, M11 template) |
| StudyDefinitionDocument | 2 | Protocol documents |
| StudyCohort | 2 | Study cohorts |
| StudyAmendmentReason | 2 | Amendment reasons |
| Strength | 2 | Drug strengths |
| Masking | 2 | Blinding/masking records |
| Indication | 2 | ICD-10 + SNOMED Alzheimer's codes |
| DocumentContentReference | 2 | Amendment section references |
| Condition | 2 | Conditional scheduling rules (HbA1c, practice-only) |
| SubjectEnrollment | 1 | Enrollment quantity record |
| StudyVersion | 1 | Version 2 of the study |
| StudySite | 1 | Single study site |
| StudyDesignPopulation | 1 | Population definition |
| StudyChange | 1 | Amendment change record |
| StudyAmendmentImpact | 1 | Amendment impact record |
| StudyAmendment | 1 | Amendment 1 |
| Study | 1 | Root study object |
| ScheduledDecisionInstance | 1 | Decision node at Week 16 (NPI branching) |
| ReferenceIdentifier | 1 | External reference identifier |
| ProductOrganizationRole | 1 | Product/org role |
| PersonName | 1 | Investigator name |
| InterventionalStudyDesign | 1 | Study design root |
| IntercurrentEvent | 1 | Intercurrent event definition |
| Ingredient | 1 | Drug ingredient |
| Estimand | 1 | Estimand definition |
| ConditionAssignment | 1 | Arm assignment condition |
| AssignedPerson | 1 | Investigator person record |
| AnalysisPopulation | 1 | Analysis population |
| AdministrableProductProperty | 1 | Administrable product property |
| AdministrableProduct | 1 | Administrable product |

**Key counts for downstream tasks:**
- 12 Encounters (all IN PERSON; 4 also have TELEPHONE CALL mode)
- 40 Activities (leaf nodes)
- 5 BiomedicalConceptSurrogates (instruments)
- 40 BiomedicalConcepts (measurements)
- 31 EligibilityCriteria (8 inclusion, 23 exclusion)
- 25 Timing objects (16 encounter-level + 8 intra-visit sub-timings + 1 decision node)
- 4 ScheduleTimelines (Main, AE, ET, VS-BP)
- 24 ScheduledActivityInstances + 1 ScheduledDecisionInstance

---

## Section 2 — Field-Level Mapping Table

### 2.1 Study / ResearchStudy

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `study.name` | ResearchStudy | `title` | "CDISC PILOT - LZZT" |
| `study.versions[0].versionIdentifier` | ResearchStudy | `version` | "2" |
| `study.versions[0].studyIdentifiers[0].text` | ResearchStudy | `identifier[0].value` | "H2Q-MC-LZZT"; scopeId → Organization_1 (Sponsor) |
| `study.versions[0].studyIdentifiers[1].text` | ResearchStudy | `identifier[1].value` | "NCT12345678"; scopeId → Organization_2 (Registry) |
| `study.versions[0].studyIdentifiers[].scopeId` | ResearchStudy | `identifier[].assigner` | Resolve scopeId → Organization; use org type to set identifier.type |
| `studyDesigns[0].studyPhase.standardCode` | ResearchStudy | `phase` | Code C15601 "Phase II Trial" → FHIR `#phase-2` |
| `studyDesigns[0].indications[0].codes[0]` | ResearchStudy | `condition[0]` | G30.9 / ICD-10-CM "Alzheimer's disease, unspecified" |
| `studyDesigns[0].indications[1].codes[0]` | ResearchStudy | `condition[1]` | 26929004 / SNOMED "Alzheimer's disease" |
| `studyDesigns[0].therapeuticAreas[]` | ResearchStudy | `focus[]` | MILD_MOD_ALZ (sponsor) + 26929004 (SNOMED) |
| `studyDesigns[0].arms[0].name/label/description` | ResearchStudy | `comparisonGroup[0].name/description` | "Placebo" |
| `studyDesigns[0].arms[0].type.standardCode` | ResearchStudy | `comparisonGroup[0].type` | C174268 "Placebo Control Arm" |
| `studyDesigns[0].arms[1].name/label/description` | ResearchStudy | `comparisonGroup[1].name/description` | "Xanomeline Low Dose" |
| `studyDesigns[0].arms[1].type.standardCode` | ResearchStudy | `comparisonGroup[1].type` | C174267 "Active Comparator Arm" |
| `studyDesigns[0].arms[2].name/label/description` | ResearchStudy | `comparisonGroup[2].name/description` | "Xanomeline High Dose" |
| `studyDesigns[0].arms[2].type.standardCode` | ResearchStudy | `comparisonGroup[2].type` | C174267 "Active Comparator Arm" |
| `studyDesigns[0].objectives[0].level.standardCode` | ResearchStudy | `objective[0].type` | C85826 "Study Primary Objective" → `#primary` |
| `studyDesigns[0].objectives[0].endpoints[].text` | ResearchStudy | `objective[0].description` | ADAS-Cog / CIBIC+ dose-response |
| `studyDesigns[0].objectives[1..5].level.standardCode` | ResearchStudy | `objective[1..5].type` | C85827 "Study Secondary Objective" → `#secondary` |
| `studyDesigns[0].epochs[]` | ResearchStudy | (extension or note) | 5 epochs: Screening, Treatment 1–3, Follow-Up; no direct FHIR R6 element; document in description or custom extension |

### 2.2 Organization

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `organizations[0].id` | Organization | `id` | "Organization_1" → slug "LILLY" |
| `organizations[0].name` | Organization | `name` | "LILLY" |
| `organizations[0].label` | Organization | `alias[]` | "Eli Lilly" |
| `organizations[0].type.standardCode` | Organization | `type[0]` | C70793 "Sponsor" |
| `organizations[0].identifiers[0].text` | Organization | `identifier[0].value` | DUNS "00-642-1325" |
| `organizations[1].name` | Organization | `name` | "CT-GOV" |
| `organizations[1].type.standardCode` | Organization | `type[0]` | C93453 "Study Registry" |
| `organizations[2].name` | Organization | `name` | "SITE_ORG_1" |
| `organizations[2].label` | Organization | `alias[]` | "Big Hospital" |
| `study.versions[0].studyIdentifiers[0].scopeId` | ResearchStudy | `sponsor` | Reference(Organization/LILLY) |

### 2.3 Practitioner / Person

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `studyDesigns[0].studyRoles[].assignedPersons[0]` | Practitioner | `id` | AssignedPerson_1 → "Pers_001" |
| `assignedPerson.personName.text` | Practitioner | `name[0].text` | "Mr. X" |
| `assignedPerson.personName.familyName` | Practitioner | `name[0].family` | "X" |
| `assignedPerson.personName.givenNames[]` | Practitioner | `name[0].given[]` | ["Ab", "Theo"] |
| `assignedPerson.jobTitle` | Practitioner | `qualification[0].code.text` | "Physician" |
| `studyRole.type` (Investigator) | ResearchStudy | `principalInvestigator` | Reference(Practitioner/Pers_001) |

> **Note:** There is no top-level `persons[]` array in this USDM file. Person data lives only within `StudyRole.assignedPersons`. The `USDMDoc.persons()` method must traverse `studyDesigns[0].studyRoles[*].assignedPersons`.

### 2.4 Eligibility Groups

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `studyDesigns[0].population.criterionIds[]` | Group | (drives which criteria to include) | 31 criterion IDs |
| `EligibilityCriterion.category.standardCode.code` | Group | `characteristic[].exclude` | C25532 → `false`; C25370 → `true` |
| `EligibilityCriterion.text` (strip HTML) | Group | `characteristic[].valueCodeableConcept.text` | Plain text after HTML stripping |
| `EligibilityCriterion.category.standardCode.code` | Group | `characteristic[].code` | `#eligibility` |

### 2.5 Encounters / Visit PlanDefinitions

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `encounter.id` | PlanDefinition | `id` (instance id suffix) | e.g. "H2Q-MC-LZZT-E1-USDM" |
| `encounter.name` | PlanDefinition | `action[0].id` | Used as action id and relatedAction targetId |
| `encounter.label` | PlanDefinition | `title` and `action[0].title` | "Screening 1", "Week 2", etc. |
| `encounter.description` | PlanDefinition | `description` and `action[0].description` | Visit description text |
| `encounter.scheduledAtId` | PlanDefinition | `action[0].extension[soaTimepoint]` | Resolve to Timing object; null → anchor visit |
| `encounter.previousId` | PlanDefinition | `action[0].relatedAction[0].targetId` | Reference to prior encounter name |
| `encounter.nextId` | (ordering) | (encounter chain order) | Used to determine encounter sequence |
| `encounter.contactModes[].code.decode` | PlanDefinition | **GAP** — see Section 5 | "IN PERSON", "TELEPHONE CALL" |

### 2.6 Timing

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `Timing.value` (ISO 8601 duration) | PlanDefinition | `action.extension[soaTimepoint].extension[soaPlannedTimePoint].valueQuantity` | Parse P\<n\>D or P\<n\>W → days; unit = "d" |
| `Timing.windowLower` | PlanDefinition | `action.extension[soaTimepoint].extension[soaPlannedRange].valueRange.low` | Parse ISO 8601 duration → days |
| `Timing.windowUpper` | PlanDefinition | `action.extension[soaTimepoint].extension[soaPlannedRange].valueRange.high` | Parse ISO 8601 duration → days |
| `Timing.relativeFromScheduledInstanceId` | PlanDefinition | `action.extension[soaTimepoint].extension[soaReferenceTimePoint].valueString` | Resolve SAI id → encounter name |

### 2.7 Activities / ActivityDefinitions

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `Activity.label` | ActivityDefinition | `title` | Human-readable label |
| `Activity.name` | ActivityDefinition | `name` | Machine name |
| `Activity.biomedicalConceptIds[]` | ActivityDefinition | `code` (from BC.code) | archetype = measurement |
| `Activity.bcSurrogateIds[]` | ActivityDefinition | `code` (blank or surrogate) | archetype = instrument → Questionnaire shell |
| `Activity.definedProcedures[0].code` | ActivityDefinition | `code` | archetype = procedure |
| `Activity.timelineId` | (SoA matrix fallback) | (assign to all encounters on that timeline) | Used when no SAI links activity to specific encounter |

### 2.8 BiomedicalConcept

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `BiomedicalConcept.code.standardCode.code` | ActivityDefinition / ObservationDefinition | `code.coding[0].code` | CDISC code (e.g. C25299 for DIABP) |
| `BiomedicalConcept.code.standardCode.codeSystem` | ActivityDefinition / ObservationDefinition | `code.coding[0].system` | "http://www.cdisc.org" |
| `BiomedicalConcept.code.standardCode.decode` | ActivityDefinition / ObservationDefinition | `code.coding[0].display` | Human-readable decode |
| `BiomedicalConceptProperty[name=VSORRES].aliasCode` | ObservationDefinition | `quantitativeDetails.unit` | Unit for result value |
| `BiomedicalConceptProperty[name=VSORRESU].responseCode[]` | ObservationDefinition | `permittedUnit[]` | Permitted units |

### 2.9 BiomedicalConceptSurrogate

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `BiomedicalConceptSurrogate.id` | Questionnaire | `id` (slugified) | e.g. "H2Q-MC-LZZT-MMSE-USDM" |
| `BiomedicalConceptSurrogate.label` | Questionnaire | `title` | "MMSE", "Hachinski Ischemic Scale", etc. |
| `BiomedicalConceptSurrogate.name` | Questionnaire | `name` | Machine name |
| (no code on surrogate) | Questionnaire | `code` | Blank; MCP enrichment (Task F-5b) may supply |

### 2.10 ScheduleTimeline / ScheduledActivityInstance (SoA Matrix)

| USDM path | FHIR resource | FHIR element | Notes |
|---|---|---|---|
| `ScheduleTimeline.mainTimeline` | (routing) | (primary vs. secondary timeline) | Main timeline drives encounter order |
| `ScheduleTimeline.entryId` | (routing) | (first SAI in chain) | Start of linked list |
| `ScheduledActivityInstance.encounterIds[]` | PlanDefinition | `action[].definitionUri` | Maps activity to encounter |
| `ScheduledActivityInstance.activityIds[]` | PlanDefinition | `action[].definitionUri` | Activities scheduled at that encounter |
| `ScheduledActivityInstance.previousId` | (ordering) | (chain traversal) | Linked list for encounter order |
| `ScheduledActivityInstance.nextId` | (ordering) | (chain traversal) | Linked list for encounter order |

---

## Section 3 — Encounter ↔ Timing Resolution Logic

### 3.1 Overview

Each `Encounter` object has a `scheduledAtId` field that either:
- Is **null** → the encounter is an **anchor visit** (no timing extension values emitted)
- Contains a **Timing object id** → resolve to a `Timing` object for planned day and window

### 3.2 Step-by-step algorithm

```
function resolve_encounter_timing(encounter, usdm_doc):

  1. If encounter.scheduledAtId is null:
       → anchor visit
       → emit soaTimepoint with soaTimePointType and soaTimePointSubType only
       → no soaPlannedTimePoint, no soaPlannedRange, no soaReferenceTimePoint
       → no relatedAction
       → return None

  2. timing = usdm_doc.resolve(encounter.scheduledAtId)
     # O(1) lookup in the flat id→object index

  3. planned_day_value = parse_iso8601_duration_to_days(timing.value)
     # See §3.3 below

  4. window_lower_days = parse_iso8601_duration_to_days(timing.windowLower)
       if timing.windowLower is not null else None
     window_upper_days = parse_iso8601_duration_to_days(timing.windowUpper)
       if timing.windowUpper is not null else None

  5. reference_encounter_name = None
     if timing.relativeFromScheduledInstanceId is not null:
       sai = usdm_doc.resolve(timing.relativeFromScheduledInstanceId)
       # sai is a ScheduledActivityInstance
       # The reference encounter is the encounter that contains this SAI
       # Look up: which encounter has this SAI in its timeline position?
       # Strategy: traverse ScheduleTimeline_4 (main timeline) instances;
       #   find the SAI whose id = timing.relativeFromScheduledInstanceId;
       #   the encounter for that SAI is the reference encounter.
       reference_encounter = usdm_doc.resolve(sai.encounterIds[0])
       reference_encounter_name = reference_encounter.name

  6. return ResolvedTiming(
       planned_day_value = planned_day_value,
       planned_day_unit  = "d",
       window_lower_days = window_lower_days,
       window_upper_days = window_upper_days,
       reference_encounter_name = reference_encounter_name
     )
```

### 3.3 ISO 8601 duration parser

The USDM uses the following duration formats in this file:

| Format | Example | Conversion |
|---|---|---|
| `P<n>D` | `P2D`, `P14D`, `P182D` | n days |
| `P<n>W` | `P2W`, `P4W`, `P26W` | n × 7 days |
| `PT<n>H` | `PT4H`, `PT0H` | n / 24 days (sub-day; used in windowLower/Upper for Timing_2) |
| `PT<n>M` | `PT0M`, `PT5M` | n / 1440 days (sub-minute; used in intra-visit VS timeline) |

**Required parser logic (stdlib only):**

```python
import re

def parse_iso8601_duration_to_days(s: str) -> float:
    if s is None:
        return None
    # Week form: P<n>W
    m = re.fullmatch(r'P(\d+(?:\.\d+)?)W', s)
    if m:
        return float(m.group(1)) * 7
    # Day form: P<n>D
    m = re.fullmatch(r'P(\d+(?:\.\d+)?)D', s)
    if m:
        return float(m.group(1))
    # Hour form: PT<n>H
    m = re.fullmatch(r'PT(\d+(?:\.\d+)?)H', s)
    if m:
        return float(m.group(1)) / 24
    # Minute form: PT<n>M
    m = re.fullmatch(r'PT(\d+(?:\.\d+)?)M', s)
    if m:
        return float(m.group(1)) / 1440
    raise ValueError(f"Unsupported ISO 8601 duration: {s!r}")
```

> **Note on sub-day timings:** `Timing_2` (Encounter_2, Screening 2) has `windowLower = PT4H` and `windowUpper = PT0H`. These are sub-day windows for the ambulatory ECG placement visit. The `soaPlannedRange` extension uses `SimpleQuantity` with unit `"d"`, so these convert to fractional days (4/24 ≈ 0.167 d, 0/24 = 0 d). The `TimingResolver` must handle this without error; the fractional values are unusual but valid.

### 3.4 Anchor visits

Two encounters have `scheduledAtId = null`:

| Encounter | Name | Label | Reason |
|---|---|---|---|
| Encounter_1 | E1 | Screening 1 | First encounter — no prior reference; anchor of the entire timeline |
| Encounter_3 | E3 | Baseline | Baseline is the treatment start anchor; `scheduledAtId = null` despite having a `previousId` |

For both: emit `soaTimepoint` with `soaTimePointType = "interaction"` and `soaTimePointSubType` only. No `soaPlannedTimePoint`, no `soaPlannedRange`, no `soaReferenceTimePoint`, no `relatedAction`.

### 3.5 relativeFromScheduledInstanceId → reference encounter

The `Timing.relativeFromScheduledInstanceId` field points to a `ScheduledActivityInstance` id. The reference encounter is the encounter that SAI belongs to. Mapping:

| Timing id | relativeFromScheduledInstanceId | Reference SAI encounter | Reference encounter name |
|---|---|---|---|
| Timing_2 | ScheduledActivityInstance_10 | Encounter_2 | E2 (Screening 2) |
| Timing_4 | ScheduledActivityInstance_12 | Encounter_4 | E4 (Week 2) |
| Timing_5 | ScheduledActivityInstance_13 | Encounter_5 | E5 (Week 4) |
| Timing_6 | ScheduledActivityInstance_14 | Encounter_6 | E7 (Week 6) |
| Timing_7 | ScheduledActivityInstance_15 | Encounter_7 | E8 (Week 8) |
| Timing_9 | ScheduledActivityInstance_17 | Encounter_8 | E9 (Week 12) |
| Timing_11 | ScheduledActivityInstance_19 | Encounter_9 | E10 (Week 16) |
| Timing_13 | ScheduledActivityInstance_21 | Encounter_10 | E11 (Week 20) |
| Timing_15 | ScheduledActivityInstance_23 | Encounter_11 | E12 (Week 24) |
| Timing_16 | ScheduledActivityInstance_24 | Encounter_12 | E13 (Week 26) |

> **Implementation note:** The `relativeFromScheduledInstanceId` on a Timing object points to the SAI that *uses* that timing — i.e., the SAI for the encounter being scheduled, not the reference encounter. The reference encounter is the *previous* encounter in the chain (the one the timing is measured from). The `TimingResolver` must follow the SAI's `previousId` chain or use `encounter.previousId` to find the reference. Specifically: `encounter.previousId` gives the reference encounter id directly.

---

## Section 4 — Visit × Activity Schedule Encoding

### 4.1 Primary mechanism: ScheduledActivityInstance

The main schedule is encoded in **ScheduleTimeline_4** (Main Timeline, `mainTimeline = true`). Each `ScheduledActivityInstance` (SAI) node in this timeline has:
- `encounterIds[]` — which encounter(s) this node belongs to
- `activityIds[]` — which activities are scheduled at this node

The SAI nodes form a **singly-linked list** via `previousId` / `nextId`. The chain starts at `ScheduleTimeline_4.entryId = ScheduledActivityInstance_9`.

**Encounter order** (following `nextId` chain from anchor):

```
SAI_9 (Encounter_1: Screening 1)
  → SAI_10 (Encounter_2: Screening 2)
    → SAI_11 (Encounter_3: Baseline)
      → SAI_12 (Encounter_4: Week 2)
        → SAI_13 (Encounter_5: Week 4)
          → SAI_14 (Encounter_6: Week 6)
            → SAI_15 (Encounter_7: Week 8)
              → SAI_16 (Encounter_7: Week 8 — NPI sub-node)
                → SAI_17 (Encounter_8: Week 12)
                  → SAI_18 (Encounter_8: Week 12 — NPI sub-node)
                    → SAI_19 (Encounter_9: Week 16)
                      → ScheduledDecisionInstance_1 (decision node)
                        → SAI_20 (Encounter_9: Week 16 — NPI sub-node)
                          → SAI_21 (Encounter_10: Week 20)
                            → SAI_22 (Encounter_10: Week 20 — NPI sub-node)
                              → SAI_23 (Encounter_11: Week 24)
                                → SAI_24 (Encounter_12: Week 26)
```

> **Note:** Multiple SAI nodes can map to the same encounter (e.g., SAI_15 and SAI_16 both map to Encounter_7). The SoA matrix must union the `activityIds` from all SAI nodes for a given encounter.

### 4.2 Fallback mechanism: Activity.timelineId

Two activities have a `timelineId` set:
- **Activity_13** (Vital Signs and Temperature): `timelineId = ScheduleTimeline_3`
- **Activity_32** (Check adverse events): `timelineId = ScheduleTimeline_1`
- **Activity_32b** (Vital Signs Supine/Standing): `timelineId = ScheduleTimeline_3`

These activities are also referenced in specific SAI `activityIds` lists, so the fallback is not needed for them in this file. However, the `extract_soa_matrix()` function should implement the fallback per the spec: if an activity has `timelineId` set and no SAI links it to a specific encounter, assign it to all encounters on that timeline.

### 4.3 Secondary timelines

| Timeline | mainTimeline | Purpose | Encounters |
|---|---|---|---|
| ScheduleTimeline_1 | false | Adverse Event | No encounter (null encounterIds) — triggered by AE |
| ScheduleTimeline_2 | false | Early Termination | No encounter (null encounterIds) — triggered by early exit |
| ScheduleTimeline_3 | false | Vital Signs BP Protocol | No encounter (null encounterIds) — sub-procedure sequence |
| ScheduleTimeline_4 | true | Main Study Timeline | All 12 encounters |

> **Important:** The ET (Early Termination) and RT (Retreatment) encounters present in the hand-authored FSH (`H2Q-MC-LZZT-Study-ET-14`, `H2Q-MC-LZZT-Study-RT-15`) have **no corresponding Encounter objects in the USDM**. The ET activities are in ScheduleTimeline_2 (SAI_2) with `encounterIds = null`. There is no RT encounter or timeline in the USDM at all. See Section 5 (Gaps) for disposition.

### 4.4 Activity-to-encounter spot check

**Encounter_1 (Screening 1) — SAI_9:**
Activities: Informed consent, Inclusion/exclusion criteria, Patient number assigned, Demographics (BC_20/21 + BCSurr_1), Hachinski (BCSurr_2), MMSE (BCSurr_3), Physical examination, Medical history, Habits (Alcohol/Caffeine), Chest X-ray, Apo E genotyping, Vital Signs and Temperature, ECG, Placebo TTS test, CT scan, Concomitant medications, Hematology, Chemistry, Urinalysis, Hemoglobin A1C (conditional), ADAS-Cog (practice), CIBIC+ (practice), DAD (practice), NPI-X (practice)

**Encounter_2 (Screening 2) — SAI_10:**
Activities: Vital Signs and Temperature, Ambulatory ECG placed

**Encounter_3 (Baseline) — SAI_11:**
Activities: Patient randomised, Vital Signs and Temperature, Ambulatory ECG removed, Concomitant medications, Plasma Specimen (Xanomeline), Study drug record, ADAS-Cog, CIBIC+, DAD, NPI-X

**Encounter_4 (Week 2) — SAI_12:**
Activities: Apo E genotyping, Vital Signs and Temperature, ECG, Concomitant medications, Hematology, Chemistry, Plasma Specimen, Study drug record, NPI-X

**Encounter_7 (Week 8) — SAI_15 + SAI_16:**
Activities (SAI_15): Vital Signs and Temperature, ECG, Concomitant medications, Hematology, Chemistry, Study drug record, ADAS-Cog, CIBIC+, DAD, NPI-X
Activities (SAI_16): NPI-X (additional NPI sub-node)

**Encounter_12 (Week 26) — SAI_24:**
Activities: Physical examination, Vital Signs and Temperature, ECG, Concomitant medications, Hematology, Chemistry, Study drug record, TTS Acceptability Survey, NPI-X

---

## Section 5 — Gaps

### 5.1 Encounter contact mode — CRITICAL GAP

**USDM field:** `encounter.contactModes[].code.decode`

**Values present in this file:**
- `"IN PERSON"` (CDISC code C175574) — all 12 encounters
- `"TELEPHONE CALL"` (CDISC code C171537) — Encounters 7–10 (Week 8, 12, 16, 20)

**Gap analysis:** `SoA-Profiles.fsh` defines `SOAPlanDefinition` (Profile: `soaPlanDefinition`) with the following action-level elements:
- `action.extension[soaTimepoint]` (SOATimePoint extension)
- `action.action.extension[soaTransition]` (SOATransition extension)
- `action.title`, `action.code`, `action.trigger`, `action.relatedAction`, `action.timing[x]`, `action.requiredBehavior`, `action.cardinalityBehavior`, `action.definition[x]`

**There is no element for encounter contact mode** in `SOAPlanDefinition`, `StudyVisitSoa`, or `StudyProtocolSoa`. The `action.code` element is present (`* action.code MS`) but carries no defined binding.

**Proposed workaround (per spec §Task F-4):**
Use `action.code` with a CDISC coded value:

```fsh
* action[+]
  * id = "E7"
  * title = "Week 8"
  // GAP: No SOAPlanDefinition element for encounter contact mode.
  // Workaround: encode as action.code using CDISC C171537 / C175574.
  * code[+]
    * coding[+]
      * system = "http://www.cdisc.org"
      * code = #C175574
      * display = "IN PERSON"
    * coding[+]
      * system = "http://www.cdisc.org"
      * code = #C171537
      * display = "TELEPHONE CALL"
```

**Long-term disposition:** Propose a `soaContactMode` sub-extension on `SOATimePoint` in a future profile version. File as a profile gap issue.

### 5.2 Early Termination encounter — GAP

**USDM situation:** No `Encounter` object for Early Termination. ScheduleTimeline_2 has SAI_2 with `encounterIds = null` and a list of ET activities.

**Hand-authored FSH:** `H2Q-MC-LZZT-Study-ET-14` exists as a full visit PlanDefinition.

**Proposed disposition:** The USDM-generated pipeline cannot emit an ET visit PlanDefinition from encounter data alone. Options:
1. **Synthesize** an ET encounter from ScheduleTimeline_2 (SAI_2 activities + no timing) — label it "Early Termination", subtype `"early-termination"`. This is the recommended approach.
2. **Skip** ET in the generated output and keep the hand-authored `H2Q-MC-LZZT-Study-ET-14` as-is.

**Recommendation:** Synthesize from ScheduleTimeline_2. Log a WARNING noting the synthetic encounter. Document in F-9 reconciliation.

### 5.3 Retreatment (RT) encounter — GAP

**USDM situation:** No `Encounter` object and no timeline for Retreatment.

**Hand-authored FSH:** `H2Q-MC-LZZT-Study-RT-15` exists.

**Proposed disposition:** Drop from generated output. Keep hand-authored `H2Q-MC-LZZT-Study-RT-15` as-is. Document in F-9 reconciliation as "hand-authored only".

### 5.4 ScheduledDecisionInstance — GAP

**USDM situation:** `ScheduledDecisionInstance_1` (WK16_Dec) appears in the main timeline between SAI_19 and SAI_20. It has `instanceType = "ScheduledDecisionInstance"` and `Timing_12b` (P0D). It represents a branching decision at Week 16 (NPI assessment).

**FHIR home:** `PlanDefinition.action` supports `condition` elements for applicability/start/stop. The decision node has no direct FHIR equivalent as a timeline node.

**Proposed disposition:** Skip the decision node in timeline traversal (treat as transparent). Log a WARNING. The NPI-X activity at Week 16 is captured via SAI_20 (`encounterIds = [Encounter_9]`). Document in F-9.

### 5.5 BiomedicalConceptCategory — partial gap

**USDM situation:** `BiomedicalConceptCategory` objects (BCCat_1 Vital Signs, BCCat_3 Chemistry, BCCat_4 Urinalysis) group BCs into panels. Activity_13 references `bcCategoryIds = [BCCat_1]` rather than individual BC ids.

**FHIR home:** `ObservationDefinition` supports `hasMember` for panels. The observation catalog should emit one panel `ObservationDefinition` per `BiomedicalConceptCategory` with `kind = panel` and member analyte rows.

**Proposed disposition:** Map → `ObservationDefinition` panel rows in the observation catalog (per spec §Task F-5).

### 5.6 Condition (conditional scheduling) — partial gap

**USDM situation:** Two `Condition` objects:
- `Condition_1` (HA1C): Activity_24 (Hemoglobin A1C) is conditional — only for insulin-dependent diabetic patients.
- `Condition_2` (Practice): Activities 27–30 (ADAS-Cog, CIBIC+, DAD, NPI-X) at SAI_9 are practice-only.

**FHIR home:** `PlanDefinition.action.condition` with `kind = #applicability` and a FHIRPath expression. The hand-authored Visit-1 FSH already implements this for HbA1c (see `H2Q-MC-LZZT-Visit-1.fsh` lines 107–110).

**Proposed disposition:** Map → `action.condition[+].kind = #applicability` with a text expression. The USDM `Condition.text` provides the condition description.

### 5.7 StudyEpoch chain — partial gap

**USDM situation:** 5 epochs (Screening, Treatment 1–3, Follow-Up) with `previousId`/`nextId` chain.

**FHIR home:** `ResearchStudy` has no direct epoch element in R6. The `period` element covers the overall study period only.

**Proposed disposition:** Document epochs in `ResearchStudy.description` as a structured note. Alternatively, use a custom extension. For Phase F, drop from generated FSH with a comment; document as a known gap.

### 5.8 StudyAmendment — drop

**USDM situation:** `StudyAmendment_1` with reason, changes, impacts, and geographic scopes.

**FHIR home:** No direct FHIR R6 element.

**Proposed disposition:** Drop from generated FSH. Document in IG narrative.

### 5.9 GovernanceDate — drop

**USDM situation:** 4 governance dates (approval, etc.).

**FHIR home:** `ResearchStudy.date` covers a single date. Multiple governance dates have no standard home.

**Proposed disposition:** Drop from generated FSH. Could be encoded as `ResearchStudy.extension` if needed.

### 5.10 Intra-visit sub-timings (Timing_17–24) — drop for Phase F

**USDM situation:** Timings 17–24 are sub-minute/sub-hour timings for the Vital Signs BP protocol (ScheduleTimeline_3): 5-minute supine, 1-minute standing, etc.

**FHIR home:** These are intra-visit procedure sequencing, not visit-level timing. They belong in the VS-BP sub-PlanDefinition, not in the main visit PlanDefinitions.

**Proposed disposition:** Out of scope for Phase F (visit-level only). Document as a known gap for a future phase.

### 5.11 Summary of gaps

| USDM field / concept | FHIR home | Disposition |
|---|---|---|
| `encounter.contactModes[]` | None in current profiles | Workaround: `action.code` with CDISC codes; flag in FSH comment |
| ET encounter (no USDM Encounter object) | PlanDefinition | Synthesize from ScheduleTimeline_2; log WARNING |
| RT encounter (no USDM data) | PlanDefinition | Keep hand-authored; document as hand-authored-only in F-9 |
| `ScheduledDecisionInstance` | None direct | Skip in traversal; log WARNING |
| `BiomedicalConceptCategory` | ObservationDefinition panel | Map → panel rows in observation catalog (F-5) |
| `Condition` (conditional scheduling) | `action.condition` | Map → `action.condition[+].kind = #applicability` |
| `StudyEpoch` chain | None in R6 | Drop from FSH; document in description |
| `StudyAmendment` | None | Drop from FSH; document in IG narrative |
| `GovernanceDate` | `ResearchStudy.date` (partial) | Drop from FSH |
| Intra-visit sub-timings (Timing_17–24) | Sub-PlanDefinition | Out of scope for Phase F |
| `persons[]` top-level array | Practitioner | Traverse `studyRoles[*].assignedPersons` instead |

---

## Section 6 — Timing Spot-Check Table

### 6.1 USDM timing derivation

ISO 8601 durations converted to days (P\<n\>W × 7, P\<n\>D as-is):

| Encounter id | Encounter name | Encounter label | scheduledAtId | USDM value | USDM day (d) | USDM windowLower | USDM windowUpper |
|---|---|---|---|---|---|---|---|
| Encounter_1 | E1 | Screening 1 | null | — | anchor | — | — |
| Encounter_2 | E2 | Screening 2 | Timing_2 | P2D | 2 | PT4H (0.167 d) | PT0H (0 d) |
| Encounter_3 | E3 | Baseline | null | — | anchor | — | — |
| Encounter_4 | E4 | Week 2 | Timing_4 | P2W | 14 | P3D (3 d) | P3D (3 d) |
| Encounter_5 | E5 | Week 4 | Timing_5 | P4W | 28 | P3D (3 d) | P3D (3 d) |
| Encounter_6 | E7 | Week 6 | Timing_6 | P6W | 42 | P3D (3 d) | P3D (3 d) |
| Encounter_7 | E8 | Week 8 | Timing_7 | P8W | 56 | P3D (3 d) | P3D (3 d) |
| Encounter_8 | E9 | Week 12 | Timing_9 | P12W | 84 | P4D (4 d) | P4D (4 d) |
| Encounter_9 | E10 | Week 16 | Timing_11 | P16W | 112 | P4D (4 d) | P4D (4 d) |
| Encounter_10 | E11 | Week 20 | Timing_13 | P20W | 140 | P4D (4 d) | P4D (4 d) |
| Encounter_11 | E12 | Week 24 | Timing_15 | P24W | 168 | P4D (4 d) | P4D (4 d) |
| Encounter_12 | E13 | Week 26 | Timing_16 | P26W | 182 | P3D (3 d) | P3D (3 d) |

### 6.2 Hand-authored values (from H2Q-MC-LZZT-ProtocolDesign.fsh)

The hand-authored `H2Q-MC-LZZT-ProtocolDesign.fsh` uses a different encounter numbering scheme (Visit-1 through Visit-13, ET-14, RT-15) that does not directly correspond to USDM encounter names. The mapping is inferred from labels and descriptions:

| Hand-authored visit id | Title | soaPlannedTimePoint (d) | soaPlannedRange low (d) | soaPlannedRange high (d) | soaReferenceTimePoint |
|---|---|---|---|---|---|
| H2Q-MC-LZZT-Study-Visit-1 | Visit-1 | 1 | — | — | (none — anchor) |
| H2Q-MC-LZZT-Study-Visit-2 | Visit-2 | 29 | -7 | 7 | Visit-1 |
| H2Q-MC-LZZT-Study-Visit-3 | Visit-3 | 30 | — | — | Visit-2 |
| H2Q-MC-LZZT-Study-Visit-4 | Visit-4 | 44 | -3 | 3 | Visit-3 |
| H2Q-MC-LZZT-Study-Visit-5 | Visit-5 | 58 | -3 | 3 | Visit-3 |
| H2Q-MC-LZZT-Study-Visit-6 | Visit-6 | (commented out) | — | — | — |
| H2Q-MC-LZZT-Study-Visit-7 | Visit-7 | 43 | -3 | 3 | Visit-1 |
| H2Q-MC-LZZT-Study-Visit-8 | Visit-8 | 57 | -3 | 3 | Visit-1 |
| H2Q-MC-LZZT-Study-Visit-9 | Visit-9 | 85 | -3 | 3 | Visit-1 |
| H2Q-MC-LZZT-Study-Visit-10 | Visit-10 | 113 | -3 | 3 | Visit-1 |
| H2Q-MC-LZZT-Study-Visit-11 | Visit-11 | 141 | -3 | 3 | Visit-1 |
| H2Q-MC-LZZT-Study-Visit-12 | Visit-12 | 169 | -3 | 3 | Visit-1 |
| H2Q-MC-LZZT-Study-Visit-13 | Visit-13 | 183 | -3 | 3 | Visit-1 |
| H2Q-MC-LZZT-Study-ET-14 | ET-14 | (none) | — | — | Visit-1 |
| H2Q-MC-LZZT-Study-RT-15 | RT-15 | (none) | — | — | (none) |

### 6.3 Comparison table

The hand-authored ProtocolDesign uses a **cumulative day** scheme (days from study start), while the USDM uses **relative durations** from the previous encounter. The USDM values below are the raw Timing.value converted to days; the reference encounter is the encounter pointed to by `Timing.relativeFromScheduledInstanceId`.

| USDM encounter | USDM label | USDM day | USDM window (±d) | Hand-authored visit | Hand-authored day | Hand-authored window | Match? | Notes |
|---|---|---|---|---|---|---|---|---|
| Encounter_1 | Screening 1 | anchor | — | Visit-1 | 1 | — | ⚠️ DISCREPANCY | USDM: anchor (no day); hand-authored: day 1 |
| Encounter_2 | Screening 2 | 2 d from E2 | +0.167/−0 d | Visit-2 | 29 d from V1 | ±7 d | ❌ MISMATCH | Different reference + different value; USDM is 2 days after Screening 1; hand-authored is 29 days from Visit-1 (likely Baseline) |
| Encounter_3 | Baseline | anchor | — | Visit-3 | 30 d from V2 | — | ⚠️ DISCREPANCY | USDM: anchor; hand-authored: 30 d from Visit-2 |
| Encounter_4 | Week 2 | 14 d (P2W) | ±3 d | Visit-4 | 44 d from V3 | ±3 d | ⚠️ DISCREPANCY | USDM: 14 d from Baseline; hand-authored: 44 d from Visit-3 (≈ 14 d from Baseline if V3=day 30) |
| Encounter_5 | Week 4 | 28 d (P4W) | ±3 d | Visit-5 | 58 d from V3 | ±3 d | ⚠️ DISCREPANCY | USDM: 28 d from Baseline; hand-authored: 58 d from Visit-3 (≈ 28 d from Baseline if V3=day 30) |
| Encounter_6 | Week 6 | 42 d (P6W) | ±3 d | Visit-6 | (commented out) | — | ❓ MISSING | Visit-6 is commented out in hand-authored FSH |
| Encounter_7 | Week 8 | 56 d (P8W) | ±3 d | Visit-7 | 43 d from V1 | ±3 d | ❌ MISMATCH | Different reference: USDM from Baseline; hand-authored from Visit-1 (Screening) |
| Encounter_8 | Week 12 | 84 d (P12W) | ±4 d | Visit-8 | 57 d from V1 | ±3 d | ❌ MISMATCH | Different reference + different value |
| Encounter_9 | Week 16 | 112 d (P16W) | ±4 d | Visit-9 | 85 d from V1 | ±3 d | ❌ MISMATCH | Different reference + different value |
| Encounter_10 | Week 20 | 140 d (P20W) | ±4 d | Visit-10 | 113 d from V1 | ±3 d | ❌ MISMATCH | Different reference + different value |
| Encounter_11 | Week 24 | 168 d (P24W) | ±4 d | Visit-11 | 141 d from V1 | ±3 d | ❌ MISMATCH | Different reference + different value |
| Encounter_12 | Week 26 | 182 d (P26W) | ±3 d | Visit-12 | 169 d from V1 | ±3 d | ❌ MISMATCH | Different reference + different value |
| (none) | — | — | — | Visit-13 | 183 d from V1 | ±3 d | ❓ MISSING | No USDM encounter corresponds to Visit-13 |
| (none — ET timeline) | — | — | — | ET-14 | (no day) | — | ⚠️ PARTIAL | ET activities in USDM ScheduleTimeline_2; no Encounter object |
| (none) | — | — | — | RT-15 | (no day) | — | ❌ MISSING | No USDM data for RT |

### 6.4 Discrepancy analysis

**Root cause of mismatches:** The hand-authored ProtocolDesign uses a **cumulative absolute day** scheme (all visits referenced from Visit-1 / Screening), while the USDM uses **relative durations from Baseline** (Encounter_3). The USDM `Timing.value` is the duration from the reference encounter (Baseline), not from study start.

**Reconciliation:**
- USDM Week 2 = 14 d from Baseline. If Baseline = day 30 (from Screening), then absolute day = 44. Hand-authored Visit-4 = 44 d from Visit-3 (Baseline). **These are consistent** when the reference is correctly resolved.
- USDM Week 4 = 28 d from Baseline → absolute day 58. Hand-authored Visit-5 = 58 d from Visit-3. **Consistent.**
- USDM Week 8 = 56 d from Baseline → absolute day 86. Hand-authored Visit-7 = 43 d from Visit-1 (Screening). **Inconsistent** — the hand-authored value appears to use a different reference point.
- The hand-authored Visit-7 through Visit-13 all reference Visit-1 (Screening), while USDM references Baseline. This is a systematic difference in reference point, not a data error.

**Authoritative source:** Per the spec, **USDM is authoritative**. The hand-authored values are reference only. The F-9 reconciliation report will surface these differences for human review.

**Visit-13 / Week 26+2 discrepancy:** The USDM has 12 encounters (Screening 1, Screening 2, Baseline, Week 2–26). The hand-authored FSH has 13 regular visits + ET + RT = 15. The USDM Encounter_12 (Week 26, 182 d) corresponds to hand-authored Visit-12 (169 d from V1) or Visit-13 (183 d from V1). The 1-day difference (182 vs 183) is within rounding of P26W = 182 d vs 26×7+1 = 183 d. This is a minor discrepancy.

---

## Appendix A — Encounter Summary

| USDM id | Name | Label | scheduledAtId | USDM day | Contact modes |
|---|---|---|---|---|---|
| Encounter_1 | E1 | Screening 1 | null (anchor) | — | IN PERSON |
| Encounter_2 | E2 | Screening 2 | Timing_2 | 2 d | IN PERSON |
| Encounter_3 | E3 | Baseline | null (anchor) | — | IN PERSON |
| Encounter_4 | E4 | Week 2 | Timing_4 | 14 d | IN PERSON |
| Encounter_5 | E5 | Week 4 | Timing_5 | 28 d | IN PERSON |
| Encounter_6 | E7 | Week 6 | Timing_6 | 42 d | IN PERSON |
| Encounter_7 | E8 | Week 8 | Timing_7 | 56 d | IN PERSON + TELEPHONE CALL |
| Encounter_8 | E9 | Week 12 | Timing_9 | 84 d | IN PERSON + TELEPHONE CALL |
| Encounter_9 | E10 | Week 16 | Timing_11 | 112 d | IN PERSON + TELEPHONE CALL |
| Encounter_10 | E11 | Week 20 | Timing_13 | 140 d | IN PERSON + TELEPHONE CALL |
| Encounter_11 | E12 | Week 24 | Timing_15 | 168 d | IN PERSON |
| Encounter_12 | E13 | Week 26 | Timing_16 | 182 d | IN PERSON |

---

## Appendix B — Activity Classification Summary

| Activity id | Label | Archetype | BC / Surrogate / Procedure |
|---|---|---|---|
| Activity_1 | Informed consent | measurement | BC_33 (Informed Consent, C16735) |
| Activity_2 | Inclusion and exclusion criteria | procedure | Procedure_3: SNOMED 61871000000107 |
| Activity_3 | Patient number assigned | procedure | Procedure_4: SNOMED 4561000175109 |
| Activity_4 | Demographics | instrument | BCSurr_1 (Date of Birth) + BC_20 (Sex) + BC_21 (Age) |
| Activity_5 | Hachinski Ischemic Scale | instrument | BCSurr_2 |
| Activity_6 | MMSE | instrument | BCSurr_3 |
| Activity_7 | Physical examination | measurement | BC_34 (Physical Examination Finding, C83119) — BC wins over Procedure_5 |
| Activity_8 | Medical history | measurement | BC_35 (Medical History, C83119) |
| Activity_9 | Habits | measurement | BC_36 (Alcohol Use, C81229) + BC_37 (Caffeine Use, C201990) |
| Activity_10 | Chest X-ray | procedure | Procedure_6: LOINC LA16043-4 |
| Activity_11 | Apo E genotyping | instrument | BCSurr_4 |
| Activity_12 | Patient randomised | procedure | Procedure_7: OMOP 4976950 |
| Activity_13 | Vital Signs and Temperature | measurement | BCCat_1 (panel) — via bcCategoryIds |
| Activity_14 | Ambulatory ECG placed | procedure | Procedure_8: SNOMED 164850009 |
| Activity_15 | Ambulatory ECG removed | procedure | Procedure_9: SNOMED 164850009 |
| Activity_16 | ECG | measurement | BC_38 (ECG Measurement, C62085) |
| Activity_17 | Placebo TTS test | instrument | BCSurr_5 |
| Activity_18 | CT scan | procedure | Procedure_1: SNOMED 383371000119108 |
| Activity_19 | Concomitant medications | measurement | BC_39 (Concomitant Therapy, C83056) |
| Activity_20 | Hematology | measurement | BC_32 (HbA1C, C64849) — note: also used for Activity_24 |
| Activity_21 | Chemistry | measurement | BCCat_3 (panel) — via bcCategoryIds |
| Activity_22 | Urinalysis | measurement | BCCat_4 (panel) — via bcCategoryIds |
| Activity_23 | Plasma Specimen (Xanomeline) | procedure | Procedure_10: SNOMED 119361006 |
| Activity_24 | Hemoglobin A1C | measurement | BC_32 (HbA1C, C64849) — conditional |
| Activity_25 | Study drug record / dispensed / returned | procedure | Procedure_11 + Procedure_12 |
| Activity_26 | TTS Acceptability Survey | procedure | Procedure_13: SNOMED 725111000000103 |
| Activity_27 | ADAS-Cog | measurement | BC_40 (ADAS-Cog, C100247) |
| Activity_28 | CIBIC+ | measurement | BC_20 + BC_21 |
| Activity_29 | DAD | measurement | BC_20 + BC_21 |
| Activity_30 | NPI-X | measurement | BC_20 + BC_21 |
| Activity_31 | Adverse events | measurement | BC_1 (Adverse Event Pre-specified, C87840) |
| Activity_32 | Check adverse events | procedure | Procedure_14: SNOMED 453961000124104 |
| Activity_33 | Subject supine | procedure | Procedure_15: SPONSOR 123 |
| Activity_34 | Vital signs while supine | measurement | BC_14 (SBP) + BC_15 (DBP) + BC_16 (HR) |
| Activity_35 | Subject Standing | procedure | Procedure_16: SPONSOR 124 |
| Activity_36 | Vital signs while standing | measurement | BC_17 (SBP) + BC_18 (DBP) + BC_19 (HR) |

> **Note on Activity_0 and Activity_4a/4b/32b:** These appear to be header/grouping rows (empty label or structural labels like "All Demographics Header", "Scores", "Vital Signs Supine/Standing"). They should be classified as `WARNING: unclassified` and skipped per the activity classification decision tree.

---

## Appendix C — Required Test Cases for TimingResolver (Task F-3)

| Timing id | scheduledAtId on encounter | Timing.value | Expected planned_day_value | windowLower (d) | windowUpper (d) |
|---|---|---|---|---|---|
| null | Encounter_1 (anchor) | — | None | None | None |
| null | Encounter_3 (anchor) | — | None | None | None |
| Timing_2 | Encounter_2 | P2D | 2.0 | 0.167 (PT4H) | 0.0 (PT0H) |
| Timing_4 | Encounter_4 | P2W | 14.0 | 3.0 | 3.0 |
| Timing_5 | Encounter_5 | P4W | 28.0 | 3.0 | 3.0 |
| Timing_6 | Encounter_6 | P6W | 42.0 | 3.0 | 3.0 |
| Timing_7 | Encounter_7 | P8W | 56.0 | 3.0 | 3.0 |
| Timing_9 | Encounter_8 | P12W | 84.0 | 4.0 | 4.0 |
| Timing_11 | Encounter_9 | P16W | 112.0 | 4.0 | 4.0 |
| Timing_13 | Encounter_10 | P20W | 140.0 | 4.0 | 4.0 |
| Timing_15 | Encounter_11 | P24W | 168.0 | 4.0 | 4.0 |
| Timing_16 | Encounter_12 | P26W | 182.0 | 3.0 | 3.0 |

> The spec (Task F-3) lists Timing_2 → 2.0, Timing_4 → 14.0, Timing_5 → 28.0 as required test cases. All confirmed correct above.
