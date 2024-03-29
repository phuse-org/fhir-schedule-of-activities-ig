Instance: H2Q-MC-LZZT-Study-Visit-9
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-9"
Description: "Planned Visit [Visit-9] - removed in Protocol Amendment"
* identifier[+].value = "VISIT-9"
* extension[plannedStudyDay].valueInteger = 84
* identifier[+].value = "SE.TRT_VISIT_06"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* status = #retired
* type = #clinical-protocol
* action[+].title = "Record Visit Date"
* action[=].id = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Vital signs: Weight"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Weight-PD"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Temperature"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Heart Rate and Blood Pressure"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "ECG"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ECG"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Hematology)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Hemat"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Chemistry)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Chem"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Urinalysis)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Urinalysis"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Plasma Specimen (Xanomeline) "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Plasma-Specimen"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Study drug record: Medications Dispensed/Returned "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised"
* action[=].id = "VISIT-10-H2Q-MC-LZZT-NPI-X"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised (2w post visit)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "VISIT-10-H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetDuration.value = 2
* action[=].relatedAction[=].offsetDuration.code = #wk
* action[+].title = "Concomitant Medications"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Adverse events "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
* action[=].relatedAction[+].actionId = "VISIT-9-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
