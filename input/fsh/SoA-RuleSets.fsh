// Archetype helper RuleSets and aliases for Schedule-of-Activities resources.
Alias: LOINC = http://loinc.org

// --- Archetype 1: quantitative measurement -------------------------------

// ActivityDefinition for a vital-sign / simple measurement.
// oidsys: ODM def type (ItemDef|FormDef); oid: ODM OID; loinc: LOINC code; lname: LOINC display.
RuleSet: VitalSignActivity(oidsys, oid, loinc, lname)
* status = #active
* kind = #ServiceRequest
* intent = #plan
* participant[+].type = #practitioner
* identifier[+].value = "{oid}"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/{oidsys}#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* code.coding[+] = LOINC#{loinc} "{lname}"

// ObservationDefinition describing the result a measurement must produce.
RuleSet: VitalSignObservation(loinc, lname, unit)
* status = #active
* code = LOINC#{loinc} "{lname}"
* permittedDataType = #Quantity
* permittedUnit = UCUM#"{unit}"
* preferredReportName = "{lname}"

// --- Archetype 2: PRO / clinician instrument -----------------------------

// Appends a direct Questionnaire attachment to a PlanDefinition action.
// qcanonical: Questionnaire instance id; title: action title; ptype: #patient|#practitioner.
RuleSet: InstrumentAction(qcanonical, title, ptype)
* action[+].title = "{title}"
* action[=].definitionCanonical = Canonical({qcanonical})
* action[=].participant[+].type = {ptype}

// Optional scored-result ObservationDefinition (SDC extraction target).
RuleSet: ScoredInstrumentObservation(loinc, lname)
* status = #active
* code = LOINC#{loinc} "{lname}"
* permittedDataType = #integer
* preferredReportName = "{lname}"
