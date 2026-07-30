#!/usr/bin/env python3
"""
usdm_timing.py — TimingResolver and ResolvedTiming for USDM v4 JSON.

Standalone module for Phase F Task F-3.  After F-1 is committed and F-8
merges everything, this module will be folded into usdm_reader.py.

stdlib only — no third-party imports.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


# ---------------------------------------------------------------------------
# ISO 8601 duration parser (stdlib only)
# ---------------------------------------------------------------------------

def parse_iso8601_duration_to_days(s: Optional[str]) -> Optional[float]:
    """
    Parse an ISO 8601 duration string to a float number of days.

    Supported formats:
      P<n>W  — weeks (× 7)
      P<n>D  — days
      PT<n>H — hours (÷ 24)
      PT<n>M — minutes (÷ 1440)

    Returns None if s is None.
    Raises ValueError for unsupported formats.

    Examples:
      >>> parse_iso8601_duration_to_days("P2D")
      2.0
      >>> parse_iso8601_duration_to_days("P2W")
      14.0
      >>> parse_iso8601_duration_to_days("PT4H")
      0.16666666666666666
      >>> parse_iso8601_duration_to_days("PT0H")
      0.0
      >>> parse_iso8601_duration_to_days(None) is None
      True
    """
    if s is None:
        return None
    # Week form: P<n>W
    m = re.fullmatch(r"P(\d+(?:\.\d+)?)W", s)
    if m:
        return float(m.group(1)) * 7
    # Day form: P<n>D
    m = re.fullmatch(r"P(\d+(?:\.\d+)?)D", s)
    if m:
        return float(m.group(1))
    # Hour form: PT<n>H
    m = re.fullmatch(r"PT(\d+(?:\.\d+)?)H", s)
    if m:
        return float(m.group(1)) / 24
    # Minute form: PT<n>M
    m = re.fullmatch(r"PT(\d+(?:\.\d+)?)M", s)
    if m:
        return float(m.group(1)) / 1440
    raise ValueError(f"Unsupported ISO 8601 duration: {s!r}")


# ---------------------------------------------------------------------------
# ResolvedTiming dataclass
# ---------------------------------------------------------------------------

@dataclass
class ResolvedTiming:
    """
    Resolved timing values for a single encounter.

    planned_day_value       — numeric duration from the reference encounter (days)
    planned_day_unit        — always "d"
    transition_delay_days   — same as planned_day_value (the Timing.value in days)
    window_lower_days       — lower window bound in days, or None
    window_upper_days       — upper window bound in days, or None
    reference_encounter_name — FHIR name (e.g. "E3") of the reference encounter,
                               or None when no relativeFromScheduledInstanceId is set
    """
    planned_day_value: float
    planned_day_unit: str          # always "d"
    transition_delay_days: float
    window_lower_days: Optional[float]
    window_upper_days: Optional[float]
    reference_encounter_name: Optional[str]


# ---------------------------------------------------------------------------
# _load_usdm — standalone loader / indexer
# ---------------------------------------------------------------------------

def _load_usdm(path: Union[str, Path]) -> dict:
    """
    Load a USDM v4 JSON file and return a dict with:
      "raw"   — the full parsed JSON
      "index" — flat id → object mapping for O(1) resolution

    This mirrors the USDMDoc._build_index logic so TimingResolver can work
    standalone (before F-8 merges everything into USDMDoc).
    """
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)

    index: dict[str, dict] = {}

    def _walk(node) -> None:
        if isinstance(node, dict):
            node_id = node.get("id")
            if node_id and isinstance(node_id, str):
                index[node_id] = node
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(raw)
    return {"raw": raw, "index": index}


# ---------------------------------------------------------------------------
# TimingResolver
# ---------------------------------------------------------------------------

class TimingResolver:
    """
    Resolves encounter timing from a USDM document.

    Accepts either:
      - a pre-loaded dict (as returned by _load_usdm), or
      - a USDMDoc instance (from usdm_reader.py — duck-typed via .resolve()
        and .encounters())

    Usage (standalone):
        usdm = _load_usdm("path/to/usdm.json")
        resolver = TimingResolver(usdm)
        timing = resolver.resolve(encounter["scheduledAtId"])

    Usage (with USDMDoc from F-1):
        doc = USDMDoc("path/to/usdm.json")
        resolver = TimingResolver(doc)
        timing = resolver.resolve(encounter["scheduledAtId"])
    """

    def __init__(self, usdm_doc) -> None:
        # Support both a pre-loaded dict and a USDMDoc instance.
        if isinstance(usdm_doc, dict) and "index" in usdm_doc:
            # Standalone mode: dict from _load_usdm()
            self._index: dict[str, dict] = usdm_doc["index"]
            raw = usdm_doc["raw"]
            sd = raw["study"]["versions"][0]["studyDesigns"][0]
            self._encounters: list[dict] = sd.get("encounters", [])
        else:
            # USDMDoc mode: duck-type the interface
            self._index = usdm_doc._index
            self._encounters = usdm_doc.encounters()

        # Build encounter-id → encounter map for fast lookup
        self._encounter_by_id: dict[str, dict] = {
            e["id"]: e for e in self._encounters
        }

        # Build SAI-id → encounter map:
        # For each encounter, find all SAIs whose encounterId == encounter.id
        # We need this to resolve relativeFromScheduledInstanceId → encounter.
        # Strategy: walk all SAIs in all timelines and map sai.id → encounter.
        self._sai_to_encounter: dict[str, dict] = {}
        self._build_sai_encounter_map()

    def _resolve(self, obj_id: str) -> dict:
        """Resolve an id to its object, raising KeyError if not found."""
        if obj_id not in self._index:
            raise KeyError(f"USDM id not found: {obj_id!r}")
        return self._index[obj_id]

    def _build_sai_encounter_map(self) -> None:
        """
        Walk all ScheduledActivityInstance objects in the index and map
        each SAI id to its encounter (via SAI.encounterId).

        Note: the USDM field is 'encounterId' (singular), not 'encounterIds'.
        """
        for obj_id, obj in self._index.items():
            if obj.get("instanceType") == "ScheduledActivityInstance":
                enc_id = obj.get("encounterId")
                if enc_id and enc_id in self._encounter_by_id:
                    self._sai_to_encounter[obj_id] = self._encounter_by_id[enc_id]

    def resolve(self, scheduled_at_id: Optional[str]) -> Optional[ResolvedTiming]:
        """
        Resolve a Timing object reference to a ResolvedTiming.

        Returns None for anchor visits (scheduled_at_id is None).

        Algorithm (per F-0 audit §3.2):
          1. If scheduled_at_id is None → anchor visit → return None
          2. Look up the Timing object
          3. Parse Timing.value → planned_day_value (days)
          4. Parse Timing.windowLower / windowUpper → window bounds (days)
          5. Resolve reference encounter:
             - Timing.relativeFromScheduledInstanceId → SAI id
             - SAI.encounterId → encounter
             - That encounter's .previousId → reference encounter
             (The relativeFromScheduledInstanceId points to the SAI for the
              encounter being scheduled; the reference is the prior encounter.)
          6. Return ResolvedTiming
        """
        if scheduled_at_id is None:
            return None

        # Step 2: look up Timing object
        timing = self._resolve(scheduled_at_id)

        # Step 3: parse planned day value
        planned_day_value = parse_iso8601_duration_to_days(timing.get("value"))
        if planned_day_value is None:
            raise ValueError(
                f"Timing {scheduled_at_id!r} has no 'value' field"
            )

        # Step 4: parse window bounds
        window_lower_days = parse_iso8601_duration_to_days(
            timing.get("windowLower")
        )
        window_upper_days = parse_iso8601_duration_to_days(
            timing.get("windowUpper")
        )

        # Step 5: resolve reference encounter name
        reference_encounter_name: Optional[str] = None
        rel_sai_id = timing.get("relativeFromScheduledInstanceId")
        if rel_sai_id:
            # rel_sai_id is the SAI for the encounter being scheduled.
            # The reference encounter is the encounter that this SAI belongs to,
            # then we follow encounter.previousId to get the reference.
            #
            # Per F-0 audit §3.5 implementation note:
            #   "encounter.previousId gives the reference encounter id directly."
            #
            # So: find the encounter that owns rel_sai_id, then use its previousId.
            sai_encounter = self._sai_to_encounter.get(rel_sai_id)
            if sai_encounter is not None:
                prev_enc_id = sai_encounter.get("previousId")
                if prev_enc_id and prev_enc_id in self._encounter_by_id:
                    ref_enc = self._encounter_by_id[prev_enc_id]
                    reference_encounter_name = ref_enc.get("name")

        return ResolvedTiming(
            planned_day_value=planned_day_value,
            planned_day_unit="d",
            transition_delay_days=planned_day_value,
            window_lower_days=window_lower_days,
            window_upper_days=window_upper_days,
            reference_encounter_name=reference_encounter_name,
        )

    def resolve_encounter(self, encounter: dict) -> Optional[ResolvedTiming]:
        """
        Convenience wrapper: resolve timing for a full encounter dict.

        Returns None for anchor visits (encounter.scheduledAtId is None).
        """
        return self.resolve(encounter.get("scheduledAtId"))
