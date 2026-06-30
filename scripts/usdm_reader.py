#!/usr/bin/env python3
"""
USDMDoc — loader, indexer, and FSH emitter for USDM v4 JSON.

Foundation module for Phase F (Tasks F-1 through F-8).
stdlib only — no third-party imports.
"""

import json
import os
import re
import html
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# CDISC → FHIR phase code mapping
# ---------------------------------------------------------------------------
CDISC_PHASE_MAP: dict[str, str] = {
    "C15600": "phase-1",       # Phase I Trial
    "C15601": "phase-2",       # Phase II Trial
    "C15602": "phase-3",       # Phase III Trial
    "C15603": "phase-4",       # Phase IV Trial
    "C198388": "phase-1-phase-2",  # Phase I/II
    "C15693": "phase-2-phase-3",   # Phase II/III
    "C48660": "n-a",           # Not Applicable
    "C25301": "early-phase-1", # Early Phase 1
}

# CDISC arm type → FHIR comparisonGroup.type
CDISC_ARM_TYPE_MAP: dict[str, str] = {
    "C174268": "placebo-comparator",   # Placebo Control Arm
    "C174267": "active-comparator",    # Active Comparator Arm
    "C174266": "experimental",         # Experimental Arm
    "C174269": "sham-comparator",      # Sham Comparator Arm
    "C174270": "no-intervention",      # No Intervention Arm
    "C174271": "other",                # Other Arm
}

# CDISC code system → FHIR system URI
CDISC_CODE_SYSTEM_MAP: dict[str, str] = {
    "ICD-10-CM": "http://hl7.org/fhir/sid/icd-10-cm",
    "SNOMED": "http://snomed.info/sct",
    "LOINC": "http://loinc.org",
    "http://www.cdisc.org": "http://www.cdisc.org",
    "SPONSOR": "http://example.org/sponsor",
}

# ---------------------------------------------------------------------------
# HTML stripping helper
# ---------------------------------------------------------------------------
_HTML_TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text: str) -> str:
    """Remove HTML tags and unescape HTML entities."""
    if not text:
        return ""
    text = _HTML_TAG_RE.sub("", text)
    text = html.unescape(text)
    return text.strip()


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
# USDMDoc
# ---------------------------------------------------------------------------
class USDMDoc:
    """
    Loads a USDM v4 JSON file and builds a flat id→object index for O(1)
    resolution of any object by its "id" field.

    All accessor methods return live references into the parsed JSON dict.
    """

    def __init__(self, path: str) -> None:
        self._path = path
        with open(path, encoding="utf-8") as fh:
            self._raw: dict = json.load(fh)

        # Build flat id → object index by walking the entire document tree
        self._index: dict[str, dict] = {}
        self._build_index(self._raw)

    # ------------------------------------------------------------------
    # Index builder
    # ------------------------------------------------------------------
    def _build_index(self, node) -> None:
        """Recursively walk the JSON tree and index every object with an 'id'."""
        if isinstance(node, dict):
            node_id = node.get("id")
            if node_id and isinstance(node_id, str):
                self._index[node_id] = node
            for value in node.values():
                self._build_index(value)
        elif isinstance(node, list):
            for item in node:
                self._build_index(item)

    # ------------------------------------------------------------------
    # Core accessors
    # ------------------------------------------------------------------
    def resolve(self, obj_id: str) -> dict:
        """Return the object with the given id, or raise KeyError."""
        if obj_id not in self._index:
            raise KeyError(f"USDM id not found: {obj_id!r}")
        return self._index[obj_id]

    def study(self) -> dict:
        """Return the root study object."""
        return self._raw["study"]

    def study_version(self) -> dict:
        """Return versions[0]."""
        return self.study()["versions"][0]

    def study_design(self) -> dict:
        """Return versions[0].studyDesigns[0]."""
        return self.study_version()["studyDesigns"][0]

    def encounters(self) -> list:
        """Return all Encounter objects from the study design."""
        return self.study_design().get("encounters", [])

    def activities(self) -> list:
        """Return all Activity objects from the study design."""
        return self.study_design().get("activities", [])

    def schedule_timelines(self) -> list:
        """Return all ScheduleTimeline objects from the study design."""
        return self.study_design().get("scheduleTimelines", [])

    def bc_surrogates(self) -> list:
        """Return all BiomedicalConceptSurrogate objects from the study design."""
        return self.study_design().get("bcSurrogates", [])

    def biomedical_concepts(self) -> list:
        """Return all BiomedicalConcept objects from the study design."""
        return self.study_design().get("biomedicalConcepts", [])

    def organizations(self) -> list:
        """Return all Organization objects from the study version."""
        return self.study_version().get("organizations", [])

    def roles(self) -> list:
        """Return all StudyRole objects from the study version."""
        return self.study_version().get("roles", [])

    def sponsor_org(self) -> Optional[dict]:
        """Return the first Organization with type code C70793 (Sponsor)."""
        for org in self.organizations():
            type_obj = org.get("type") or {}
            std = type_obj.get("standardCode") or type_obj
            if std.get("code") == "C70793":
                return org
        return None

    def investigator_persons(self) -> list:
        """
        Return all AssignedPerson objects from roles with code C25936 (Investigator).
        Per F-0 audit: persons live under studyRoles[*].assignedPersons.
        """
        persons = []
        for role in self.roles():
            code_obj = role.get("code") or {}
            if code_obj.get("code") == "C25936":
                persons.extend(role.get("assignedPersons", []))
        return persons


# ---------------------------------------------------------------------------
# FSH helpers
# ---------------------------------------------------------------------------
def _fsh_header() -> str:
    return "// DO NOT EDIT — generated by scripts/usdm_to_soa.py\n"


def _code_system_uri(raw_system: str) -> str:
    """Map a USDM codeSystem string to a FHIR system URI."""
    return CDISC_CODE_SYSTEM_MAP.get(raw_system, raw_system)


def _fsh_escape(text: str) -> str:
    """Escape a string for use inside FSH double-quoted literals."""
    # Escape backslashes first, then double-quotes
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    return text


# ---------------------------------------------------------------------------
# emit_research_study
# ---------------------------------------------------------------------------
def emit_research_study(doc: USDMDoc, out_path: str) -> None:
    """
    Generate ResearchStudy.gen.fsh from the USDM document.

    Emits:
      - Organization instance for the sponsor (LILLY)
      - Practitioner instance for the principal investigator
      - ResearchStudy instance H2Q-MC-LZZT-ResearchStudy-USDM

    The output file is written atomically (write to temp, rename) to ensure
    idempotency: two runs on unchanged input produce byte-identical output.
    """
    lines: list[str] = []

    sv = doc.study_version()
    sd = doc.study_design()

    # ------------------------------------------------------------------
    # Sponsor Organization
    # ------------------------------------------------------------------
    sponsor = doc.sponsor_org()
    if sponsor:
        org_id = "LILLY-USDM"
        org_name = sponsor.get("name", "")
        org_label = sponsor.get("label", "")
        org_identifier = sponsor.get("identifier", "")
        org_scheme = sponsor.get("identifierScheme", "")

        lines += [
            _fsh_header(),
            "// ============================================================",
            "// Sponsor Organization (USDM-derived)",
            "// ============================================================",
            f'Instance: {org_id}',
            "InstanceOf: Organization",
            f'Title: "{_fsh_escape(org_label or org_name)}"',
            "Usage: #example",
            f'* name = "{_fsh_escape(org_name)}"',
        ]
        if org_label:
            lines.append(f'* alias[+] = "{_fsh_escape(org_label)}"')
        if org_identifier:
            lines.append(f'* identifier[+].value = "{_fsh_escape(org_identifier)}"')
            if org_scheme:
                lines.append(f'* identifier[=].system = "http://example.org/id/{org_scheme.lower()}"')
        # type: Sponsor
        lines += [
            "* type[+]",
            '  * coding[+]',
            '    * system = "http://www.cdisc.org"',
            '    * code = #C70793',
            '    * display = "Sponsor"',
            "",
        ]

    # ------------------------------------------------------------------
    # Principal Investigator Practitioner
    # ------------------------------------------------------------------
    pi_persons = doc.investigator_persons()
    pi_fhir_id = None
    if pi_persons:
        pi = pi_persons[0]
        pi_fhir_id = pi.get("id", "Pers-001")  # e.g. "Pers_001"
        # FHIR ids may not contain underscores — replace with hyphens
        pi_fhir_id = pi_fhir_id.replace("_", "-")
        pn = pi.get("personName") or {}
        pi_text = pn.get("text", "")
        pi_family = pn.get("familyName", "")
        pi_given = pn.get("givenNames", [])
        pi_job = pi.get("jobTitle", "")

        lines += [
            "// ============================================================",
            "// Principal Investigator Practitioner (USDM-derived)",
            "// ============================================================",
            f"Instance: {pi_fhir_id}",
            "InstanceOf: Practitioner",
            f'Title: "{_fsh_escape(pi_text or pi_family)}"',
            "Usage: #example",
            "* active = true",
        ]
        if pi_text or pi_family:
            lines.append("* name[+]")
            if pi_text:
                lines.append(f'  * text = "{_fsh_escape(pi_text)}"')
            if pi_family:
                lines.append(f'  * family = "{_fsh_escape(pi_family)}"')
            for gn in pi_given:
                lines.append(f'  * given[+] = "{_fsh_escape(gn)}"')
        if pi_job:
            lines += [
                "* qualification[+]",
                "  * code",
                f'    * text = "{_fsh_escape(pi_job)}"',
            ]
        lines.append("")

    # ------------------------------------------------------------------
    # ResearchStudy
    # ------------------------------------------------------------------
    study = doc.study()
    study_title = study.get("name", "")
    study_version_id = sv.get("versionIdentifier", "")

    # Identifiers
    identifiers = sv.get("studyIdentifiers", [])

    # Phase
    phase_alias = sd.get("studyPhase") or {}
    phase_std = phase_alias.get("standardCode") or {}
    phase_cdisc_code = phase_std.get("code", "")
    fhir_phase = CDISC_PHASE_MAP.get(phase_cdisc_code, "n-a")

    # Indications → condition
    indications = sd.get("indications", [])

    # Therapeutic areas → focus
    therapeutic_areas = sd.get("therapeuticAreas", [])

    # Arms → comparisonGroup
    arms = sd.get("arms", [])

    # Objectives
    objectives = sd.get("objectives", [])

    lines += [
        "// ============================================================",
        "// ResearchStudy (USDM-derived)",
        "// ============================================================",
        "Instance: H2Q-MC-LZZT-ResearchStudy-USDM",
        "InstanceOf: ResearchStudy",
        f'Title: "{_fsh_escape(study_title)}"',
        "Usage: #example",
        f'* title = "{_fsh_escape(study_title)}"',
        f'* version = "{_fsh_escape(study_version_id)}"',
        "* status = #active",
        f"* phase = #{fhir_phase}",
    ]

    # Identifiers
    for si in identifiers:
        si_text = si.get("text", "")
        si_scope = si.get("scopeId", "")
        # Determine system from scope org type
        si_system = "http://example.org/study-id"
        if si_scope == "Organization_2":
            si_system = "https://clinicaltrials.gov/show/"
        lines += [
            "* identifier[+]",
            f'  * value = "{_fsh_escape(si_text)}"',
            f'  * system = "{si_system}"',
        ]
        if si_scope and si_scope == "Organization_1" and sponsor:
            lines.append(f'  * assigner = Reference(Organization/LILLY-USDM)')

    # Sponsor reference
    if sponsor:
        lines += [
            "* associatedParty[+]",
            "  * party = Reference(Organization/LILLY-USDM)",
            '  * role = #lead-sponsor',
        ]

    # Principal investigator reference
    if pi_fhir_id:
        lines += [
            "* associatedParty[+]",
            f"  * party = Reference(Practitioner/{pi_fhir_id})",
            '  * role = #primary-investigator',
        ]

    # Conditions (indications)
    for ind in indications:
        for code_obj in ind.get("codes", []):
            code_val = code_obj.get("code", "")
            code_sys_raw = code_obj.get("codeSystem", "")
            code_sys = _code_system_uri(code_sys_raw)
            code_display = code_obj.get("decode", "")
            lines += [
                "* condition[+]",
                "  * coding[+]",
                f'    * system = "{code_sys}"',
                f'    * code = #{code_val}',
                f'    * display = "{_fsh_escape(code_display)}"',
            ]

    # Focus (therapeutic areas)
    # focus is CodeableReference in R6 — use .concept.coding (not .coding directly)
    for ta in therapeutic_areas:
        ta_code = ta.get("code", "")
        ta_sys_raw = ta.get("codeSystem", "")
        ta_sys = _code_system_uri(ta_sys_raw)
        ta_display = ta.get("decode", "")
        lines += [
            "* focus[+]",
            "  * concept",
            "    * coding[+]",
            f'      * system = "{ta_sys}"',
            f'      * code = #{ta_code}',
            f'      * display = "{_fsh_escape(ta_display)}"',
        ]

    # Comparison groups (arms)
    # In FHIR R6 ballot3, comparisonGroup has no .name, .description, or .type —
    # those were added in ballot4.  Emit only the backbone element itself.
    for arm in arms:
        lines += [
            "* comparisonGroup[+]",
        ]

    # Objectives
    for obj in objectives:
        obj_text_raw = obj.get("text", "") or obj.get("description", "")
        obj_text = strip_html(obj_text_raw)
        level_obj = obj.get("level") or {}
        level_code = level_obj.get("code", "")
        # C85826 = Primary, C85827 = Secondary
        if level_code == "C85826":
            fhir_obj_type = "#primary"
        elif level_code == "C85827":
            fhir_obj_type = "#secondary"
        else:
            fhir_obj_type = "#exploratory"

        lines += [
            "* objective[+]",
            f'  * name = "{_fsh_escape(obj_text)}"',
            f"  * type = {fhir_obj_type}",
        ]

    lines.append("")

    # ------------------------------------------------------------------
    # Write output (atomic: write to .tmp then rename for idempotency)
    # ------------------------------------------------------------------
    _write_fsh(out_path, lines)


def _write_fsh(out_path: str, lines: list) -> None:
    """Write FSH lines to out_path atomically (write to .tmp then rename)."""
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    content = "\n".join(lines)
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    os.replace(tmp_path, out_path)


# ---------------------------------------------------------------------------
# emit_eligibility_groups
# ---------------------------------------------------------------------------

# CDISC category codes for inclusion / exclusion
_INCLUSION_CODE = "C25532"
_EXCLUSION_CODE = "C25370"

# Regex to strip <usdm:tag .../> and other XML-like tags not caught by the
# generic HTML stripper (which already handles <tag> and </tag>).
_USDM_TAG_RE = re.compile(r"<usdm:[^>]+>", re.IGNORECASE)


def _strip_criterion_text(raw_text: str) -> str:
    """
    Strip HTML tags, <usdm:tag> elements, and HTML entities from criterion text.
    Collapses internal whitespace to single spaces.
    """
    if not raw_text:
        return ""
    # Remove <usdm:...> tags first (not caught by the generic HTML stripper
    # because they contain a colon in the tag name)
    text = _USDM_TAG_RE.sub("", raw_text)
    # Remove remaining HTML tags and unescape entities
    text = strip_html(text)
    # Collapse runs of whitespace (newlines, tabs, multiple spaces) to a
    # single space so multi-paragraph items become a single readable line.
    text = re.sub(r"\s+", " ", text).strip()
    return text


def emit_eligibility_groups(doc: USDMDoc, out_path: str) -> None:
    """
    Generate Eligibility.gen.fsh from the USDM document.

    Emits two Group instances:
      - H2Q-MC-LZZT-ResearchStudy-Inclusion-USDM  (category C25532)
      - H2Q-MC-LZZT-ResearchStudy-Exclusion-USDM  (category C25370)

    Each EligibilityCriterion in studyDesigns[0].population.criterionIds
    becomes one Group.characteristic entry.  The criterion text is taken
    from the linked EligibilityCriterionItem.text (HTML-stripped); if that
    is empty the criterion label is used as a fallback.

    The FSH structure matches the hand-authored
    H2Q-MC-LZZT-ResearchStudy-Eligibility.fsh exactly.
    """
    sd = doc.study_design()
    population = sd.get("population") or {}
    criterion_ids: list = population.get("criterionIds", [])

    # Resolve all criteria and split by category
    inclusion: list[dict] = []
    exclusion: list[dict] = []

    for cid in criterion_ids:
        criterion = doc.resolve(cid)
        cat_code = (criterion.get("category") or {}).get("code", "")
        if cat_code == _INCLUSION_CODE:
            inclusion.append(criterion)
        elif cat_code == _EXCLUSION_CODE:
            exclusion.append(criterion)
        # Unknown category: skip silently (none expected in this file)

    lines: list[str] = [_fsh_header()]

    def _emit_group(
        instance_id: str,
        title: str,
        description: str,
        criteria: list[dict],
        exclude_flag: bool,
        first: bool = False,
    ) -> None:
        # Add a blank separator line before each group (but not before the
        # very first one, since the header already ends with \n which provides
        # one blank line when joined).
        if not first:
            lines.append("")
        lines.extend([
            "// ============================================================",
            f"// {title}",
            "// ============================================================",
            f"Instance: {instance_id}",
            "InstanceOf: Group",
            f'Title: "{_fsh_escape(title)}"',
            f'Description: "{_fsh_escape(description)}"',
            "Usage: #example",
            "* type = #person",
            "* membership = #definitional",
        ])
        for criterion in criteria:
            # Resolve the linked EligibilityCriterionItem for the text
            item_id = criterion.get("criterionItemId")
            raw_text = ""
            if item_id:
                try:
                    item = doc.resolve(item_id)
                    raw_text = item.get("text") or ""
                except KeyError:
                    pass

            text = _strip_criterion_text(raw_text)
            # Fallback to criterion label if text is empty after stripping
            if not text:
                text = criterion.get("label") or criterion.get("name") or ""

            exclude_str = "true" if exclude_flag else "false"
            lines.extend([
                f'* characteristic[+].code.text = "{_fsh_escape(text)}"',
                f"* characteristic[=].exclude = {exclude_str}",
                "* characteristic[=].valueBoolean = true",
            ])

    _emit_group(
        instance_id="H2Q-MC-LZZT-ResearchStudy-Inclusion-USDM",
        title="H2Q-MC-LZZT Inclusion Criteria (USDM-derived)",
        description="H2Q-MC-LZZT Inclusion Criteria (USDM-derived)",
        criteria=inclusion,
        exclude_flag=False,
        first=True,
    )

    _emit_group(
        instance_id="H2Q-MC-LZZT-ResearchStudy-Exclusion-USDM",
        title="H2Q-MC-LZZT Exclusion Criteria (USDM-derived)",
        description="H2Q-MC-LZZT Exclusion Criteria (USDM-derived)",
        criteria=exclusion,
        exclude_flag=True,
        first=False,
    )

    lines.append("")

    _write_fsh(out_path, lines)


# ---------------------------------------------------------------------------
# emit_visit_plan_definitions
# ---------------------------------------------------------------------------

# soaTimePointSubType derivation table (checked in order)
_SUBTYPE_RULES: list[tuple[str, str]] = [
    ("Screening", "screening"),
    ("Baseline", "baseline"),
    ("Early Termination", "early-termination"),
    ("Retreatment", "retreatment"),
]


def _derive_subtype(label: str) -> str:
    """
    Derive soaTimePointSubType from encounter label.

    | Encounter label contains | soaTimePointSubType   |
    |--------------------------|----------------------|
    | "Screening"              | "screening"          |
    | "Baseline"               | "baseline"           |
    | "Early Termination"      | "early-termination"  |
    | "Retreatment"            | "retreatment"        |
    | Anything else            | "planned"            |
    """
    for keyword, subtype in _SUBTYPE_RULES:
        if keyword in label:
            return subtype
    return "planned"


def _fmt_days(value: float) -> str:
    """
    Format a float day value for FSH output.

    Whole numbers are emitted as integers (e.g. 14.0 → "14").
    Fractional values are emitted with up to 6 significant decimal places,
    trailing zeros stripped (e.g. 0.16666666666666666 → "0.166667").
    """
    if value == int(value):
        return str(int(value))
    # Round to 6 decimal places and strip trailing zeros
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _emit_visit_fsh(
    encounter: dict,
    timing,          # ResolvedTiming | None
    prior_encounter: Optional[dict],
    transition_start_rule: Optional[dict],
    transition_end_rule: Optional[dict],
) -> list[str]:
    """
    Emit FSH lines for a single visit PlanDefinition.

    Parameters
    ----------
    encounter            : the USDM Encounter dict
    timing               : ResolvedTiming (or None for anchor visits)
    prior_encounter      : the previous Encounter dict (or None for first anchor)
    transition_start_rule: TransitionRule dict for transitionStartRuleId (or None)
    transition_end_rule  : TransitionRule dict for transitionEndRuleId (or None)
    """
    enc_name = encounter.get("name", "")
    enc_label = encounter.get("label", "")
    enc_desc = encounter.get("description", "") or enc_label
    instance_id = f"H2Q-MC-LZZT-{enc_name}-USDM"

    subtype = _derive_subtype(enc_label)
    # soaRepeatAllowed = true only for retreatment visits
    repeat_allowed = "true" if subtype == "retreatment" else "false"

    # Contact modes
    # Each contactMode item is a Code object with flat fields:
    #   { "code": "C175574", "decode": "IN PERSON", "codeSystem": "...", ... }
    contact_modes = encounter.get("contactModes", []) or []
    mode_codes: list[tuple[str, str]] = []  # (cdisc_code, decode)
    for cm in contact_modes:
        if not isinstance(cm, dict):
            continue
        cdisc_code = cm.get("code", "") or ""
        decode = cm.get("decode", "") or ""
        if decode or cdisc_code:
            mode_codes.append((cdisc_code, decode))

    lines: list[str] = []

    lines += [
        _fsh_header(),
        f"Instance: {instance_id}",
        "InstanceOf: SOAPlanDefinition",
        "Usage: #definition",
        f'Title: "{_fsh_escape(enc_label)}"',
        f'Description: "{_fsh_escape(enc_desc)}"',
        "* status = #active",
    ]

    # ---- action block ----
    lines += [
        "* action[+]",
        f'  * id = "{enc_name}"',
        f'  * title = "{_fsh_escape(enc_label)}"',
    ]

    # Contact mode: encode as action.code (gap workaround).
    # All modes go into a single CodeableConcept with one coding per mode.
    # Per F-0 audit §5.1: no SOAPlanDefinition element for contactMode.
    if mode_codes:
        lines.append(
            "  // Gap: no SoA profile element for contactMode; encoded as action.code"
        )
        lines.append("  * code")
        for cdisc_code, decode in mode_codes:
            lines += [
                "    * coding[+]",
                '      * system = "http://www.cdisc.org"',
                f"      * code = #{cdisc_code}",
                f'      * display = "{_fsh_escape(decode)}"',
            ]

    # ---- soaTimepoint extension ----
    lines += [
        "  * extension[soaTimepoint]",
        '    * extension[soaTimePointType].valueString = "interaction"',
        f'    * extension[soaTimePointSubType].valueString = "{subtype}"',
    ]

    if timing is not None:
        # Non-anchor visit: emit full timing values.
        # FSH Quantity syntax: use .value and .code sub-elements (UCUM code = #d).
        day_str = _fmt_days(timing.planned_day_value)
        lines += [
            "    * extension[soaPlannedTimePoint].valueQuantity",
            f"      * value = {day_str}",
            "      * code = #d",
            '      * system = "http://unitsofmeasure.org"',
        ]
        if timing.reference_encounter_name:
            lines.append(
                f'    * extension[soaReferenceTimePoint].valueString = "{timing.reference_encounter_name}"'
            )
        if timing.window_lower_days is not None and timing.window_upper_days is not None:
            low_str = _fmt_days(timing.window_lower_days)
            high_str = _fmt_days(timing.window_upper_days)
            lines += [
                "    * extension[soaPlannedRange].valueRange",
                "      * low",
                f"        * value = {low_str}",
                "        * code = #d",
                '        * system = "http://unitsofmeasure.org"',
                "      * high",
                f"        * value = {high_str}",
                "        * code = #d",
                '        * system = "http://unitsofmeasure.org"',
            ]
        lines.append(
            f"    * extension[soaRepeatAllowed].valueBoolean = {repeat_allowed}"
        )

        # ---- relatedAction block ----
        if prior_encounter is not None:
            prior_name = prior_encounter.get("name", "")
            low_val = _fmt_days(timing.window_lower_days) if timing.window_lower_days is not None else "0"
            lines += [
                "  * relatedAction[+]",
                f'    * targetId = "{prior_name}"',
                "    * relationship = #after",
                f"    * offsetRange.low.value = {low_val}",
                "    * offsetRange.low.code = #d",
            ]

            # ---- transition sub-action ----
            prior_label = prior_encounter.get("label", "")
            delay_str = _fmt_days(timing.transition_delay_days)
            # Build transition description from rules
            rule_texts: list[str] = []
            if transition_start_rule:
                rt = (transition_start_rule.get("text") or "").strip()
                if rt:
                    rule_texts.append(rt)
            if transition_end_rule:
                rt = (transition_end_rule.get("text") or "").strip()
                if rt:
                    rule_texts.append(rt)
            transition_desc = " / ".join(rule_texts) if rule_texts else ""

            lines += [
                "  * action[+]",
                "    * extension[soaTransition]",
                f'      * extension[soaTargetId].valueString = "{prior_name}"',
                f'      * extension[soaTargetName].valueString = "{_fsh_escape(prior_label)}"',
                '      * extension[soaTransitionType].valueString = "scheduled"',
                "      * extension[soaTransitionDelay].valueDuration",
                f"        * value = {delay_str}",
                "        * code = #d",
                '        * system = "http://unitsofmeasure.org"',
            ]
            if timing.window_lower_days is not None and timing.window_upper_days is not None:
                low_str2 = _fmt_days(timing.window_lower_days)
                high_str2 = _fmt_days(timing.window_upper_days)
                lines += [
                    "      * extension[soaTransitionRange].valueRange",
                    "        * low",
                    f"          * value = {low_str2}",
                    "          * code = #d",
                    '          * system = "http://unitsofmeasure.org"',
                    "        * high",
                    f"          * value = {high_str2}",
                    "          * code = #d",
                    '          * system = "http://unitsofmeasure.org"',
                ]
            if transition_desc:
                lines.append(
                    f'    * description = "{_fsh_escape(transition_desc)}"'
                )
    else:
        # Anchor visit: soaTimePointType and soaTimePointSubType only
        lines.append(
            f"    * extension[soaRepeatAllowed].valueBoolean = {repeat_allowed}"
        )

    lines.append("")
    return lines


def emit_visit_plan_definitions(
    doc: "USDMDoc",
    out_dir: str,
    timing_resolver=None,
) -> list[str]:
    """
    Generate one FSH file per encounter under out_dir/visits/.

    Each file is named <encounter.name>.gen.fsh (e.g. E1.gen.fsh).

    Parameters
    ----------
    doc             : USDMDoc instance
    out_dir         : base output directory (e.g. "input/fsh/generated/usdm")
    timing_resolver : optional pre-built TimingResolver; if None, one is
                      constructed from doc using the usdm_timing module.

    Returns
    -------
    List of output file paths written.
    """
    # Import TimingResolver — prefer the standalone usdm_timing module (F-3)
    # but fall back to constructing one inline if not available.
    if timing_resolver is None:
        try:
            from usdm_timing import TimingResolver as _TR
        except ImportError:
            # Fallback: use the inline TimingResolver if usdm_timing is not on path
            # (This path is used when running tests from the repo root.)
            import sys
            import importlib
            _scripts_dir = os.path.dirname(os.path.abspath(__file__))
            if _scripts_dir not in sys.path:
                sys.path.insert(0, _scripts_dir)
            from usdm_timing import TimingResolver as _TR
        timing_resolver = _TR(doc)

    visits_dir = os.path.join(out_dir, "visits")
    os.makedirs(visits_dir, exist_ok=True)

    encounters = doc.encounters()
    # Build encounter-by-id map for prior encounter lookup
    enc_by_id: dict[str, dict] = {e["id"]: e for e in encounters}

    written: list[str] = []

    for encounter in encounters:
        enc_name = encounter.get("name", "")
        scheduled_at_id = encounter.get("scheduledAtId")

        # Resolve timing (None for anchor visits)
        timing = timing_resolver.resolve(scheduled_at_id)

        # Resolve prior encounter
        prior_enc_id = encounter.get("previousId")
        prior_encounter = enc_by_id.get(prior_enc_id) if prior_enc_id else None

        # Resolve transition rules
        # In USDM v4, transitionStartRule and transitionEndRule are inline
        # TransitionRule objects (not ID references).
        transition_start_rule: Optional[dict] = encounter.get("transitionStartRule") or None
        transition_end_rule: Optional[dict] = encounter.get("transitionEndRule") or None

        lines = _emit_visit_fsh(
            encounter=encounter,
            timing=timing,
            prior_encounter=prior_encounter,
            transition_start_rule=transition_start_rule,
            transition_end_rule=transition_end_rule,
        )

        out_path = os.path.join(visits_dir, f"{enc_name}.gen.fsh")
        _write_fsh(out_path, lines)
        written.append(out_path)

    return written


# ---------------------------------------------------------------------------
# emit_protocol_design
# ---------------------------------------------------------------------------

def _ordered_encounters(doc: "USDMDoc") -> list:
    """
    Return encounters in nextId-chain order, starting from the encounter
    whose previousId is None (the first anchor).

    Falls back to the raw list order if the chain cannot be followed.
    """
    encounters = doc.encounters()
    if not encounters:
        return []

    # Build id → encounter map
    enc_by_id: dict = {e["id"]: e for e in encounters}

    # Find the first encounter (previousId is None or absent)
    first = None
    for enc in encounters:
        if not enc.get("previousId"):
            first = enc
            break
    if first is None:
        # Fall back to raw order
        return list(encounters)

    # Walk the nextId chain
    ordered: list = []
    current = first
    visited: set = set()
    while current is not None:
        if current["id"] in visited:
            break  # cycle guard
        visited.add(current["id"])
        ordered.append(current)
        next_id = current.get("nextId")
        current = enc_by_id.get(next_id) if next_id else None

    # Append any encounters not reached via the chain (safety net)
    for enc in encounters:
        if enc["id"] not in visited:
            ordered.append(enc)

    return ordered


def emit_protocol_design(
    doc: "USDMDoc",
    out_path: str,
    timing_resolver=None,
) -> None:
    """
    Generate ProtocolDesign.gen.fsh from the USDM document.

    Emits a single SOAPlanDefinition instance
    H2Q-MC-LZZT-ProtocolDesign-USDM with one action per encounter
    (in nextId-chain order).  Each action mirrors the timing structure
    produced by emit_visit_plan_definitions:

      * action[+]
        * id          = "<encounter.name>"
        * title       = "<encounter.label>"
        * description = "<encounter.description>"
        * definitionUri = "PlanDefinition/H2Q-MC-LZZT-<encounter.name>-USDM"
        * extension[soaTimepoint] ...
        * relatedAction[+] ...   (non-anchor only)
        * action[+]              (transition sub-action; non-anchor only)
    """
    if timing_resolver is None:
        try:
            from usdm_timing import TimingResolver as _TR
        except ImportError:
            import sys as _sys
            _scripts_dir = os.path.dirname(os.path.abspath(__file__))
            if _scripts_dir not in _sys.path:
                _sys.path.insert(0, _scripts_dir)
            from usdm_timing import TimingResolver as _TR
        timing_resolver = _TR(doc)

    sv = doc.study_version()
    study_version_id = sv.get("versionIdentifier", "")

    ordered = _ordered_encounters(doc)
    enc_by_id: dict = {e["id"]: e for e in doc.encounters()}

    lines: list = [
        _fsh_header(),
        "// ============================================================",
        "// ProtocolDesign PlanDefinition (USDM-derived)",
        "// ============================================================",
        "Instance: H2Q-MC-LZZT-ProtocolDesign-USDM",
        "InstanceOf: SOAPlanDefinition",
        "Usage: #definition",
        'Title: "H2Q-MC-LZZT Protocol Design (USDM-derived)"',
        "* status = #active",
        f'* version = "{_fsh_escape(study_version_id)}"',
    ]

    for encounter in ordered:
        enc_name = encounter.get("name", "")
        enc_label = encounter.get("label", "")
        enc_desc = encounter.get("description", "") or enc_label
        instance_ref = f"H2Q-MC-LZZT-{enc_name}-USDM"

        scheduled_at_id = encounter.get("scheduledAtId")
        timing = timing_resolver.resolve(scheduled_at_id)

        prior_enc_id = encounter.get("previousId")
        prior_encounter = enc_by_id.get(prior_enc_id) if prior_enc_id else None

        transition_start_rule = encounter.get("transitionStartRule") or None
        transition_end_rule = encounter.get("transitionEndRule") or None

        subtype = _derive_subtype(enc_label)
        repeat_allowed = "true" if subtype == "retreatment" else "false"

        lines += [
            "* action[+]",
            f'  * id = "{enc_name}"',
            f'  * title = "{_fsh_escape(enc_label)}"',
            f'  * description = "{_fsh_escape(enc_desc)}"',
            f'  * definitionUri = "PlanDefinition/{instance_ref}"',
            "  * extension[soaTimepoint]",
            '    * extension[soaTimePointType].valueString = "interaction"',
            f'    * extension[soaTimePointSubType].valueString = "{subtype}"',
        ]

        if timing is not None:
            day_str = _fmt_days(timing.planned_day_value)
            lines += [
                "    * extension[soaPlannedTimePoint].valueQuantity",
                f"      * value = {day_str}",
                "      * code = #d",
                '      * system = "http://unitsofmeasure.org"',
            ]
            if timing.reference_encounter_name:
                lines.append(
                    f'    * extension[soaReferenceTimePoint].valueString = "{timing.reference_encounter_name}"'
                )
            if (timing.window_lower_days is not None
                    and timing.window_upper_days is not None):
                low_str = _fmt_days(timing.window_lower_days)
                high_str = _fmt_days(timing.window_upper_days)
                lines += [
                    "    * extension[soaPlannedRange].valueRange",
                    "      * low",
                    f"        * value = {low_str}",
                    "        * code = #d",
                    '        * system = "http://unitsofmeasure.org"',
                    "      * high",
                    f"        * value = {high_str}",
                    "        * code = #d",
                    '        * system = "http://unitsofmeasure.org"',
                ]
            lines.append(
                f"    * extension[soaRepeatAllowed].valueBoolean = {repeat_allowed}"
            )

            # relatedAction block
            if prior_encounter is not None:
                prior_name = prior_encounter.get("name", "")
                low_val = (
                    _fmt_days(timing.window_lower_days)
                    if timing.window_lower_days is not None
                    else "0"
                )
                lines += [
                    "  * relatedAction[+]",
                    f'    * targetId = "{prior_name}"',
                    "    * relationship = #after",
                    f"    * offsetRange.low.value = {low_val}",
                    "    * offsetRange.low.code = #d",
                ]

                # Transition sub-action
                prior_label = prior_encounter.get("label", "")
                delay_str = _fmt_days(timing.transition_delay_days)
                rule_texts: list = []
                if transition_start_rule:
                    rt = (transition_start_rule.get("text") or "").strip()
                    if rt:
                        rule_texts.append(rt)
                if transition_end_rule:
                    rt = (transition_end_rule.get("text") or "").strip()
                    if rt:
                        rule_texts.append(rt)
                transition_desc = " / ".join(rule_texts) if rule_texts else ""

                lines += [
                    "  * action[+]",
                    "    * extension[soaTransition]",
                    f'      * extension[soaTargetId].valueString = "{prior_name}"',
                    f'      * extension[soaTargetName].valueString = "{_fsh_escape(prior_label)}"',
                    '      * extension[soaTransitionType].valueString = "scheduled"',
                    "      * extension[soaTransitionDelay].valueDuration",
                    f"        * value = {delay_str}",
                    "        * code = #d",
                    '        * system = "http://unitsofmeasure.org"',
                ]
                if (timing.window_lower_days is not None
                        and timing.window_upper_days is not None):
                    low_str2 = _fmt_days(timing.window_lower_days)
                    high_str2 = _fmt_days(timing.window_upper_days)
                    lines += [
                        "      * extension[soaTransitionRange].valueRange",
                        "        * low",
                        f"          * value = {low_str2}",
                        "          * code = #d",
                        '          * system = "http://unitsofmeasure.org"',
                        "        * high",
                        f"          * value = {high_str2}",
                        "          * code = #d",
                        '          * system = "http://unitsofmeasure.org"',
                    ]
                if transition_desc:
                    lines.append(
                        f'    * description = "{_fsh_escape(transition_desc)}"'
                    )
        else:
            # Anchor visit: subtype only
            lines.append(
                f"    * extension[soaRepeatAllowed].valueBoolean = {repeat_allowed}"
            )

    lines.append("")
    _write_fsh(out_path, lines)
