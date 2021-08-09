Instance: H2Q-MC-LZZT-Study-Visit-2
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-2"
Description: "Planned Visit [Visit-2]"
* identifier[+].value = "VISIT-2"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "SE.AMB_ECG_VISIT"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* extension[plannedStudyDay].valueInteger = 0
* status = #active
* action[+].title = "Record Visit Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[=].id = "VISIT-2-H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Vital signs: Weight"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Weight-PD"
* action[=].relatedAction[+].actionId = "VISIT-2-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Temperature"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
* action[=].relatedAction[+].actionId = "VISIT-2-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Heart Rate and Blood Pressure"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
* action[=].relatedAction[+].actionId = "VISIT-2-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Ambulatory ECG placed"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Ambulatory-ECG-placed"
* action[=].relatedAction[+].actionId = "VISIT-2-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Adverse events"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
* action[=].relatedAction[+].actionId = "VISIT-2-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
