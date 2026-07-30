Instance: H2Q-MC-LZZT-Study-Visit-1
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-1"
Description: "Planned Visit [Visit-1]"
* identifier[+]
  * value = "VISIT-1"
  * type = #PLAC
  * use = #usual
* identifier[+]
  * value = "SE.SCREENING_VISIT"
  * system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
  * type
    * coding[0]
      * system = "http://www.cdisc.org/ns/odm/v1.3#"
      * display = "OID"
    * text = "OID"
  * use = #secondary
* status = #active
// ActivityDefinition instances are referenced by their canonical URL, which is the same as the resource URL.
* action[+]
  * title = "Record Visit Date"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
  * id = "VISIT-1-H2Q-MC-LZZT-Visit-Date"
// This should be the activity that initiates all other activities
// * action[=].trigger = 
* action[+]
  * title = "Informed Consent"
  * id = "H2Q-MC-LZZT-Informed-Consent"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Informed-Consent"
  * relatedAction[+]
    * targetId = "VISIT-1-H2Q-MC-LZZT-Visit-Date"
    * relationship = #after
* action[+]
  * title = "Patient number assigned"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Patient-number-assigned"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Hachinski 4"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Hachinski-4"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "MMSE 10-23"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-MMSE-10-23"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Physical examination"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Physical-examination"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Medical History"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Medical-History"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Habits - Alcohol"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Habits-Alcohol"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Habits - Caffeine"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Habits-Caffeine"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Habits - Smoking"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Habits-Smoking"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Chest x-ray"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Chest-x-ray"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Vital signs: Height"
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Height-PD"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Vital signs: Weight"
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Weight-PD"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Vital Signs: Temperature"
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Vital Signs: Heart Rate and Blood Pressure"
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "ECG"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ECG"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Placebo TTS test"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Placebo-TTS-test"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "CT Scan"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-CT-Scan"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Concomitant Medications"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
  * relatedAction[+]
    * targetId = "VISIT-1-H2Q-MC-LZZT-Visit-Date"
    * relationship = #after
* action[+]
  * title = "Laboratory (Hematology)"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Hemat"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Laboratory (Chemistry)"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Chem"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Hemoglobin A1C"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Hemoglobin-A1C"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
// Conditional scheduling: HbA1c only applies to (e.g.) diabetic subjects.
  * condition[+]
    * kind = #applicability
    * expression[+]
      * description = "Blood Chemistry with HbA1c"
      * language = #"text/fhirpath"
      * expression = "Condition.where(subject.reference = 'Patient/' + Id).where(code.coding.system = 'http://snomed.info/sct' and code.coding.code = '73211009').exists()"
* action[+]
  * title = "Laboratory (Urinalysis)"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Urinalysis"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "ADAS-Cog"
  * definitionUri = "Questionnaire/H2Q-MC-LZZT-ADAS-Cog"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Clinician's Interview-Based Impression of Change"
  * definitionUri = "Questionnaire/H2Q-MC-LZZT-CIBIC+"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Disability Assessment for Dementia"
  * definitionUri = "Questionnaire/H2Q-MC-LZZT-DAD"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Neuropsychiatric Inventory Questionnaire – Revised"
  * definitionUri = "Questionnaire/H2Q-MC-LZZT-NPI-X"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Informed-Consent"
    * relationship = #after
* action[+]
  * title = "Adverse events"
  * definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
  * relatedAction[+]
    * targetId = "VISIT-1-H2Q-MC-LZZT-Visit-Date"
    * relationship = #after
