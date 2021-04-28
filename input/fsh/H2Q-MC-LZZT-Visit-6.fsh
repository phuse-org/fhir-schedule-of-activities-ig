Instance: H2Q-MC-LZZT-Study-Visit-6
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-6"
Description: "Planned Visit [Visit-6]"
* identifier[+].value = "VISIT-6"
* extension[plannedStudyDay].valueInteger = 28
* identifier[+].value = "SE.TRT_VISIT_03"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* status = #active
* action[+].title = "Visit"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit"
