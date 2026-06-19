// PRO exemplar — core-R6 Questionnaire attached directly from the visit action.
// SDC patterns adopted by convention (no R6 SDC package); extension URLs may
// raise tolerated "unresolved extension" WARNINGS, not errors.
Alias: SDC_EXTRACT = http://hl7.org/fhir/uv/sdc/StructureDefinition/sdc-questionnaire-itemExtractionContext

Instance: H2Q-MC-LZZT-Questionnaire-TTS-Acceptability-Survey
InstanceOf: Questionnaire
Usage: #definition
Title: "TTS Acceptability Survey"
Description: "Patient-reported acceptability survey for the transdermal therapeutic system (TTS)."
* status = #active
* subjectType = #Patient
* identifier[+].value = "F.TTSACC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* code = LOINC#71969-0 "Adverse drug reaction assessment"
* item[+].linkId = "comfort"
* item[=].text = "How comfortable was the patch to wear?"
* item[=].type = #coding
* item[=].answerOption[+].valueString = "Very comfortable"
* item[=].answerOption[+].valueString = "Comfortable"
* item[=].answerOption[+].valueString = "Uncomfortable"
* item[=].answerOption[+].valueString = "Very uncomfortable"
* item[+].linkId = "adhesion"
* item[=].text = "Did the patch stay on for the full wear period?"
* item[=].type = #boolean
* item[+].linkId = "score"
* item[=].text = "Overall acceptability score (0-10)"
* item[=].type = #integer

Instance: H2Q-MC-LZZT-TTS-Acceptability-Score-Obs
InstanceOf: ObservationDefinition
Usage: #example
Title: "TTS Acceptability Score - Observation"
Description: "Scored result extracted from the TTS Acceptability Survey (SDC extraction target)."
* insert ScoredInstrumentObservation(71969-0, [[TTS acceptability score]])
