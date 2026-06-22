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
