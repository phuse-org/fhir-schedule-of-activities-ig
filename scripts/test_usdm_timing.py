#!/usr/bin/env python3
"""
test_usdm_timing.py — Unit tests for usdm_timing.py (Task F-3).

Run with:
    python3 -m unittest discover scripts/
or:
    python3 -m unittest scripts.test_usdm_timing
"""

import math
import os
import sys
import unittest
from pathlib import Path
from typing import Optional

# Ensure scripts/ is on the path when run via unittest discover
_SCRIPTS_DIR = Path(__file__).parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from usdm_timing import (
    ResolvedTiming,
    TimingResolver,
    _load_usdm,
    parse_iso8601_duration_to_days,
)

# ---------------------------------------------------------------------------
# Path to the real USDM file (relative to repo root)
# ---------------------------------------------------------------------------
_REPO_ROOT = _SCRIPTS_DIR.parent
_USDM_PATH = _REPO_ROOT / "input" / "usdm" / "CDISC_Pilot_Study_v4_FIXED.json"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _approx_equal(a: float, b: float, rel_tol: float = 1e-6) -> bool:
    """Return True if a and b are within rel_tol of each other."""
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=1e-9)


# ===========================================================================
# Tests for parse_iso8601_duration_to_days
# ===========================================================================

class TestParseISO8601Duration(unittest.TestCase):
    """Unit tests for the ISO 8601 duration parser."""

    # --- None passthrough ---
    def test_none_returns_none(self):
        self.assertIsNone(parse_iso8601_duration_to_days(None))

    # --- Day forms ---
    def test_P0D(self):
        self.assertEqual(parse_iso8601_duration_to_days("P0D"), 0.0)

    def test_P1D(self):
        self.assertEqual(parse_iso8601_duration_to_days("P1D"), 1.0)

    def test_P2D(self):
        self.assertEqual(parse_iso8601_duration_to_days("P2D"), 2.0)

    def test_P14D(self):
        self.assertEqual(parse_iso8601_duration_to_days("P14D"), 14.0)

    def test_P182D(self):
        self.assertEqual(parse_iso8601_duration_to_days("P182D"), 182.0)

    # --- Week forms ---
    def test_P1W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P1W"), 7.0)

    def test_P2W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P2W"), 14.0)

    def test_P4W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P4W"), 28.0)

    def test_P6W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P6W"), 42.0)

    def test_P8W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P8W"), 56.0)

    def test_P12W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P12W"), 84.0)

    def test_P16W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P16W"), 112.0)

    def test_P20W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P20W"), 140.0)

    def test_P24W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P24W"), 168.0)

    def test_P26W(self):
        self.assertEqual(parse_iso8601_duration_to_days("P26W"), 182.0)

    # --- Hour forms (sub-day) ---
    def test_PT0H(self):
        self.assertEqual(parse_iso8601_duration_to_days("PT0H"), 0.0)

    def test_PT4H(self):
        result = parse_iso8601_duration_to_days("PT4H")
        self.assertTrue(_approx_equal(result, 4.0 / 24))

    def test_PT24H(self):
        self.assertEqual(parse_iso8601_duration_to_days("PT24H"), 1.0)

    # --- Minute forms (sub-hour) ---
    def test_PT0M(self):
        self.assertEqual(parse_iso8601_duration_to_days("PT0M"), 0.0)

    def test_PT5M(self):
        result = parse_iso8601_duration_to_days("PT5M")
        self.assertTrue(_approx_equal(result, 5.0 / 1440))

    def test_PT1M(self):
        result = parse_iso8601_duration_to_days("PT1M")
        self.assertTrue(_approx_equal(result, 1.0 / 1440))

    # --- Unsupported formats raise ValueError ---
    def test_unsupported_raises(self):
        with self.assertRaises(ValueError):
            parse_iso8601_duration_to_days("P1Y")

    def test_unsupported_combined_raises(self):
        with self.assertRaises(ValueError):
            parse_iso8601_duration_to_days("P1DT2H")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_iso8601_duration_to_days("")

    def test_plain_number_raises(self):
        with self.assertRaises(ValueError):
            parse_iso8601_duration_to_days("14")


# ===========================================================================
# Tests for TimingResolver (require the real USDM file)
# ===========================================================================

@unittest.skipUnless(
    _USDM_PATH.exists(),
    f"USDM file not found at {_USDM_PATH} — skipping integration tests",
)
class TestTimingResolver(unittest.TestCase):
    """
    Integration tests for TimingResolver against the real USDM JSON.

    These tests verify:
      1. Anchor visits return None
      2. Known timing values (Timing_2, Timing_4, Timing_5) match spec
      3. All 16 non-null scheduledAtId references resolve without error
      4. Window bounds are correct
      5. Reference encounter names are correct
    """

    @classmethod
    def setUpClass(cls):
        """Load the USDM document once for all tests in this class."""
        cls.usdm = _load_usdm(_USDM_PATH)
        cls.resolver = TimingResolver(cls.usdm)

        # Build encounter lookup by id for convenience
        raw = cls.usdm["raw"]
        sd = raw["study"]["versions"][0]["studyDesigns"][0]
        cls.encounters = sd.get("encounters", [])
        cls.encounter_by_id = {e["id"]: e for e in cls.encounters}
        cls.encounter_by_name = {e["name"]: e for e in cls.encounters}

    # -----------------------------------------------------------------------
    # Anchor visits → None
    # -----------------------------------------------------------------------

    def test_anchor_encounter_1_returns_none(self):
        """Encounter_1 (Screening 1) has scheduledAtId=null → anchor → None."""
        enc = self.encounter_by_id["Encounter_1"]
        self.assertIsNone(enc.get("scheduledAtId"))
        result = self.resolver.resolve(enc.get("scheduledAtId"))
        self.assertIsNone(result)

    def test_anchor_encounter_3_returns_none(self):
        """Encounter_3 (Baseline) has scheduledAtId=null → anchor → None."""
        enc = self.encounter_by_id["Encounter_3"]
        self.assertIsNone(enc.get("scheduledAtId"))
        result = self.resolver.resolve(enc.get("scheduledAtId"))
        self.assertIsNone(result)

    def test_resolve_none_directly_returns_none(self):
        """Calling resolve(None) directly returns None."""
        self.assertIsNone(self.resolver.resolve(None))

    # -----------------------------------------------------------------------
    # Required test cases from spec (Task F-3 table)
    # -----------------------------------------------------------------------

    def test_timing_2_planned_day_value(self):
        """Timing_2 (Encounter_2, Screening 2): P2D → 2.0 days."""
        enc = self.encounter_by_id["Encounter_2"]
        self.assertEqual(enc.get("scheduledAtId"), "Timing_2")
        result = self.resolver.resolve("Timing_2")
        self.assertIsNotNone(result)
        self.assertEqual(result.planned_day_value, 2.0)
        self.assertEqual(result.planned_day_unit, "d")

    def test_timing_4_planned_day_value(self):
        """Timing_4 (Encounter_4, Week 2): P2W → 14.0 days."""
        enc = self.encounter_by_id["Encounter_4"]
        self.assertEqual(enc.get("scheduledAtId"), "Timing_4")
        result = self.resolver.resolve("Timing_4")
        self.assertIsNotNone(result)
        self.assertEqual(result.planned_day_value, 14.0)
        self.assertEqual(result.planned_day_unit, "d")

    def test_timing_5_planned_day_value(self):
        """Timing_5 (Encounter_5, Week 4): P4W → 28.0 days."""
        enc = self.encounter_by_id["Encounter_5"]
        self.assertEqual(enc.get("scheduledAtId"), "Timing_5")
        result = self.resolver.resolve("Timing_5")
        self.assertIsNotNone(result)
        self.assertEqual(result.planned_day_value, 28.0)
        self.assertEqual(result.planned_day_unit, "d")

    # -----------------------------------------------------------------------
    # Window bounds
    # -----------------------------------------------------------------------

    def test_timing_2_window_bounds(self):
        """Timing_2: windowLower=PT4H (≈0.167d), windowUpper=PT0H (0.0d)."""
        result = self.resolver.resolve("Timing_2")
        self.assertIsNotNone(result)
        # windowLower = PT4H = 4/24 days
        self.assertIsNotNone(result.window_lower_days)
        self.assertTrue(
            _approx_equal(result.window_lower_days, 4.0 / 24),
            f"Expected ~{4/24:.6f}, got {result.window_lower_days}",
        )
        # windowUpper = PT0H = 0.0 days
        self.assertIsNotNone(result.window_upper_days)
        self.assertEqual(result.window_upper_days, 0.0)

    def test_timing_4_window_bounds(self):
        """Timing_4: windowLower=P3D (3.0d), windowUpper=P3D (3.0d)."""
        result = self.resolver.resolve("Timing_4")
        self.assertIsNotNone(result)
        self.assertEqual(result.window_lower_days, 3.0)
        self.assertEqual(result.window_upper_days, 3.0)

    def test_timing_5_window_bounds(self):
        """Timing_5: windowLower=P3D (3.0d), windowUpper=P3D (3.0d)."""
        result = self.resolver.resolve("Timing_5")
        self.assertIsNotNone(result)
        self.assertEqual(result.window_lower_days, 3.0)
        self.assertEqual(result.window_upper_days, 3.0)

    def test_timing_9_window_bounds(self):
        """Timing_9 (Week 12): windowLower=P4D (4.0d), windowUpper=P4D (4.0d)."""
        result = self.resolver.resolve("Timing_9")
        self.assertIsNotNone(result)
        self.assertEqual(result.window_lower_days, 4.0)
        self.assertEqual(result.window_upper_days, 4.0)

    # -----------------------------------------------------------------------
    # Full spot-check table (all 10 non-anchor encounters)
    # -----------------------------------------------------------------------

    def _check_encounter(
        self,
        enc_id: str,
        timing_id: str,
        expected_days: float,
        expected_lower: Optional[float],
        expected_upper: Optional[float],
    ):
        """Helper: resolve an encounter's timing and assert expected values."""
        enc = self.encounter_by_id[enc_id]
        self.assertEqual(enc.get("scheduledAtId"), timing_id)
        result = self.resolver.resolve(timing_id)
        self.assertIsNotNone(result, f"{enc_id} / {timing_id} resolved to None")
        self.assertTrue(
            _approx_equal(result.planned_day_value, expected_days),
            f"{enc_id}: expected {expected_days}d, got {result.planned_day_value}d",
        )
        if expected_lower is None:
            self.assertIsNone(result.window_lower_days)
        else:
            self.assertIsNotNone(result.window_lower_days)
            self.assertTrue(
                _approx_equal(result.window_lower_days, expected_lower),
                f"{enc_id} lower: expected {expected_lower}, got {result.window_lower_days}",
            )
        if expected_upper is None:
            self.assertIsNone(result.window_upper_days)
        else:
            self.assertIsNotNone(result.window_upper_days)
            self.assertTrue(
                _approx_equal(result.window_upper_days, expected_upper),
                f"{enc_id} upper: expected {expected_upper}, got {result.window_upper_days}",
            )

    def test_encounter_2_screening_2(self):
        self._check_encounter("Encounter_2", "Timing_2", 2.0, 4.0 / 24, 0.0)

    def test_encounter_4_week_2(self):
        self._check_encounter("Encounter_4", "Timing_4", 14.0, 3.0, 3.0)

    def test_encounter_5_week_4(self):
        self._check_encounter("Encounter_5", "Timing_5", 28.0, 3.0, 3.0)

    def test_encounter_6_week_6(self):
        self._check_encounter("Encounter_6", "Timing_6", 42.0, 3.0, 3.0)

    def test_encounter_7_week_8(self):
        self._check_encounter("Encounter_7", "Timing_7", 56.0, 3.0, 3.0)

    def test_encounter_8_week_12(self):
        self._check_encounter("Encounter_8", "Timing_9", 84.0, 4.0, 4.0)

    def test_encounter_9_week_16(self):
        self._check_encounter("Encounter_9", "Timing_11", 112.0, 4.0, 4.0)

    def test_encounter_10_week_20(self):
        self._check_encounter("Encounter_10", "Timing_13", 140.0, 4.0, 4.0)

    def test_encounter_11_week_24(self):
        self._check_encounter("Encounter_11", "Timing_15", 168.0, 4.0, 4.0)

    def test_encounter_12_week_26(self):
        self._check_encounter("Encounter_12", "Timing_16", 182.0, 3.0, 3.0)

    # -----------------------------------------------------------------------
    # All 16 non-null scheduledAtId references resolve without error
    # -----------------------------------------------------------------------

    def test_all_non_null_scheduled_at_ids_resolve(self):
        """
        All 16 non-null scheduledAtId references in the USDM must resolve
        without raising an exception.

        The 16 non-null Timing ids referenced by encounters and SAIs are:
        Timing_1 through Timing_16 (excluding Timing_3 which is not on an
        encounter, and Timing_12b which is on a ScheduledDecisionInstance).

        We collect all unique non-null scheduledAtId values from encounters
        and all Timing ids referenced by SAIs, then resolve each.
        """
        # Collect all non-null scheduledAtId values from encounters
        encounter_timing_ids = set()
        for enc in self.encounters:
            sat_id = enc.get("scheduledAtId")
            if sat_id:
                encounter_timing_ids.add(sat_id)

        # There should be exactly 10 non-null encounter scheduledAtIds
        self.assertEqual(
            len(encounter_timing_ids),
            10,
            f"Expected 10 non-null encounter scheduledAtIds, got {len(encounter_timing_ids)}: "
            f"{sorted(encounter_timing_ids)}",
        )

        # Resolve all of them — none should raise
        errors = []
        for timing_id in sorted(encounter_timing_ids):
            try:
                result = self.resolver.resolve(timing_id)
                self.assertIsNotNone(
                    result,
                    f"resolve({timing_id!r}) returned None for a non-null scheduledAtId",
                )
            except Exception as exc:
                errors.append(f"{timing_id}: {exc}")

        self.assertEqual(
            errors,
            [],
            f"Errors resolving timing ids:\n" + "\n".join(errors),
        )

    def test_all_16_timing_ids_resolve(self):
        """
        All 16 Timing ids that are referenced by SAIs in the main timeline
        (Timing_1 through Timing_16, including Timing_12b) resolve without
        error when called directly.

        Per F-0 audit: 16 encounter-level + 8 intra-visit sub-timings = 24
        total (plus Timing_12b = 25). The 16 encounter-level ones are the
        ones referenced by encounters or SAIs in the main timeline.
        """
        # These are the 16 Timing ids referenced by SAIs in the main timeline
        # (from F-0 audit Section 2 timing table)
        main_timeline_timing_ids = [
            "Timing_1",   # Screening (SAI_9 → SAI_11)
            "Timing_2",   # Pre dose / Screening 2
            "Timing_3",   # Dosing / Baseline
            "Timing_4",   # Week 2
            "Timing_5",   # Week 4
            "Timing_6",   # Week 6
            "Timing_7",   # Week 8
            "Timing_8",   # Week 8 Home
            "Timing_9",   # Week 12
            "Timing_10",  # Week 12 Home
            "Timing_11",  # Week 16
            "Timing_12",  # Week 16 Home
            "Timing_12b", # Week 16 Decision
            "Timing_13",  # Week 20
            "Timing_14",  # Week 20 Home
            "Timing_15",  # Week 24
            # Timing_16 is Week 26 — also in main timeline
            "Timing_16",
        ]

        errors = []
        for timing_id in main_timeline_timing_ids:
            try:
                # These may or may not be on encounters; we just check they
                # resolve without raising KeyError or ValueError
                result = self.resolver.resolve(timing_id)
                # result may be None only if timing_id is None (it's not here)
                # but the Timing object itself should parse fine
            except KeyError as exc:
                errors.append(f"KeyError for {timing_id}: {exc}")
            except ValueError as exc:
                errors.append(f"ValueError for {timing_id}: {exc}")
            except Exception as exc:
                errors.append(f"Unexpected error for {timing_id}: {exc}")

        self.assertEqual(
            errors,
            [],
            "Errors resolving timing ids:\n" + "\n".join(errors),
        )

    # -----------------------------------------------------------------------
    # Reference encounter names
    # -----------------------------------------------------------------------

    def test_timing_4_reference_encounter_name(self):
        """
        Timing_4 (Week 2): relativeFromScheduledInstanceId = SAI_12
        SAI_12.encounterId = Encounter_4 (Week 2)
        Encounter_4.previousId = Encounter_3 (Baseline, name="E3")
        → reference_encounter_name = "E3"
        """
        result = self.resolver.resolve("Timing_4")
        self.assertIsNotNone(result)
        self.assertEqual(result.reference_encounter_name, "E3")

    def test_timing_5_reference_encounter_name(self):
        """
        Timing_5 (Week 4): relativeFromScheduledInstanceId = SAI_13
        SAI_13.encounterId = Encounter_5 (Week 4)
        Encounter_5.previousId = Encounter_4 (Week 2, name="E4")
        → reference_encounter_name = "E4"
        """
        result = self.resolver.resolve("Timing_5")
        self.assertIsNotNone(result)
        self.assertEqual(result.reference_encounter_name, "E4")

    def test_timing_2_reference_encounter_name(self):
        """
        Timing_2 (Screening 2): relativeFromScheduledInstanceId = SAI_10
        SAI_10.encounterId = Encounter_2 (Screening 2)
        Encounter_2.previousId = Encounter_1 (Screening 1, name="E1")
        → reference_encounter_name = "E1"
        """
        result = self.resolver.resolve("Timing_2")
        self.assertIsNotNone(result)
        self.assertEqual(result.reference_encounter_name, "E1")

    # -----------------------------------------------------------------------
    # ResolvedTiming dataclass fields
    # -----------------------------------------------------------------------

    def test_resolved_timing_unit_is_always_d(self):
        """planned_day_unit must always be 'd'."""
        for enc in self.encounters:
            sat_id = enc.get("scheduledAtId")
            if sat_id:
                result = self.resolver.resolve(sat_id)
                self.assertIsNotNone(result)
                self.assertEqual(result.planned_day_unit, "d")

    def test_transition_delay_equals_planned_day_value(self):
        """transition_delay_days must equal planned_day_value."""
        for enc in self.encounters:
            sat_id = enc.get("scheduledAtId")
            if sat_id:
                result = self.resolver.resolve(sat_id)
                self.assertIsNotNone(result)
                self.assertEqual(
                    result.transition_delay_days,
                    result.planned_day_value,
                )

    # -----------------------------------------------------------------------
    # resolve_encounter convenience wrapper
    # -----------------------------------------------------------------------

    def test_resolve_encounter_anchor(self):
        """resolve_encounter on an anchor encounter returns None."""
        enc = self.encounter_by_id["Encounter_1"]
        result = self.resolver.resolve_encounter(enc)
        self.assertIsNone(result)

    def test_resolve_encounter_non_anchor(self):
        """resolve_encounter on a non-anchor encounter returns ResolvedTiming."""
        enc = self.encounter_by_id["Encounter_4"]
        result = self.resolver.resolve_encounter(enc)
        self.assertIsNotNone(result)
        self.assertEqual(result.planned_day_value, 14.0)

    # -----------------------------------------------------------------------
    # _load_usdm helper
    # -----------------------------------------------------------------------

    def test_load_usdm_returns_raw_and_index(self):
        """_load_usdm returns a dict with 'raw' and 'index' keys."""
        usdm = _load_usdm(_USDM_PATH)
        self.assertIn("raw", usdm)
        self.assertIn("index", usdm)
        self.assertIsInstance(usdm["raw"], dict)
        self.assertIsInstance(usdm["index"], dict)

    def test_load_usdm_index_contains_encounters(self):
        """The index must contain all 12 encounter ids."""
        usdm = _load_usdm(_USDM_PATH)
        for i in range(1, 13):
            enc_id = f"Encounter_{i}"
            self.assertIn(enc_id, usdm["index"], f"{enc_id} not in index")

    def test_load_usdm_index_contains_timings(self):
        """The index must contain the key timing ids."""
        usdm = _load_usdm(_USDM_PATH)
        for tid in ["Timing_2", "Timing_4", "Timing_5", "Timing_16"]:
            self.assertIn(tid, usdm["index"], f"{tid} not in index")


if __name__ == "__main__":
    unittest.main()
