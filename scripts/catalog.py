#!/usr/bin/env python3
"""Loader + validator for the protocol-pipeline catalogs (stdlib only)."""
import csv
import sys
import pathlib

ARCHETYPES = {"measurement", "instrument"}
OBS_KINDS = {"analyte", "panel"}


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


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
        if a["archetype"] == "instrument" and not a["questionnaire_id"]:
            errors.append(f"{aid}: instrument missing questionnaire_id")
        if a.get("default_condition") and a["default_condition"] not in cond_ids:
            errors.append(
                f"{aid}: default_condition {a['default_condition']} "
                f"not in condition catalog")
    return errors


def validate_observations(observations):
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
        if o["kind"] == "panel" and not o["code"]:
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


def validate_catalogs(activities, observations, conditions):
    obs_ids = {o["obsdef_id"] for o in observations}
    cond_ids = {c["condition_id"] for c in conditions}
    return (validate_activities(activities, obs_ids, cond_ids)
            + validate_observations(observations)
            + validate_conditions(conditions))


def main():
    base = pathlib.Path(__file__).resolve().parent.parent / "input/data"
    errs = validate_catalogs(
        load_csv(base / "activity-catalog.csv"),
        load_csv(base / "observation-catalog.csv"),
        load_csv(base / "condition-catalog.csv"),
    )
    for e in errs:
        print("ERROR:", e)
    print(f"{len(errs)} error(s).")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
