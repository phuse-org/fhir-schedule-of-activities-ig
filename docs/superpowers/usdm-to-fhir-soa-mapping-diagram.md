# USDM to FHIR SoA Mapping Summary Diagram

This diagram summarizes how the USDM source file is transformed by the Phase F
pipeline into FHIR SoA structures and supporting artifacts.

```mermaid
flowchart LR
  USDM["USDM JSON\ninput/usdm/CDISC_Pilot_Study_v4_FIXED.json"]

  subgraph PIPE["scripts/usdm_to_soa.py"]
    L["Load + index\nUSDMDoc"]
    T["Resolve timing\nTimingResolver"]
    C["Extract catalogs\nactivity / observation / SoA matrix CSV"]
    E1["Emit core study resources"]
    E2["Emit visit and protocol plans"]
    E3["Emit stubs + inline visit actions"]
  end

  subgraph MAP1["USDM element mapping"]
    M1["study + studyDesign + identifiers + arms + objectives"]
    M2["organizations"]
    M3["studyRoles.assignedPersons"]
    M4["population.criterionIds + eligibilityCriteria"]
    M5["encounters + timing (scheduledAtId)"]
    M6["activities + biomedicalConceptIds + bcSurrogateIds + definedProcedures"]
    M7["scheduleTimelines + scheduledActivityInstances + activity.timelineId"]
  end

  subgraph FHIR["Generated FHIR SoA structures (FSH)"]
    F1["ResearchStudy.gen.fsh\n(ResearchStudy)"]
    F2["ResearchStudy.gen.fsh\n(Organization, Practitioner references)"]
    F3["Eligibility.gen.fsh\n(Group inclusion/exclusion)"]
    F4["visits/*.gen.fsh\n(SoAPlanDefinition per encounter)"]
    F5["ProtocolDesign.gen.fsh\n(master SoAPlanDefinition)"]
    F6["ActivityStubs.gen.fsh\n(ActivityDefinition / ObservationDefinition / Questionnaire stubs)"]
  end

  subgraph CSV["Generated catalogs"]
    D1["input/data/usdm-activity-catalog.csv"]
    D2["input/data/usdm-observation-catalog.csv"]
    D3["input/data/usdm-soa-matrix.csv"]
  end

  USDM --> L --> T --> C
  L --> E1
  L --> E2
  T --> E2
  C --> E3
  E2 --> E3

  L --> M1 --> F1
  L --> M2 --> F2
  L --> M3 --> F2
  L --> M4 --> F3
  T --> M5 --> F4
  L --> M6 --> F6
  L --> M7 --> D3

  C --> D1
  C --> D2
  C --> D3

  D1 --> F6
  D2 --> F6
  D1 --> E3
  D3 --> E3
  E2 --> F4
  E2 --> F5
  E3 --> F4
```

## Reading Notes

- The pipeline is deterministic and idempotent: unchanged USDM input yields
  byte-identical generated outputs.
- `usdm-activity-catalog.csv` and `usdm-soa-matrix.csv` are used twice:
  first as extracted artifacts, then to add activity/action details to visit
  PlanDefinitions.
- Activity classification precedence is:
  `biomedicalConceptIds` -> measurement,
  `bcSurrogateIds` -> instrument/questionnaire,
  `definedProcedures` -> procedure.

## Slide-Friendly Diagram (Compact)

Use this version when you need a single-slide summary focused on source
elements, transformation stages, and final SoA resource families.

```mermaid
flowchart LR
  subgraph A["1) USDM Source Elements"]
    A1["Study + Design + Arms + Objectives"]
    A2["Organizations + Study Roles + Persons"]
    A3["Population + Eligibility Criteria"]
    A4["Encounters + Timing"]
    A5["Activities + BC / BCS / Procedures"]
    A6["Schedule Timelines + Scheduled Activity Instances"]
  end

  subgraph B["2) Transformation Pipeline"]
    B1["Load + Index\nUSDMDoc"]
    B2["Resolve Timing\nTimingResolver"]
    B3["Build Catalogs\nactivity / observation / matrix"]
    B4["Emit FSH + Inline Actions"]
  end

  subgraph C["3) FHIR SoA Outputs"]
    C1["ResearchStudy\n(+ Organization, Practitioner refs)"]
    C2["Eligibility Group"]
    C3["Visit SoAPlanDefinition(s)"]
    C4["ProtocolDesign SoAPlanDefinition"]
    C5["ActivityDefinition / ObservationDefinition / Questionnaire stubs"]
  end

  A1 --> B1
  A2 --> B1
  A3 --> B1
  A4 --> B2
  A5 --> B3
  A6 --> B3

  B1 --> B4
  B2 --> B4
  B3 --> B4

  B4 --> C1
  B4 --> C2
  B4 --> C3
  B4 --> C4
  B4 --> C5
```