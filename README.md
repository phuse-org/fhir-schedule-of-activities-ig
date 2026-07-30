# FHIR Schedule of Activities Implementation Guide

A PHUSE/HL7 FHIR R6 Implementation Guide for representing a clinical trial
**Schedule of Activities (SoA)** as computable FHIR resources. The exemplar
study is **H2Q-MC-LZZT** — the CDISC Alzheimer's Pilot Study (Xanomeline TTS).

- **Status:** draft v0.1.1 (FHIR R6 ballot3)
- **Published IG:** <https://phuse-org.github.io/fhir-schedule-of-activities-ig/>
- **Repository:** <https://github.com/phuse-org/fhir-schedule-of-activities-ig>

---

## Quick start

Prerequisites: Java 11+, [SUSHI](https://fshschool.org/sushi/) v3+, Python 3.9+,
[Task](https://taskfile.dev) v3+.

```sh
# 1. Download the IG Publisher (first time only)
task update-publisher

# 2. Generate FSH from USDM source and lab panels
task generate

# 3. Run Python unit tests
task test

# 4. Compile FSH → FHIR JSON
task sushi

# 5. Full IG build (requires network for terminology server)
task build

# Offline build (no terminology server)
task build:notx
```

Run `task` with no arguments for a full list of available tasks.

---

## Repository layout

```
input/
  usdm/                     USDM v4 source (CDISC_Pilot_Study_v4_FIXED.json)
  fsh/                      Hand-authored FHIR Shorthand
    generated/usdm/         Auto-generated FSH — DO NOT EDIT
  data/
    usdm-activity-catalog.csv   Activities extracted from USDM (generated)
    usdm-observation-catalog.csv
    usdm-soa-matrix.csv         36-activity × 12-encounter SoA grid (generated)
    lab-panels.csv              Hand-authored lab panel / analyte definitions
scripts/
  usdm_to_soa.py            Main USDM → FSH pipeline (11 steps)
  lab_panels_to_fsh.py      Lab panels CSV → FSH generator
  usdm_reader.py            USDM loader, indexer, FSH emitters
  usdm_catalogs.py          Activity & observation catalog extraction
  usdm_timing.py            ISO 8601 duration → planned-day resolver
  usdm_reconcile.py         Reconciliation report (USDM vs hand-authored)
  test_*.py                 Unit + integration tests (394 tests)
fsh-generated/resources/    SUSHI output — DO NOT EDIT
Taskfile.yml                Task runner (generate / test / sushi / build)
```

---

## Generation pipeline

```
USDM JSON  ──► usdm_to_soa.py ──► ActivityStubs.gen.fsh
                                   ProtocolDesign.gen.fsh
                                   visits/E*.gen.fsh
                                   ResearchStudy.gen.fsh
                                   Eligibility.gen.fsh
                                   usdm-*-catalog.csv

lab-panels.csv ──► lab_panels_to_fsh.py ──► LabPanels.gen.fsh

input/fsh/ (hand-authored + generated) ──► sushi . ──► fsh-generated/resources/

fsh-generated/ ──► publisher.jar ──► output/ (published IG)
```

The `usdm-*` catalog CSVs and all `*.gen.fsh` files are generated — do not
edit them by hand. To change generated output, edit the source USDM file, the
`lab-panels.csv`, or the classification overrides in `scripts/usdm_catalogs.py`,
then re-run `task generate`.

---

## Lab panels

Lab test definitions (Hematology, Chemistry, Urinalysis, Thyroid, Other) that
are absent or incomplete in the USDM are maintained in `input/data/lab-panels.csv`.
Edit that file and run `task generate:labs` to regenerate `LabPanels.gen.fsh`.

---

## Contributing

1. Create a branch from `main` (e.g. `feature/my-change`).
2. Make changes; run `task generate && task test && task sushi` to verify.
3. Commit, push, and open a pull request against `main`.
4. CI runs `task ci` (generate → test → sushi) on every push.

See the [Developer Setup](https://phuse-org.github.io/fhir-schedule-of-activities-ig/developer.html)
page in the published IG for full installation instructions.
