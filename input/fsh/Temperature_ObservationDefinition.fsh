Instance: H2Q-MC-LZZT-Vitalsigns-Temperature_Observation
InstanceOf: ObservationDefinition
Usage: #example
Title: "Temperature Measurement - Observation"
Description: "Observation of Temperature Measurement"
* identifier[+].value = "Temperature Measurement - Observation"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "I.TEMP"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].type.text = "OID"
* identifier[=].use = #secondary
* code.coding[+].code = #8310-5
* code.coding[=].system = "http://loinc.org"
* code.coding[=].display = "Temperature taking (procedure)"
