Instance: H2Q-MC-LZZT-Vitalsigns-Temperature-Observation
InstanceOf: ObservationDefinition
Usage: #example
Title: "Temperature Measurement - Observation"
Description: "Observation of Temperature Measurement"
* status = #active
* code
  * coding[+]
    * code = #8310-5
    * system = "http://loinc.org"
    * display = "Temperature taking (procedure)"
  * text = "Temperature taking (procedure)"

// * identifier[+].value = "Temperature Measurement - Observation"
// * identifier[=].type = #PLAC
// * identifier[=].use = #usual

* identifier[+]
  * value = "I.TEMP"
  * system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
  * type
    * text = "OID"
  * use = #secondary
