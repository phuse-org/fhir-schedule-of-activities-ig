Instance: H2Q-MC-LZZT-Study-Visit-3
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-3"
Description: "Planned Visit [Visit-3]"
* identifier[+].value = "VISIT-3"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "SE.RANDOMIZATION_VISIT"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* extension[plannedStudyDay].valueInteger = 0
* status = #active
* action[+].title = "Record Visit Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[=].id = "VISIT-3-H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Vital signs: Weight"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Weight-PD"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Temperature"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Heart Rate and Blood Pressure"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Ambulatory ECG removed"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Ambulatory-ECG-removed"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Concomitant Medications"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Patient randomized"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Patient-randomized"
* action[=].id = "VISIT-3-H2Q-MC-LZZT-Patient-randomized"
* action[+].title = "Plasma Specimen (Xanomeline) "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Plasma-Specimen"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Patient-randomized"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Study drug record: Medications Dispensed/Returned"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Patient-randomized"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "ADAS-Cog"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ADAS-Cog"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Patient-randomized"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Clinician's Interview-Based Impression of Change"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-CIBIC+"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Patient-randomized"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Disability Assessment for Dementia"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-DAD"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Patient-randomized"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Patient-randomized"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Adverse events"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
* action[=].relatedAction[+].actionId = "VISIT-3-H2Q-MC-LZZT-Patient-randomized"
* action[=].relatedAction[=].relationship = #after
