#!/usr/bin/env python3
"""
usdm_loader.py — USDM file loading and pre-flight validation.

Provides a single entry point for loading a USDM JSON file into the raw
dict used by the rest of the pipeline, with optional validation via the
``usdm4`` library when it is installed.

Public API
----------
load(path, *, validate=True, strict=False) -> dict
    Load a USDM JSON file.  Returns the raw parsed dict that USDMDoc expects.
    When ``validate=True`` and usdm4 is available, runs DDF rule validation
    before returning.  If ``strict=True`` any validation *errors* (not just
    warnings) cause a SystemExit.

validate_only(path) -> ValidationResult
    Run validation and return a structured result without loading the model.

ValidationResult
    Named tuple: (is_valid, finding_count, failures, text_report)

USDM4_AVAILABLE
    True if the usdm4 package is importable; False otherwise.
"""

import json
import sys
import warnings
from collections import namedtuple
from typing import Optional

# ---------------------------------------------------------------------------
# usdm4 availability check
# ---------------------------------------------------------------------------
try:
    from usdm4 import USDM4 as _USDM4Cls
    from simple_error_log.errors import Errors as _Errors

    USDM4_AVAILABLE = True
except ImportError:
    USDM4_AVAILABLE = False

# Singleton to avoid re-initialising USDM4 (which scans rule files) on every call
_usdm4_instance: Optional[object] = None


def _get_usdm4():
    global _usdm4_instance
    if _usdm4_instance is None:
        _usdm4_instance = _USDM4Cls()
    return _usdm4_instance


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------
ValidationResult = namedtuple(
    "ValidationResult",
    ["is_valid", "finding_count", "failures", "text_report"],
)


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

def load(path: str, *, validate: bool = True, strict: bool = False) -> dict:
    """
    Load a USDM JSON file and return the raw dict.

    Parameters
    ----------
    path     : Path to the USDM JSON file.
    validate : If True (default) and usdm4 is installed, run DDF rule
               validation and print a summary.  Failures are logged as
               warnings; set ``strict=True`` to exit on errors.
    strict   : If True, any validation *errors* (severity Error, not Warning)
               cause a non-zero SystemExit.  Has no effect when validate=False
               or usdm4 is not available.

    Returns
    -------
    dict  — the raw parsed USDM JSON, ready for USDMDoc(path) or direct use.
    """
    # Always load the raw JSON (the rest of the pipeline needs the dict)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if validate:
        if USDM4_AVAILABLE:
            result = _run_validation(path)
            _report_validation(result, strict=strict)
        else:
            warnings.warn(
                "usdm4 not installed — skipping USDM validation. "
                "Run: pip install usdm4  (see requirements-optional.txt)",
                stacklevel=2,
            )

    return data


def validate_only(path: str) -> ValidationResult:
    """
    Run usdm4 rule validation on a USDM file without loading it into USDMDoc.

    Returns a ValidationResult.  Raises ImportError if usdm4 is not installed.
    """
    if not USDM4_AVAILABLE:
        raise ImportError(
            "usdm4 is required for USDM validation. "
            "Install it with: pip install usdm4"
        )
    return _run_validation(path)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _run_validation(path: str) -> ValidationResult:
    """Run usdm4 DDF rule validation and return a structured result."""
    u = _get_usdm4()
    results = u.validate(path)

    failures = {
        rid: outcome
        for rid, outcome in results.outcomes.items()
        if outcome.status.value == "Failure"
    }

    return ValidationResult(
        is_valid=results.is_valid,
        finding_count=results.finding_count,
        failures=failures,
        text_report=results.format_text(),
    )


def _report_validation(result: ValidationResult, *, strict: bool = False) -> None:
    """Print a concise validation summary; exit if strict and errors found."""
    n_fail = len(result.failures)
    n_findings = result.finding_count

    if n_fail == 0:
        print(f"  USDM validation: PASSED ({n_findings} findings)")
        return

    print(f"  USDM validation: {n_fail} rule failure(s), {n_findings} finding(s)")

    # Classify failures into errors vs warnings
    errors = []
    warns = []
    for rid, outcome in result.failures.items():
        errs = outcome.errors
        items = errs._items if hasattr(errs, "_items") else (
            errs.items if hasattr(errs, "items") and not callable(errs.items) else []
        )
        for item in items:
            severity = getattr(item, "severity", None) or str(item)
            msg = getattr(item, "message", None) or str(item)
            loc = getattr(item, "location", {}) or {}
            path_str = loc.get("path", "") if isinstance(loc, dict) else ""
            rule_text = loc.get("rule_text", "") if isinstance(loc, dict) else ""
            entry = f"  [{rid}] {msg}"
            if rule_text:
                entry += f"\n    Rule: {rule_text}"
            if path_str:
                entry += f"\n    Path: {path_str}"
            # Check severity — usdm4 items have .severity or type string
            sev_str = str(severity).lower()
            if "error" in sev_str and "warning" not in sev_str:
                errors.append(entry)
            else:
                warns.append(entry)

    if warns:
        print(f"  Warnings ({len(warns)}):")
        for w in warns:
            print(f"    {w}")
    if errors:
        print(f"  Errors ({len(errors)}):")
        for e in errors:
            print(f"    {e}")

    if strict and errors:
        print(
            "\nFATAL: USDM validation errors found and --strict mode is active. "
            "Fix the USDM file before running the pipeline.",
            file=sys.stderr,
        )
        sys.exit(1)
    elif errors:
        warnings.warn(
            f"{len(errors)} USDM validation error(s) found. "
            "The pipeline will continue but output may be incorrect. "
            "Run 'task validate' for the full report.",
            stacklevel=3,
        )
