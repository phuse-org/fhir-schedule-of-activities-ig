Instance: H2Q-MC-LZZT-Study-Visit-8-1
InstanceOf: PlanDefinition
Usage: #example
Title: "Visit-8.1"
Description: "Telephone Visit [Visit-8]"
* identifier[+].value = "VISIT-8.1"
* identifier[+].value = "SE.TRT_VISIT_05_TC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* status = #active
* action[+].title = "Record Visit Date"
* action[=].id = "VISIT-8-1-H2Q-MC-LZZT-Visit-Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "VISIT-8-1-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
