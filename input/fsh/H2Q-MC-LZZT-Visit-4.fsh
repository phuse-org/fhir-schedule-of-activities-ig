Instance: H2Q-MC-LZZT-Study-Visit-4
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-4"
Description: "Planned Visit [Visit-4]"
* identifier[+].value = "VISIT-4"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "SE.TRT_VISIT_01"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* extension[plannedStudyDay].valueInteger = 14
* status = #active
* action[+].title = "Record Visit Date"
* action[=].id = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Apo E genotyping "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Apo-E-genotyping"
* action[+].title = "Vital signs: Weight"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Weight-PD"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Temperature"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Heart Rate and Blood Pressure"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "ECG "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ECG"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Hematology)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Hemat"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Chemistry)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Chem"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Urinalysis)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Urinalysis"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Plasma Specimen"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Plasma-Specimen"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Study drug record"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Concomitant Medications "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Adverse events "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
* action[=].relatedAction[+].actionId = "VISIT-4-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
