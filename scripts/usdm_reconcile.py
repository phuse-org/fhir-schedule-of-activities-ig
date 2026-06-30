#!/usr/bin/env python3
"""
usdm_reconcile.py — Reconciliation report: USDM-derived vs. hand-authored resources.

Three sections (per spec §Task F-9):
  1. Timing reconciliation — encounter planned day + window, USDM vs. hand-authored
  2. Activity reconciliation — usdm-activity-catalog.csv vs. activity-catalog.csv
  3. Schedule reconciliation — usdm-soa-matrix.csv vs. hand-authored visit FSH actions

Writes: docs/superpowers/usdm-reconciliation.md

stdlib only — no third-party imports.

Usage:
    python3 scripts/usdm_reconcile.py
"""

import csv
import os
import pathlib
import re
import sys

_SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from usdm_reader import USDMDoc  # noqa: E402
from usdm_timing import TimingResolver, parse_iso8601_duration_to_days  # noqa: E402

_USDM_PATH = _REPO_ROOT / "input" / "usdm" / "CDISC_Pilot_Study_v4_FIXED.json"
_USDM_ACTIVITY_CSV = _REPO_ROOT / "input" / "data" / "usdm-activity-catalog.csv"
_ACTIVITY_CSV = _REPO_ROOT / "input" / "data" / "activity-catalog.csv"
_MATRIX_CSV = _REPO_ROOT / "input" / "data" / "usdm-soa-matrix.csv"
_FSH_DIR = _REPO_ROOT / "input" / "fsh"
_OUT_PATH = _REPO_ROOT / "docs" / "superpowers" / "usdm-reconciliation.md"

# ---------------------------------------------------------------------------
# USDM encounter name → hand-authored visit id mapping
# (derived from F-0 audit §6.2 label comparison)
# ---------------------------------------------------------------------------
USDM_TO_HA_VISIT = {
    "E1": "H2Q-MC-LZZT-Study-Visit-1",
    "E2": "H2Q-MC-LZZT-Study-Visit-2",
    "E3": "H2Q-MC-LZZT-Study-Visit-3",
    "E4": "H2Q-MC-LZZT-Study-Visit-4",
    "E5": "H2Q-MC-LZZT-Study-Visit-5",
    "E7": "H2Q-MC-LZZT-Study-Visit-6",   # Visit-6 is commented out
    "E8": "H2Q-MC-LZZT-Study-Visit-7",
    "E9": "H2Q-MC-LZZT-Study-Visit-8",
    "E10": "H2Q-MC-LZZT-Study-Visit-9",
    "E11": "H2Q-MC-LZZT-Study-Visit-10",
    "E12": "H2Q-MC-LZZT-Study-Visit-11",
    "E13": "H2Q-MC-LZZT-Study-Visit-12",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_csv(path: pathlib.Path) -> list:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        # Skip comment lines starting with '#'
        lines = [ln for ln in fh if not ln.startswith("#")]
    import io
    return list(csv.DictReader(io.StringIO("".join(lines))))


def _fmt_day(val) -> str:
    if val is None:
        return "—"
    if isinstance(val, float):
        if val == int(val):
            return str(int(val))
        # Round fractional days to 4 decimal places
        return f"{val:.4f}".rstrip("0").rstrip(".")
    return str(val)


def _fmt_window(low, high) -> str:
    if low is None and high is None:
        return "—"
    return f"{_fmt_day(low)} / {_fmt_day(high)}"


# ---------------------------------------------------------------------------
# Section 1: Timing reconciliation
# ---------------------------------------------------------------------------

# Regex patterns to extract soaPlannedTimePoint value and soaPlannedRange
# from hand-authored FSH files.
_HA_PROTOCOL_FSH = _FSH_DIR / "H2Q-MC-LZZT-ProtocolDesign.fsh"


def _parse_ha_protocol_timing() -> dict:
    """
    Parse H2Q-MC-LZZT-ProtocolDesign.fsh and return a dict:
      visit_id → {"day": float|None, "window_low": float|None,
                   "window_high": float|None, "target": str|None}

    Each action block:
      * definitionUri = "PlanDefinition/<visit_id>"
      * relatedAction[+]
        * targetId = "<target>"
        * offsetRange.low.value = <N>
        * offsetRange.high.value = <M>   (optional)
    """
    if not _HA_PROTOCOL_FSH.exists():
        return {}

    content = _HA_PROTOCOL_FSH.read_text(encoding="utf-8")
    # Split on action[+] boundaries; each chunk covers one action
    # We split on lines that start "* action[+]" (top-level action)
    action_blocks = re.split(r"(?=^\* action\[\+\])", content, flags=re.MULTILINE)

    result = {}
    for block in action_blocks:
        # Get definitionUri
        m_uri = re.search(r'definitionUri\s*=\s*"PlanDefinition/([^"]+)"', block)
        if not m_uri:
            continue
        visit_id = m_uri.group(1)

        m_target = re.search(r'targetId\s*=\s*"([^"]+)"', block)
        target = m_target.group(1) if m_target else None

        m_low = re.search(r'offsetRange\.low\.value\s*=\s*([0-9.]+)', block)
        day = float(m_low.group(1)) if m_low else None

        m_high = re.search(r'offsetRange\.high\.value\s*=\s*([0-9.]+)', block)
        window_high = float(m_high.group(1)) if m_high else None

        result[visit_id] = {
            "day": day,
            "window_low": day,        # hand-authored uses low only for offset
            "window_high": window_high,
            "target": target,
        }

    return result


def _read_fsh(visit_id: str) -> str:
    """Read a hand-authored visit FSH file by visit id."""
    # Try multiple naming conventions
    candidates = [
        _FSH_DIR / f"{visit_id}.fsh",
        _FSH_DIR / f"H2Q-MC-LZZT-{visit_id}.fsh",
    ]
    # Also handle the common pattern: H2Q-MC-LZZT-Study-Visit-N → H2Q-MC-LZZT-Visit-N.fsh
    # e.g. H2Q-MC-LZZT-Study-Visit-4 → H2Q-MC-LZZT-Visit-4.fsh
    short = visit_id.replace("H2Q-MC-LZZT-Study-", "H2Q-MC-LZZT-")
    candidates.append(_FSH_DIR / f"{short}.fsh")
    # ET/RT special names
    # H2Q-MC-LZZT-Study-ET-14 → H2Q-MC-LZZT-Visit-14-ET.fsh
    # H2Q-MC-LZZT-Study-RT-15 → H2Q-MC-LZZT-Visit-15-RT.fsh
    if "ET-14" in visit_id:
        candidates.append(_FSH_DIR / "H2Q-MC-LZZT-Visit-14-ET.fsh")
    if "RT-15" in visit_id:
        candidates.append(_FSH_DIR / "H2Q-MC-LZZT-Visit-15-RT.fsh")
    for p in candidates:
        if p.exists():
            return p.read_text(encoding="utf-8")
    return ""


def _ordered_encounters(doc: USDMDoc) -> list:
    encounters = doc.encounters()
    enc_by_id = {e["id"]: e for e in encounters}
    first = next((e for e in encounters if not e.get("previousId")), None)
    if first is None:
        return list(encounters)
    ordered, visited = [], set()
    current = first
    while current is not None:
        if current["id"] in visited:
            break
        visited.add(current["id"])
        ordered.append(current)
        nxt = current.get("nextId")
        current = enc_by_id.get(nxt) if nxt else None
    for e in encounters:
        if e["id"] not in visited:
            ordered.append(e)
    return ordered


def section_timing(doc: USDMDoc, resolver: TimingResolver) -> str:
    """Generate the timing reconciliation section."""
    ha_timing = _parse_ha_protocol_timing()
    rows = []
    ordered = _ordered_encounters(doc)

    for enc in ordered:
        enc_name = enc.get("name", "")
        enc_label = enc.get("label", "")
        ha_visit_id = USDM_TO_HA_VISIT.get(enc_name, "—")

        timing = resolver.resolve(enc.get("scheduledAtId"))

        # USDM values
        usdm_day = _fmt_day(timing.planned_day_value if timing else None)
        usdm_window = _fmt_window(
            timing.window_lower_days if timing else None,
            timing.window_upper_days if timing else None,
        )

        # Hand-authored values
        if ha_visit_id == "—":
            ha_day = "—"
            ha_window = "—"
            ha_ref = "—"
            match = "N/A"
        else:
            ha = ha_timing.get(ha_visit_id, {})
            if not ha and ha_visit_id not in ha_timing:
                # Check if it's commented out (Visit-6)
                ha_day = "commented out"
                ha_window = "—"
                ha_ref = "—"
                match = "⚠️ COMMENTED OUT"
            else:
                ha_day = _fmt_day(ha.get("day"))
                ha_window_low = ha.get("window_low")
                ha_window_high = ha.get("window_high")
                ha_window = _fmt_window(ha_window_low, ha_window_high)
                ha_ref = ha.get("target") or "—"

                # Determine match
                if timing is None:
                    match = "✅ ANCHOR" if ha.get("day") is None else "⚠️ DISCREPANCY"
                elif ha.get("day") is None:
                    match = "⚠️ DISCREPANCY"
                elif abs(timing.planned_day_value - ha["day"]) <= 1.0:
                    match = "✅ MATCH"
                else:
                    match = "❌ MISMATCH"

        rows.append((enc_name, enc_label, usdm_day, usdm_window,
                     ha_visit_id, ha_day, ha_window, match))

    lines = [
        "## Section 1 — Timing Reconciliation",
        "",
        "Compares USDM-derived `soaPlannedTimePoint` and window against "
        "hand-authored FSH values for each encounter.",
        "",
        "| USDM enc | USDM label | USDM day | USDM window (low/high) | "
        "Hand-authored visit | HA day | HA window | Match? |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for enc_name, enc_label, usdm_day, usdm_window, ha_id, ha_day, ha_window, match in rows:
        lines.append(
            f"| {enc_name} | {enc_label} | {usdm_day} | {usdm_window} | "
            f"{ha_id} | {ha_day} | {ha_window} | {match} |"
        )

    # Extra hand-authored visits with no USDM equivalent
    lines += [
        "",
        "### Hand-authored visits with no USDM encounter",
        "",
        "| Hand-authored visit | Notes |",
        "|---|---|",
        "| H2Q-MC-LZZT-Study-Visit-13 | No USDM equivalent; nearest is E13 (Week 26, 182d vs 183d) |",
        "| H2Q-MC-LZZT-Study-ET-14 | ET timeline in USDM (ScheduleTimeline_2); no Encounter object |",
        "| H2Q-MC-LZZT-Study-RT-15 | No USDM data; hand-authored only |",
        "",
        "> **Root cause of systematic mismatches:** The hand-authored ProtocolDesign uses "
        "cumulative absolute days from Visit-1 (Screening), while the USDM uses relative "
        "durations from the previous anchor (Baseline). USDM is authoritative per the spec.",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section 2: Activity reconciliation
# ---------------------------------------------------------------------------

def section_activities() -> str:
    usdm_rows = _load_csv(_USDM_ACTIVITY_CSV)
    ha_rows = _load_csv(_ACTIVITY_CSV)

    usdm_ids = {r["id"] for r in usdm_rows if r.get("id")}
    ha_ids = {r["id"] for r in ha_rows if r.get("id")}

    matched = usdm_ids & ha_ids
    usdm_only = usdm_ids - ha_ids
    ha_only = ha_ids - usdm_ids

    lines = [
        "## Section 2 — Activity Reconciliation",
        "",
        f"Compares `usdm-activity-catalog.csv` ({len(usdm_ids)} activities) against "
        f"`activity-catalog.csv` ({len(ha_ids)} activities).",
        "",
        f"- **Matched:** {len(matched)}",
        f"- **USDM-only:** {len(usdm_only)}",
        f"- **Hand-authored-only:** {len(ha_only)}",
        "",
    ]

    if usdm_only:
        lines += [
            "### USDM-only activities (not in hand-authored catalog)",
            "",
            "| id | title | archetype |",
            "|---|---|---|",
        ]
        for r in sorted(usdm_rows, key=lambda x: x.get("id", "")):
            if r.get("id") in usdm_only:
                lines.append(
                    f"| {r.get('id','')} | {r.get('title','')} | {r.get('archetype','')} |"
                )
        lines.append("")

    if ha_only:
        lines += [
            "### Hand-authored-only activities (not in USDM catalog)",
            "",
            "| id | title | archetype |",
            "|---|---|---|",
        ]
        for r in sorted(ha_rows, key=lambda x: x.get("id", "")):
            if r.get("id") in ha_only:
                lines.append(
                    f"| {r.get('id','')} | {r.get('title','')} | {r.get('archetype','')} |"
                )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section 3: Schedule reconciliation
# ---------------------------------------------------------------------------

# Regex to find definitionUri / definitionCanonical in FSH action blocks
_RE_DEF_URI = re.compile(
    r'\*\s+definitionUri\s*=\s*"([^"]+)"'
)
_RE_DEF_CANONICAL = re.compile(
    r'\*\s+definitionCanonical\s*=\s*(?:Canonical\(([^)]+)\)|"([^"]+)")'
)


def _ha_action_refs(fsh_content: str) -> set:
    """
    Extract all definitionUri / definitionCanonical values from a FSH file.
    Returns a set of bare resource ids (last path segment).
    """
    refs = set()
    for m in _RE_DEF_URI.finditer(fsh_content):
        val = m.group(1).split("/")[-1]
        refs.add(val)
    for m in _RE_DEF_CANONICAL.finditer(fsh_content):
        val = (m.group(1) or m.group(2) or "").split("/")[-1]
        refs.add(val)
    return refs


def section_schedule() -> str:
    matrix_rows = _load_csv(_MATRIX_CSV)
    if not matrix_rows:
        return (
            "## Section 3 — Schedule Reconciliation\n\n"
            "_`usdm-soa-matrix.csv` not found — run `python3 scripts/usdm_to_soa.py` first._\n"
        )

    # Build USDM matrix: visit_col → {activity_id, ...}
    all_cols = list(matrix_rows[0].keys())
    activity_col = all_cols[0]  # first column is activity id
    visit_cols = all_cols[1:]   # remaining columns are encounter names

    usdm_schedule: dict[str, set] = {vc: set() for vc in visit_cols}
    for row in matrix_rows:
        act_id = row.get(activity_col, "").strip()
        if not act_id:
            continue
        for vc in visit_cols:
            cell = row.get(vc, "").strip()
            if cell.startswith("X"):
                usdm_schedule[vc].add(act_id)

    # Build hand-authored schedule from visit FSH files
    ha_schedule: dict[str, set] = {}
    for enc_name, ha_visit_id in USDM_TO_HA_VISIT.items():
        fsh = _read_fsh(ha_visit_id)
        ha_schedule[enc_name] = _ha_action_refs(fsh)

    # Compare
    discrepancies = []
    for enc_name in visit_cols:
        if enc_name not in ha_schedule:
            continue
        usdm_set = usdm_schedule.get(enc_name, set())
        ha_set = ha_schedule.get(enc_name, set())
        usdm_only = usdm_set - ha_set
        ha_only = ha_set - usdm_set
        if usdm_only or ha_only:
            discrepancies.append((enc_name, sorted(usdm_only), sorted(ha_only)))

    lines = [
        "## Section 3 — Schedule Reconciliation",
        "",
        "Compares the USDM SoA matrix (`usdm-soa-matrix.csv`) against "
        "hand-authored visit FSH `definitionUri`/`definitionCanonical` refs.",
        "",
    ]

    if not discrepancies:
        lines.append("_No discrepancies found — USDM and hand-authored schedules agree._")
        lines.append("")
    else:
        lines += [
            f"**{len(discrepancies)} encounter(s) with discrepancies:**",
            "",
            "| Encounter | USDM-only activities | Hand-authored-only activities |",
            "|---|---|---|",
        ]
        for enc_name, usdm_only, ha_only in discrepancies:
            u_str = ", ".join(usdm_only) if usdm_only else "—"
            h_str = ", ".join(ha_only) if ha_only else "—"
            lines.append(f"| {enc_name} | {u_str} | {h_str} |")
        lines += [
            "",
            "> **Note:** Differences are expected during the USDM migration. "
            "The USDM catalog uses slugified ids; hand-authored refs use the "
            "full FSH instance id. This report surfaces them for human review; "
            "it does not resolve them automatically.",
            "",
        ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_report() -> str:
    doc = USDMDoc(str(_USDM_PATH))
    resolver = TimingResolver(doc)

    s1 = section_timing(doc, resolver)
    s2 = section_activities()
    s3 = section_schedule()

    return "\n".join([
        "# USDM Reconciliation Report",
        "",
        "> Generated by `scripts/usdm_reconcile.py`  ",
        f"> Source: `input/usdm/CDISC_Pilot_Study_v4_FIXED.json`",
        "",
        s1,
        s2,
        s3,
    ])


def main() -> None:
    if not _USDM_PATH.exists():
        print(f"FATAL: USDM file not found: {_USDM_PATH}", file=sys.stderr)
        sys.exit(1)

    report = generate_report()
    _OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _OUT_PATH.write_text(report, encoding="utf-8")
    print(f"Report written to: {_OUT_PATH}")


if __name__ == "__main__":
    main()
