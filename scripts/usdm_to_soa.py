#!/usr/bin/env python3
"""
usdm_to_soa.py — Orchestration script for Phase F USDM → SoA transform.

Usage:
    python3 scripts/usdm_to_soa.py <path-to-usdm.json>

Exit codes:
    0  — success (unclassified activity warnings do not fail the run)
    1  — fatal error (unresolved id reference, unresolvable scheduledAtId, etc.)

Execution order (per spec §Task F-8):
    0. Pre-flight validation via usdm4 (optional; skipped when not installed)
    1. Load + index USDM via USDMDoc
    2. Build TimingResolver
    3. emit_research_study()  → input/fsh/generated/usdm/ResearchStudy.gen.fsh
    4. emit_eligibility_groups() → input/fsh/generated/usdm/Eligibility.gen.fsh
    5. emit_visit_plan_definitions() → input/fsh/generated/usdm/visits/*.gen.fsh
    6. emit_protocol_design() → input/fsh/generated/usdm/ProtocolDesign.gen.fsh
    7. extract_activity_catalog() → input/data/usdm-activity-catalog.csv
    8. extract_observation_catalog() → input/data/usdm-observation-catalog.csv
    9. extract_soa_matrix() → input/data/usdm-soa-matrix.csv

All output directories are created if they do not exist.
All generated FSH carries a DO NOT EDIT header.
CSV outputs are idempotent on unchanged inputs.

stdlib only for core pipeline — usdm4 is an optional dependency used for
pre-flight validation only; the pipeline runs without it.
"""

import os
import sys
import pathlib

# ---------------------------------------------------------------------------
# Resolve script directory so sibling modules can always be imported
# ---------------------------------------------------------------------------
_SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from usdm_loader import load as _usdm_load, USDM4_AVAILABLE  # noqa: E402

from usdm_reader import USDMDoc, emit_research_study, emit_eligibility_groups  # noqa: E402
from usdm_reader import emit_visit_plan_definitions, emit_protocol_design       # noqa: E402
from usdm_reader import emit_activity_stubs, emit_visit_activity_actions        # noqa: E402
from usdm_reader import emit_non_main_timeline_plans                            # noqa: E402
from usdm_timing import TimingResolver                                           # noqa: E402
from usdm_catalogs import (                                                      # noqa: E402
    extract_activity_catalog, write_activity_catalog,
    extract_observation_catalog, write_observation_catalog,
    extract_soa_matrix, write_soa_matrix,
)


def _repo_root(usdm_path: str) -> pathlib.Path:
    """
    Infer the repo root from the USDM file path.

    Strategy: walk up from the USDM file until we find a directory that
    contains 'input/usdm/' or 'sushi-config.yaml'.  Falls back to the
    current working directory.
    """
    p = pathlib.Path(usdm_path).resolve().parent
    for candidate in [p, p.parent, p.parent.parent]:
        if (candidate / "sushi-config.yaml").exists():
            return candidate
    return pathlib.Path.cwd()


def run(usdm_path: str) -> int:
    """
    Execute the full pipeline.  Returns 0 on success, 1 on fatal error.
    Warnings are printed to stderr but do not affect the exit code.
    """
    # Step 0: pre-flight validation (optional — graceful no-op without usdm4)
    if USDM4_AVAILABLE:
        print("Validating USDM (usdm4) …", flush=True)
    _usdm_load(usdm_path, validate=True, strict=False)

    print(f"Loading USDM: {usdm_path}", flush=True)
    try:
        doc = USDMDoc(usdm_path)
    except Exception as exc:
        print(f"FATAL: could not load USDM file: {exc}", file=sys.stderr)
        return 1

    repo = _repo_root(usdm_path)
    fsh_out = str(repo / "input" / "fsh" / "generated" / "usdm")
    data_out = str(repo / "input" / "data")

    # Step 2: build TimingResolver
    print("Building TimingResolver …", flush=True)
    try:
        resolver = TimingResolver(doc)
    except Exception as exc:
        print(f"FATAL: TimingResolver construction failed: {exc}", file=sys.stderr)
        return 1

    # Step 3: ResearchStudy
    rs_path = os.path.join(fsh_out, "ResearchStudy.gen.fsh")
    print(f"  → {rs_path}", flush=True)
    try:
        emit_research_study(doc, rs_path)
    except Exception as exc:
        print(f"FATAL: emit_research_study failed: {exc}", file=sys.stderr)
        return 1

    # Step 4: Eligibility Groups
    elig_path = os.path.join(fsh_out, "Eligibility.gen.fsh")
    print(f"  → {elig_path}", flush=True)
    try:
        emit_eligibility_groups(doc, elig_path)
    except Exception as exc:
        print(f"FATAL: emit_eligibility_groups failed: {exc}", file=sys.stderr)
        return 1

    # Step 5: Visit PlanDefinitions (main timeline encounters)
    print(f"  → {fsh_out}/visits/*.gen.fsh", flush=True)
    try:
        written = emit_visit_plan_definitions(doc, fsh_out, timing_resolver=resolver)
        print(f"     {len(written)} visit files written", flush=True)
    except Exception as exc:
        print(f"FATAL: emit_visit_plan_definitions failed: {exc}", file=sys.stderr)
        return 1

    # Step 6: ProtocolDesign
    pd_path = os.path.join(fsh_out, "ProtocolDesign.gen.fsh")
    print(f"  → {pd_path}", flush=True)
    try:
        emit_protocol_design(doc, pd_path, timing_resolver=resolver)
    except Exception as exc:
        print(f"FATAL: emit_protocol_design failed: {exc}", file=sys.stderr)
        return 1

    # Step 7: Activity catalog (needed by Steps 7b and 11)
    act_path = os.path.join(data_out, "usdm-activity-catalog.csv")
    print(f"  → {act_path}", flush=True)
    try:
        act_rows = extract_activity_catalog(usdm_path)
        write_activity_catalog(act_rows, act_path)
    except Exception as exc:
        print(f"FATAL: extract_activity_catalog failed: {exc}", file=sys.stderr)
        return 1

    # Step 7b: Non-main timeline PlanDefinitions (ET, AE, etc.)
    try:
        extra = emit_non_main_timeline_plans(doc, fsh_out, act_path)
        if extra:
            print(f"     {len(extra)} non-main timeline file(s) written", flush=True)
    except Exception as exc:
        print(f"FATAL: emit_non_main_timeline_plans failed: {exc}", file=sys.stderr)
        return 1

    # Step 8: Observation catalog
    obs_path = os.path.join(data_out, "usdm-observation-catalog.csv")
    print(f"  → {obs_path}", flush=True)
    try:
        obs_rows = extract_observation_catalog(usdm_path)
        write_observation_catalog(obs_rows, obs_path)
    except Exception as exc:
        print(f"FATAL: extract_observation_catalog failed: {exc}", file=sys.stderr)
        return 1

    # Step 9: SoA matrix
    matrix_path = os.path.join(data_out, "usdm-soa-matrix.csv")
    print(f"  → {matrix_path}", flush=True)
    try:
        matrix_result = extract_soa_matrix(usdm_path, act_path)
        write_soa_matrix(matrix_result, matrix_path)
    except Exception as exc:
        print(f"FATAL: extract_soa_matrix failed: {exc}", file=sys.stderr)
        return 1

    # Step 10: Activity, ObservationDefinition, and Questionnaire stubs
    stubs_path = os.path.join(fsh_out, "ActivityStubs.gen.fsh")
    print(f"  → {stubs_path}", flush=True)
    try:
        emit_activity_stubs(act_path, obs_path, stubs_path)
    except Exception as exc:
        print(f"FATAL: emit_activity_stubs failed: {exc}", file=sys.stderr)
        return 1

    # Step 11: Inline activity actions into visit FSH files
    visits_dir = os.path.join(fsh_out, "visits")
    print(f"  → activity actions in {visits_dir}/", flush=True)
    try:
        modified = emit_visit_activity_actions(act_path, matrix_path, visits_dir)
        print(f"     {len(modified)} visit files updated", flush=True)
    except Exception as exc:
        print(f"FATAL: emit_visit_activity_actions failed: {exc}", file=sys.stderr)
        return 1

    print("Done — pipeline complete (0 errors).", flush=True)
    return 0


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python3 scripts/usdm_to_soa.py <path-to-usdm.json>",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(run(sys.argv[1]))


if __name__ == "__main__":
    main()
