#!/usr/bin/env python3
"""
usdm_validate.py — Standalone USDM validation CLI.

Usage:
    python3 scripts/usdm_validate.py <path-to-usdm.json>

Exit codes:
    0 — validation passed
    1 — validation failed or usdm4 not installed
"""
import sys
import pathlib

_SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from usdm_loader import validate_only, USDM4_AVAILABLE  # noqa: E402

if not USDM4_AVAILABLE:
    print(
        "ERROR: usdm4 is not installed.\n"
        "Install it with:  pip install -r requirements-optional.txt",
        file=sys.stderr,
    )
    sys.exit(1)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <usdm-file.json>", file=sys.stderr)
    sys.exit(1)

result = validate_only(sys.argv[1])
print(result.text_report)
sys.exit(0 if result.is_valid else 1)
