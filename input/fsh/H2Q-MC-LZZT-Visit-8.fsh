Instance: H2Q-MC-LZZT-Study-Visit-8
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-8"
Description: "Planned Visit [Visit-8]"
* identifier[+].value = "VISIT-8"
* extension[plannedStudyDay].valueInteger = 56
* identifier[+].value = "SE.TRT_VISIT_05"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* status = #active
* action[+].title = "Record Visit Date"
* action[=].id = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Vital signs: Weight"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Weight-PD"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Temperature"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Heart Rate and Blood Pressure"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "ECG"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ECG"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Hematology)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Hemat"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Chemistry)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Chem"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Study drug record: Medications Dispensed/Returned"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "ADAS-Cog"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ADAS-Cog"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Clinician's Interview-Based Impression of Change"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-CIBIC+"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Disability Assessment for Dementia"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-DAD"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Concomitant Medications"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Adverse events "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
* action[=].relatedAction[+].actionId = "VISIT-8-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
