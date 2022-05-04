Instance: H2Q-MC-LZZT-Study-Visit-9-1
InstanceOf: PlanDefinition
Usage: #example
Title: "Visit-9.1"
Description: "Telephone Visit [Visit-9]"
* identifier[+].value = "VISIT-9.1"
* identifier[+].value = "SE.TRT_VISIT_06-TC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* status = #active
* action[+].title = "Record Visit Date"
* action[=].id = "VISIT-9-1-H2Q-MC-LZZT-Visit-Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "VISIT-9-1-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
