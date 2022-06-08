Instance: H2Q-MC-LZZT-Study-Visit-1
InstanceOf: PlanDefinition
Usage: #example
Title: "Visit-1"
Description: "Planned Visit [Visit-1]"
* identifier[+].value = "H2Q-MC-LZZT-Study-Visit-1"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "VISIT-1"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "SE.SCREENING_VISIT"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].type.text = "OID"
* identifier[=].use = #secondary
* identifier[+].value = "1.0"
* identifier[=].system = "http://www.cdisc.org/ns/sdtm/TV#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/sdtm/TV#"
* identifier[=].type.coding[0].display = "VISNUM"
* identifier[=].type.text = "VISNUM"
* identifier[=].use = #secondary
* status = #active
* action[+].title = "Record Visit Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[=].id = "VISIT-1-H2Q-MC-LZZT-Visit-Date"
// This should be the activity that initiates all other activities
* action[+].title = "Informed Consent"
* action[=].id = "H2Q-MC-LZZT-Informed-Consent"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[+].actionId = "VISIT-1-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Patient number assigned"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Patient-number-assigned"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Hachinski 4"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Hachinski-4"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "MMSE 10-23"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-MMSE-10-23"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Physical examination"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Physical-examination"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Medical History"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Medical-History"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Habits - Alcohol"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Habits-Alcohol"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Habits - Caffeine"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Habits-Caffeine"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Habits - Smoking"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Habits-Smoking"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Chest x-ray"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Chest-x-ray"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital signs: Height"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Height-PD"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital signs: Weight"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Weight-PD"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Temperature"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Vital Signs: Heart Rate and Blood Pressure"
* action[=].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "ECG"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ECG"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Placebo TTS test"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Placebo-TTS-test"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "CT Scan"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-CT-Scan"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Concomitant Medications"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[=].relatedAction[+].actionId = "VISIT-1-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Hematology)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Hemat"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Chemistry)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Chem"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Laboratory (Urinalysis)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Urinalysis"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Hemoglobin A1C"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Hemoglobin-A1C"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "ADAS-Cog"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ADAS-Cog"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Clinician's Interview-Based Impression of Change"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-CIBIC"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Disability Assessment for Dementia"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-DAD"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Neuropsychiatric Inventory Questionnaire – Revised"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Informed-Consent"
* action[=].relatedAction[=].relationship = #after
* action[+].title = "Adverse events"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
* action[=].relatedAction[+].actionId = "VISIT-1-H2Q-MC-LZZT-Visit-Date"
* action[=].relatedAction[=].relationship = #after
