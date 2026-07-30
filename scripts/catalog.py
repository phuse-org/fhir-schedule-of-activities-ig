#!/usr/bin/env python3
"""Loader + validator for the protocol-pipeline catalogs (stdlib only)."""
import csv
import sys
import pathlib

ARCHETYPES = {"measurement", "instrument", "procedure"}
OBS_KINDS = {"analyte", "panel"}


def load_csv(path):
    """Load a CSV file, skipping comment lines that start with '#'."""
    with open(path, newline="") as f:
        # Filter out comment lines before passing to DictReader
        lines = [line for line in f if not line.startswith("#")]
    return list(csv.DictReader(lines))


def validate_activities(activities, obs_ids, cond_ids):
    errors = []
    seen = set()
    for a in activities:
        aid = a["id"]
        if aid in seen:
            errors.append(f"duplicate activity id: {aid}")
        seen.add(aid)
        if a["archetype"] not in ARCHETYPES:
            errors.append(f"{aid}: bad archetype {a['archetype']!r}")
        if a["archetype"] == "measurement":
            if not a["result_obsdef_id"]:
                errors.append(f"{aid}: measurement missing result_obsdef_id")
            elif a["result_obsdef_id"] not in obs_ids:
                errors.append(
                    f"{aid}: result_obsdef_id {a['result_obsdef_id']} "
                    f"not in observation catalog")
        if a["archetype"] == "instrument":
            if not a["questionnaire_id"]:
                errors.append(f"{aid}: instrument missing questionnaire_id")
            if not a.get("respondent_type"):
                errors.append(f"{aid}: instrument missing respondent_type")
        if a["archetype"] == "procedure":
            if not a.get("code"):
                errors.append(f"{aid}: procedure missing code")
            if a.get("result_obsdef_id"):
                errors.append(
                    f"{aid}: procedure must have empty result_obsdef_id "
                    f"(got {a['result_obsdef_id']!r})")
            if a.get("questionnaire_id"):
                errors.append(
                    f"{aid}: procedure must have empty questionnaire_id "
                    f"(got {a['questionnaire_id']!r})")
        if a.get("default_condition") and a["default_condition"] not in cond_ids:
            errors.append(
                f"{aid}: default_condition {a['default_condition']} "
                f"not in condition catalog")
    return errors


def validate_observations(observations, require_panel_code=True):
    """Validate observation catalog rows.

    Args:
        observations: list of observation catalog dicts.
        require_panel_code: if True (default), panels must have a non-empty code.
            Set to False for USDM-derived catalogs where BCCategory panels have no
            code yet (F-5b enrichment supplies LOINC panel codes later).
    """
    errors = []
    seen = set()
    panel_ids = {o["obsdef_id"] for o in observations if o["kind"] == "panel"}
    for o in observations:
        oid = o["obsdef_id"]
        if oid in seen:
            errors.append(f"duplicate obsdef_id: {oid}")
        seen.add(oid)
        if o["kind"] not in OBS_KINDS:
            errors.append(f"{oid}: bad kind {o['kind']!r}")
        if require_panel_code and o["kind"] == "panel" and not o["code"]:
            errors.append(f"{oid}: panel missing code")
        if o.get("member_of") and o["member_of"] not in panel_ids:
            errors.append(f"{oid}: member_of {o['member_of']} is not a panel")
    return errors


def validate_conditions(conditions):
    errors = []
    seen = set()
    for c in conditions:
        cid = c["condition_id"]
        if cid in seen:
            errors.append(f"duplicate condition_id: {cid}")
        seen.add(cid)
        if not c["language"] or not c["expression"]:
            errors.append(f"{cid}: missing language or expression")
    return errors


def validate_catalogs(activities, observations, conditions,
                      require_panel_code=True):
    obs_ids = {o["obsdef_id"] for o in observations}
    cond_ids = {c["condition_id"] for c in conditions}
    return (validate_activities(activities, obs_ids, cond_ids)
            + validate_observations(observations,
                                    require_panel_code=require_panel_code)
            + validate_conditions(conditions))


def _validate_usdm_catalogs(base):
    """Validate the USDM-derived activity and observation catalogs.

    USDM panels have no code yet (F-5b enrichment supplies LOINC codes later),
    so require_panel_code=False.  USDM catalogs have no condition catalog.
    """
    act_path = base / "usdm-activity-catalog.csv"
    obs_path = base / "usdm-observation-catalog.csv"
    if not act_path.exists() or not obs_path.exists():
        return []  # USDM catalogs not yet generated — skip silently
    activities = load_csv(act_path)
    observations = load_csv(obs_path)
    obs_ids = {o["obsdef_id"] for o in observations}
    errs = validate_activities(activities, obs_ids, set())
    errs += validate_observations(observations, require_panel_code=False)
    return errs


def main():
    base = pathlib.Path(__file__).resolve().parent.parent / "input/data"
    errs = validate_catalogs(
        load_csv(base / "activity-catalog.csv"),
        load_csv(base / "observation-catalog.csv"),
        load_csv(base / "condition-catalog.csv"),
    )
    usdm_errs = _validate_usdm_catalogs(base)
    if usdm_errs:
        print("--- USDM catalog errors ---")
    errs += usdm_errs
    for e in errs:
        print("ERROR:", e)
    print(f"{len(errs)} error(s).")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
