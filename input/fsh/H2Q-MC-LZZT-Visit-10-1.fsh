Instance: H2Q-MC-LZZT-Study-Visit-10-1
InstanceOf: PlanDefinition
Usage: #example
Title: "Visit-10.1"
Description: "Telephone Visit [Visit-10]"
* identifier[+].value = "VISIT-10.1"
* identifier[+].value = "SE.TRT_VISIT_07-TC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* status = #active
* action[+].title = "Record Visit Date"
* action[=].id = "VISIT-10-1-H2Q-MC-LZZT-Visit-Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "VISIT-10-1-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
