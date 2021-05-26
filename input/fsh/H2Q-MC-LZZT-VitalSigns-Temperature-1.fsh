Instance: H2Q-MC-LZZT-Vitalsigns-Temperature
InstanceOf: SOAStudyActivityDefinition
Usage: #example
Title: "Temperature Measurement"
Description: "Temperature Measurement"
* identifier[+].value = "Temperature Measurement"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "I.TEMP"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].type.text = "OID"
* identifier[=].use = #secondary
* status = #active
* code.coding[+].code = #56342008
* code.coding[=].system = "http://snomed.info/sct"
* code.coding[=].display = "Temperature taking (procedure)"

* bodySite.coding[+].code = #74262004
* bodySite.coding[=].system = "http://snomed.info/sct"
* bodySite.coding[=].display = "Oral cavity"

* bodySite.coding[+].code = #34402009
* bodySite.coding[=].system = "http://snomed.info/sct"
* bodySite.coding[=].display = "Rectum"

* bodySite.coding[+].code = #91470000
* bodySite.coding[=].system = "http://snomed.info/sct"
* bodySite.coding[=].display = "Axilla"

* bodySite.coding[+].code = #42859004
* bodySite.coding[=].system = "http://snomed.info/sct"
* bodySite.coding[=].display = "Tympanic membrane structure"

