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

# USDM document/study status → FHIR publication-status
# FHIR R6 publication-status: draft | active | retired | unknown
# The USDM v4 study version carries no explicit publication status field.
# This map covers USDM StudyStatus codes if present; the fallback is used
# when the field is absent (as in CDISC_Pilot_Study_v4_FIXED.json).
USDM_STUDY_STATUS_MAP: dict[str, str] = {
    "DRAFT":     "draft",
    "IN REVIEW": "draft",
    "APPROVED":  "active",
    "ACTIVE":    "active",
    "COMPLETED": "active",    # study completed → resource is #active (authoritative)
    "RETIRED":   "retired",
    "UNKNOWN":   "unknown",
}
# Fallback when USDM carries no status — override per-study as needed.
_USDM_STATUS_FALLBACK = "active"

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

    # Publication status — derived from USDM study/version status if present,
    # otherwise fall back to the module-level default.
    usdm_status_raw = (
        sv.get("documentStatus")
        or sv.get("status")
        or study.get("documentStatus")
        or study.get("status")
        or ""
    )
    fhir_status = (
        USDM_STUDY_STATUS_MAP.get(usdm_status_raw.upper(), _USDM_STATUS_FALLBACK)
        if usdm_status_raw
        else _USDM_STATUS_FALLBACK
    )

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
        f"* status = #{fhir_status}",
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
    # FHIR R6 ballot3 comparisonGroup backbone has no .name, .type, or .description
    # elements — those were added post-ballot3.  We carry the arm name and CDISC
    # arm-type code via inline extensions (url/value[x] pattern, no pre-declared
    # StructureDefinition required) and set the backbone .id to a slug of the arm
    # name for cross-referencing.
    _EXT_ARM_NAME = "http://example.org/soa/ext/arm-name"
    _EXT_ARM_TYPE = "http://example.org/soa/ext/arm-type"
    _EXT_ARM_DESC = "http://example.org/soa/ext/arm-description"
    for arm in arms:
        arm_name = arm.get("name") or arm.get("label", "")
        arm_desc = arm.get("description", "")
        arm_type_obj = arm.get("type") or {}
        arm_type_code = arm_type_obj.get("code", "")
        arm_type_decode = arm_type_obj.get("decode", "")
        # FSH backbone element id — slug of arm name
        arm_id = re.sub(r"[^a-z0-9-]", "-",
                        re.sub(r"\s+", "-", arm_name.lower())).strip("-")
        arm_id = re.sub(r"-+", "-", arm_id)

        lines += ["* comparisonGroup[+]"]
        if arm_id:
            lines.append(f'  * id = "{arm_id}"')
        # Name
        if arm_name:
            lines += [
                '  * extension[+].url = "' + _EXT_ARM_NAME + '"',
                f'  * extension[=].valueString = "{_fsh_escape(arm_name)}"',
            ]
        # Arm type (CDISC code)
        if arm_type_code:
            lines += [
                '  * extension[+].url = "' + _EXT_ARM_TYPE + '"',
                "  * extension[=].valueCoding",
                f'    * system = "http://www.cdisc.org"',
                f'    * code = #{arm_type_code}',
                f'    * display = "{_fsh_escape(arm_type_decode)}"',
            ]
        # Description (only when it differs from name)
        if arm_desc and arm_desc != arm_name:
            lines += [
                '  * extension[+].url = "' + _EXT_ARM_DESC + '"',
                f'  * extension[=].valueString = "{_fsh_escape(arm_desc)}"',
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


def _emit_transition_sub_action(
    lines: list,
    target_id: str,
    target_label: str,
    transition_type: str,
    delay_str: str,
    window_lower_days,
    window_upper_days,
    description: str = "",
) -> None:
    """
    Append a soaTransition sub-action block to lines.

    target_id        : FHIR action id of the destination encounter
    target_label     : human-readable label of the destination encounter
    transition_type  : "scheduled" | "early-termination" | "adverse-event"
    delay_str        : formatted day value for soaTransitionDelay
    window_lower_days: float | None
    window_upper_days: float | None
    description      : optional description text
    """
    lines += [
        "  * action[+]",
        "    * extension[soaTransition]",
        f'      * extension[soaTargetId].valueString = "{target_id}"',
        f'      * extension[soaTargetName].valueString = "{_fsh_escape(target_label)}"',
        f'      * extension[soaTransitionType].valueString = "{transition_type}"',
        "      * extension[soaTransitionDelay].valueDuration",
        f"        * value = {delay_str}",
        "        * code = #d",
        '        * system = "http://unitsofmeasure.org"',
    ]
    if window_lower_days is not None and window_upper_days is not None:
        low_str = _fmt_days(window_lower_days)
        high_str = _fmt_days(window_upper_days)
        lines += [
            "      * extension[soaTransitionRange].valueRange",
            "        * low",
            f"          * value = {low_str}",
            "          * code = #d",
            '          * system = "http://unitsofmeasure.org"',
            "        * high",
            f"          * value = {high_str}",
            "          * code = #d",
            '          * system = "http://unitsofmeasure.org"',
        ]
    if description:
        lines.append(f'    * description = "{_fsh_escape(description)}"')


# ET encounter id used for early-withdrawal edges (hand-authored; no USDM Encounter object).
_ET_ENCOUNTER_ID = "H2Q-MC-LZZT-Study-ET-14"
_ET_ENCOUNTER_LABEL = "Early Termination"


def _emit_visit_fsh(
    encounter: dict,
    timing,           # ResolvedTiming | None  (this encounter's own timing)
    prior_encounter: Optional[dict],
    next_encounter: Optional[dict],
    next_timing,      # ResolvedTiming | None  (next encounter's timing, for fwd transition delay)
    transition_start_rule: Optional[dict],
    transition_end_rule: Optional[dict],
    include_et_edge: bool = True,
) -> list[str]:
    """
    Emit FSH lines for a single visit PlanDefinition.

    Transitions are **forward-facing graph edges**:
      - One "scheduled" soaTransition sub-action pointing to next_encounter
        (omitted for the last encounter in the main sequence).
      - One "early-termination" soaTransition sub-action pointing to the ET
        encounter (omitted when include_et_edge is False, e.g. for ET itself).

    The soaTransitionDelay on the forward edge is taken from next_timing
    (the planned duration from this encounter to the next one).

    The backward relatedAction (#after prior_encounter) is kept unchanged —
    it encodes the scheduling dependency, not the graph direction.
    """
    enc_name = encounter.get("name", "")
    enc_label = encounter.get("label", "")
    enc_desc = encounter.get("description", "") or enc_label
    instance_id = f"H2Q-MC-LZZT-{enc_name}-USDM"

    subtype = _derive_subtype(enc_label)
    repeat_allowed = "true" if subtype == "retreatment" else "false"

    # Contact modes
    contact_modes = encounter.get("contactModes", []) or []
    mode_codes: list[tuple[str, str]] = []
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

    # Contact mode (gap workaround — no SoA profile element)
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

        # ---- relatedAction: backward scheduling dependency (#after prior) ----
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
                '    * offsetRange.low.system = "http://unitsofmeasure.org"',
                "    * offsetRange.low.code = #d",
            ]
    else:
        # Anchor visit
        lines.append(
            f"    * extension[soaRepeatAllowed].valueBoolean = {repeat_allowed}"
        )

    # ---- soaTransition sub-actions: forward graph edges ----

    # 1. Forward "scheduled" edge → next encounter in the main sequence
    if next_encounter is not None and next_timing is not None:
        next_name = next_encounter.get("name", "")
        next_label = next_encounter.get("label", "")
        delay_str = _fmt_days(next_timing.planned_day_value)

        # Transition description from this encounter's end-rule / next's start-rule
        rule_texts: list[str] = []
        if transition_end_rule:
            rt = (transition_end_rule.get("text") or "").strip()
            if rt:
                rule_texts.append(rt)
        if transition_start_rule:
            rt = (transition_start_rule.get("text") or "").strip()
            if rt:
                rule_texts.append(rt)
        transition_desc = " / ".join(rule_texts) if rule_texts else ""

        _emit_transition_sub_action(
            lines,
            target_id=next_name,
            target_label=next_label,
            transition_type="scheduled",
            delay_str=delay_str,
            window_lower_days=next_timing.window_lower_days,
            window_upper_days=next_timing.window_upper_days,
            description=transition_desc,
        )

    # 2. Early-termination edge → ET encounter (every non-ET encounter)
    if include_et_edge:
        _emit_transition_sub_action(
            lines,
            target_id=_ET_ENCOUNTER_ID,
            target_label=_ET_ENCOUNTER_LABEL,
            transition_type="early-termination",
            delay_str="0",
            window_lower_days=None,
            window_upper_days=None,
            description="Early withdrawal or adverse event",
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
    # Build id-keyed maps
    enc_by_id: dict[str, dict] = {e["id"]: e for e in encounters}

    # Build next-encounter map: enc_id → enc whose previousId == enc_id
    next_by_id: dict[str, dict] = {}
    for enc in encounters:
        prev_id = enc.get("previousId")
        if prev_id:
            next_by_id[prev_id] = enc

    written: list[str] = []

    for encounter in encounters:
        enc_id = encounter["id"]
        enc_name = encounter.get("name", "")
        scheduled_at_id = encounter.get("scheduledAtId")

        # This encounter's own timing
        timing = timing_resolver.resolve(scheduled_at_id)

        # Prior encounter (for relatedAction backward dep)
        prior_enc_id = encounter.get("previousId")
        prior_encounter = enc_by_id.get(prior_enc_id) if prior_enc_id else None

        # Next encounter (for forward soaTransition)
        next_encounter = next_by_id.get(enc_id)
        next_timing = None
        if next_encounter is not None:
            next_timing = timing_resolver.resolve(next_encounter.get("scheduledAtId"))

        # Transition rules on this encounter (used for description text)
        transition_start_rule: Optional[dict] = encounter.get("transitionStartRule") or None
        transition_end_rule: Optional[dict] = encounter.get("transitionEndRule") or None

        # ET edge suppressed for ET/RT encounters themselves
        enc_label = encounter.get("label", "")
        subtype = _derive_subtype(enc_label)
        include_et_edge = subtype not in ("early-termination", "retreatment")

        lines = _emit_visit_fsh(
            encounter=encounter,
            timing=timing,
            prior_encounter=prior_encounter,
            next_encounter=next_encounter,
            next_timing=next_timing,
            transition_start_rule=transition_start_rule,
            transition_end_rule=transition_end_rule,
            include_et_edge=include_et_edge,
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

    # Build next-encounter map
    next_by_id: dict = {}
    for enc in doc.encounters():
        prev_id = enc.get("previousId")
        if prev_id:
            next_by_id[prev_id] = enc

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
        enc_id = encounter["id"]
        enc_name = encounter.get("name", "")
        enc_label = encounter.get("label", "")
        enc_desc = encounter.get("description", "") or enc_label
        instance_ref = f"H2Q-MC-LZZT-{enc_name}-USDM"

        scheduled_at_id = encounter.get("scheduledAtId")
        timing = timing_resolver.resolve(scheduled_at_id)

        prior_enc_id = encounter.get("previousId")
        prior_encounter = enc_by_id.get(prior_enc_id) if prior_enc_id else None

        next_encounter = next_by_id.get(enc_id)
        next_timing = None
        if next_encounter is not None:
            next_timing = timing_resolver.resolve(next_encounter.get("scheduledAtId"))

        transition_start_rule = encounter.get("transitionStartRule") or None
        transition_end_rule = encounter.get("transitionEndRule") or None

        subtype = _derive_subtype(enc_label)
        repeat_allowed = "true" if subtype == "retreatment" else "false"
        include_et_edge = subtype not in ("early-termination", "retreatment")

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

            # relatedAction: backward scheduling dependency
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
                    '    * offsetRange.low.system = "http://unitsofmeasure.org"',
                    "    * offsetRange.low.code = #d",
                ]
        else:
            lines.append(
                f"    * extension[soaRepeatAllowed].valueBoolean = {repeat_allowed}"
            )

        # Forward "scheduled" transition → next encounter
        if next_encounter is not None and next_timing is not None:
            next_name = next_encounter.get("name", "")
            next_label = next_encounter.get("label", "")
            delay_str = _fmt_days(next_timing.planned_day_value)
            rule_texts: list = []
            if transition_end_rule:
                rt = (transition_end_rule.get("text") or "").strip()
                if rt:
                    rule_texts.append(rt)
            if transition_start_rule:
                rt = (transition_start_rule.get("text") or "").strip()
                if rt:
                    rule_texts.append(rt)
            transition_desc = " / ".join(rule_texts) if rule_texts else ""
            _emit_transition_sub_action(
                lines,
                target_id=next_name,
                target_label=next_label,
                transition_type="scheduled",
                delay_str=delay_str,
                window_lower_days=next_timing.window_lower_days,
                window_upper_days=next_timing.window_upper_days,
                description=transition_desc,
            )

        # Early-termination edge
        if include_et_edge:
            _emit_transition_sub_action(
                lines,
                target_id=_ET_ENCOUNTER_ID,
                target_label=_ET_ENCOUNTER_LABEL,
                transition_type="early-termination",
                delay_str="0",
                window_lower_days=None,
                window_upper_days=None,
                description="Early withdrawal or adverse event",
            )

    lines.append("")
    _write_fsh(out_path, lines)


# ---------------------------------------------------------------------------
# Activity stubs + visit activity actions
# ---------------------------------------------------------------------------

import csv as _csv


def _load_csv_skip_comments(path: str) -> list:
    """Load a CSV file, skipping lines that start with '#'."""
    import io
    with open(path, newline="", encoding="utf-8") as fh:
        lines = [ln for ln in fh if not ln.startswith("#")]
    return list(_csv.DictReader(io.StringIO("".join(lines))))


def _activity_instance_id(activity_id: str) -> str:
    """Convert catalog id to a FHIR-safe FSH instance id (max 64 chars)."""
    raw = f"usdm-act-{activity_id}"
    if len(raw) <= 64:
        return raw
    # Truncate: prefix=9, hyphen=1, hash=6 → 16 overhead; body gets 48 chars
    import hashlib
    suffix = hashlib.md5(raw.encode()).hexdigest()[:6]
    return f"usdm-act-{activity_id[:48]}-{suffix}"


def _obsdef_instance_id(obsdef_id: str) -> str:
    """Convert catalog obsdef_id to a FHIR-safe FSH instance id."""
    return f"usdm-obs-{obsdef_id}"


def _questionnaire_instance_id(questionnaire_id: str) -> str:
    """Convert catalog questionnaire_id to a FHIR-safe FSH instance id."""
    return f"usdm-q-{questionnaire_id}"


def _code_system_to_alias(code_system: str) -> str:
    """
    Map a raw code_system string from the catalog to a FHIR system URI.
    Returns a full URI suitable for use in FSH system = "..." lines.
    """
    _MAP = {
        "LOINC": "http://loinc.org",
        "SNOMED": "http://snomed.info/sct",
        "OMOP": "http://omop.org",
        "SPONSOR": "http://example.org/sponsor",
        "http://www.cdisc.org": "http://www.cdisc.org",
    }
    return _MAP.get(code_system, code_system or "http://example.org/code-system")


def emit_activity_stubs(
    activity_catalog_path: str,
    observation_catalog_path: str,
    out_path: str,
) -> None:
    """
    Generate ActivityDefinition, ObservationDefinition, and Questionnaire
    stub FSH instances from the USDM activity + observation catalogs.

    Output: a single file at out_path (e.g.
    input/fsh/generated/usdm/ActivityStubs.gen.fsh).

    Rules:
    - measurement rows  → ActivityDefinition stub +
                          ObservationDefinition stub (if result_obsdef_id set)
    - procedure rows    → ActivityDefinition stub (no ObsDef)
    - instrument rows   → Questionnaire stub (no ActivityDefinition)
    - panel ObsDef rows → ObservationDefinition panel stub (hasMember wired
                          when analyte rows with matching member_of exist)
    - analyte ObsDef rows → ObservationDefinition analyte stub
    """
    activities = _load_csv_skip_comments(activity_catalog_path)
    observations = _load_csv_skip_comments(observation_catalog_path)

    # Index observations by id and build panel→[analyte] map
    obs_by_id = {r["obsdef_id"]: r for r in observations}
    panel_members: dict = {}  # panel_id → [analyte_id, ...]
    for obs in observations:
        mo = obs.get("member_of", "")
        if mo:
            panel_members.setdefault(mo, []).append(obs["obsdef_id"])

    lines: list = [_fsh_header()]

    # -----------------------------------------------------------------------
    # Observation definitions (panels first so analytes can reference them)
    # -----------------------------------------------------------------------
    # ObservationDefinition ids that are superseded by LabPanels.gen.fsh.
    # The lab panels generator emits richer LOINC-coded definitions for these.
    _LAB_PANEL_OBSDEF_IDS: frozenset = frozenset({
        "hematology-obs",
        "chemistry-obs",
        "uninalysis-obs",
        "thyroid-obs",
        "other-obs",
        # USDM BCCat panel stubs — superseded by richer lab panel definitions
        "chemcat1-panel-obs",
        "urincat1-panel-obs",
    })

    panels = [o for o in observations if o.get("kind") == "panel"]
    analytes = [o for o in observations if o.get("kind") == "analyte"]

    for obs in panels + analytes:
        oid = obs["obsdef_id"]
        if oid in _LAB_PANEL_OBSDEF_IDS:
            continue  # superseded by LabPanels.gen.fsh
        fhir_id = _obsdef_instance_id(oid)
        code = obs.get("code", "")
        code_display = obs.get("code_display", "")
        unit = obs.get("unit", "")
        datatype = obs.get("datatype", "")
        kind = obs.get("kind", "")

        lines += [
            "",
            f"// ObservationDefinition: {oid}",
            f"Instance: {fhir_id}",
            "InstanceOf: ObservationDefinition",
            "Usage: #definition",
            f'Title: "{_fsh_escape(code_display or oid)}"',
            f'Description: "USDM-derived observation definition for {_fsh_escape(oid)}"',
            "* status = #active",
        ]
        # code is 1..1 on ObservationDefinition — always emit it
        lines += ["* code"]
        if code:
            lines += [
                "  * coding[+]",
                f'    * system = "http://www.cdisc.org"',
                f"    * code = #{code}",
            ]
            if code_display:
                lines.append(f'    * display = "{_fsh_escape(code_display)}"')
        else:
            # Fallback text-only code so cardinality constraint is satisfied
            lines.append(f'  * text = "{_fsh_escape(code_display or oid)}"')
        if datatype == "Quantity":
            lines.append("* permittedDataType = #Quantity")
        elif datatype == "string":
            lines.append("* permittedDataType = #string")
        if unit:
            lines.append(f'* permittedUnit = UCUM#"{unit}"')
        if kind == "panel":
            for member_id in panel_members.get(oid, []):
                member_fhir_id = _obsdef_instance_id(member_id)
                lines.append(
                    f"* hasMember[+] = Reference({member_fhir_id})"
                )

    # -----------------------------------------------------------------------
    # ActivityDefinitions (measurement + procedure)
    # -----------------------------------------------------------------------
    # Activities whose ActivityDefinition is emitted by lab_panels_to_fsh.py
    # (richer LOINC panel codes, hasMember wiring).  Skip them here to avoid
    # duplicate Instance ids across FSH files.
    _LAB_PANEL_ACTIVITY_IDS: frozenset = frozenset({
        "hematology",
        "chemistry",
        "uninalysis",
        "thyroid",
        "other",
    })

    for act in activities:
        act_id = act["id"]
        archetype = act.get("archetype", "")
        title = act.get("title", act_id)
        code = act.get("code", "")
        code_display = act.get("code_display", "")
        code_system = act.get("code_system", "")
        result_obsdef_id = act.get("result_obsdef_id", "")

        if act_id in _LAB_PANEL_ACTIVITY_IDS:
            continue  # superseded by LabPanels.gen.fsh

        if archetype in ("measurement", "procedure"):
            fhir_id = _activity_instance_id(act_id)
            lines += [
                "",
                f"// ActivityDefinition: {act_id} ({archetype})",
                f"Instance: {fhir_id}",
                "InstanceOf: ActivityDefinition",
                "Usage: #definition",
                f'Title: "{_fsh_escape(title)}"',
                f'Description: "USDM-derived activity: {_fsh_escape(title)}"',
                "* status = #active",
                "* kind = #ServiceRequest",
                "* intent = #plan",
            ]
            if code and code_system:
                sys_uri = _code_system_to_alias(code_system)
                lines += [
                    "* code",
                    "  * coding[+]",
                    f'    * system = "{sys_uri}"',
                    f"    * code = #{code}",
                ]
                if code_display:
                    lines.append(f'    * display = "{_fsh_escape(code_display)}"')
            if result_obsdef_id and result_obsdef_id in obs_by_id:
                obs_fhir_id = _obsdef_instance_id(result_obsdef_id)
                # observationResultRequirement is canonical in R6, not Reference
                lines.append(
                    f"* observationResultRequirement[+] = Canonical({obs_fhir_id})"
                )

    # -----------------------------------------------------------------------
    # Questionnaires (instrument rows)
    # -----------------------------------------------------------------------
    for act in activities:
        act_id = act["id"]
        archetype = act.get("archetype", "")
        if archetype != "instrument":
            continue
        title = act.get("title", act_id)
        q_id = act.get("questionnaire_id", "") or act_id
        respondent_type = act.get("respondent_type", "")
        fhir_id = _questionnaire_instance_id(q_id)

        lines += [
            "",
            f"// Questionnaire: {act_id} (instrument)",
            f"Instance: {fhir_id}",
            "InstanceOf: Questionnaire",
            "Usage: #definition",
            f'Title: "{_fsh_escape(title)}"',
            f'Description: "USDM-derived questionnaire shell for {_fsh_escape(title)}"',
            "* status = #active",
            "* subjectType = #Patient",
        ]

    lines.append("")
    _write_fsh(out_path, lines)


def emit_visit_activity_actions(
    activity_catalog_path: str,
    matrix_path: str,
    visits_out_dir: str,
) -> list:
    """
    For each visit in the SoA matrix, append activity action[+] blocks to the
    existing visit .gen.fsh file (the visit encounter skeleton).

    Each activity row in the matrix that has an 'X' for a given encounter
    produces one action[+] block:

      * action[+]
        * title = "<activity title>"
        * definitionUri = "ActivityDefinition/usdm-act-<id>"   (measurement/procedure)
        OR
        * definitionCanonical = Canonical(usdm-q-<questionnaire_id>)   (instrument)
        * relatedAction[+]
          * targetId = "<encounter.name>"
          * relationship = #after

    The encounter action id (the relatedAction target) is the encounter name
    (e.g. "E1"), which matches the `* id = "E1"` set in the visit skeleton.

    Returns a list of visit file paths modified.
    """
    activities = _load_csv_skip_comments(activity_catalog_path)
    act_by_id = {r["id"]: r for r in activities}

    matrix_rows = _load_csv_skip_comments(matrix_path)
    if not matrix_rows:
        return []

    all_cols = list(matrix_rows[0].keys())
    activity_col = all_cols[0]
    visit_cols = all_cols[1:]

    # Collect activities per visit
    visit_activities: dict = {vc: [] for vc in visit_cols}
    for row in matrix_rows:
        act_id = row.get(activity_col, "").strip()
        if not act_id:
            continue
        for vc in visit_cols:
            if row.get(vc, "").strip().startswith("X"):
                visit_activities[vc].append(act_id)

    modified = []

    for enc_name, act_ids in visit_activities.items():
        if not act_ids:
            continue

        visit_file = os.path.join(visits_out_dir, f"{enc_name}.gen.fsh")
        if not os.path.exists(visit_file):
            continue

        with open(visit_file, encoding="utf-8") as fh:
            existing = fh.read()

        action_lines: list = [
            "",
            f"// --- Activity actions for {enc_name} ---",
        ]

        for act_id in act_ids:
            act = act_by_id.get(act_id)
            if act is None:
                continue

            archetype = act.get("archetype", "")
            title = act.get("title", act_id)
            respondent_type = act.get("respondent_type", "") or "practitioner"
            q_id = act.get("questionnaire_id", "") or act_id

            action_lines.append("* action[+]")
            action_lines.append(f'  * title = "{_fsh_escape(title)}"')

            if archetype == "instrument":
                q_fhir_id = _questionnaire_instance_id(q_id)
                action_lines.append(
                    f"  * definitionCanonical = Canonical({q_fhir_id})"
                )
                # participant type from respondent_type column
                ptype_map = {
                    "patient": "#patient",
                    "practitioner": "#practitioner",
                    "related-person": "#relatedperson",
                }
                ptype = ptype_map.get(respondent_type, "#practitioner")
                action_lines.append(f"  * participant[+].type = {ptype}")
            else:
                # measurement or procedure → ActivityDefinition
                act_fhir_id = _activity_instance_id(act_id)
                action_lines.append(
                    f"  * definitionUri = \"ActivityDefinition/{act_fhir_id}\""
                )

            # relatedAction: after the encounter anchor action
            action_lines += [
                "  * relatedAction[+]",
                f'    * targetId = "{enc_name}"',
                "    * relationship = #after",
            ]

        # Append action blocks to the visit file (before the trailing newline)
        new_content = existing.rstrip("\n") + "\n" + "\n".join(action_lines) + "\n"
        tmp = visit_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(new_content)
        os.replace(tmp, visit_file)
        modified.append(visit_file)

    return modified
