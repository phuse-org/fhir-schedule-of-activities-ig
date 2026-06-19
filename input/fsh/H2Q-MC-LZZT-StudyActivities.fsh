Instance: H2Q-MC-LZZT-DAD
InstanceOf: ActivityDefinition
Description: "Planned Activity [DAD]"
Usage: #example
Title: "Disability Assessment for Dementia"
* status = #active
* identifier[+].value = "F.DAD"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/DAD-Observations"
* observationResultRequirement = "ObservationDefinition/DAD-Observations"

Instance: H2Q-MC-LZZT-Medications-returned
InstanceOf: ActivityDefinition
Description: "Planned Activity [Medications returned]"
Usage: #example
Title: "Medications returned"
* status = #active
* observationRequirement = "ObservationDefinition/Medications-returned-Observations"
* observationResultRequirement = "ObservationDefinition/Medications-returned-Observations"

Instance: H2Q-MC-LZZT-Medications-dispensed
InstanceOf: ActivityDefinition
Description: "Planned Activity [Medications dispensed]"
Usage: #example
Title: "Medications dispensed"
* status = #active
* identifier[+].value = "F.EX_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Medications-dispensed-Observations"
* observationResultRequirement = "ObservationDefinition/Medications-dispensed-Observations"

Instance: H2Q-MC-LZZT-Ambulatory-ECG-removed
InstanceOf: ActivityDefinition
Description: "Planned Activity [Ambulatory ECG removed]"
Usage: #example
Title: "Ambulatory ECG removed"
* status = #active
* identifier[+].value = "F.PR_ECG_2"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Ambulatory-ECG-removed-Observations"
* observationResultRequirement = "ObservationDefinition/Ambulatory-ECG-removed-Observations"

Instance: H2Q-MC-LZZT-Laboratory-Urinalysis
InstanceOf: ActivityDefinition
Description: "Planned Activity [Laboratory (Urinalysis)]"
Usage: #example
Title: "Laboratory (Urinalysis)"
* status = #active
* identifier[+].value = "F.LB_URINE"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Laboratory-Urinalysis-Observations"
* observationResultRequirement = "ObservationDefinition/Laboratory-Urinalysis-Observations"

Instance: H2Q-MC-LZZT-Physical-examination
InstanceOf: ActivityDefinition
Description: "Planned Activity [Physical examination]"
Usage: #example
Title: "Physical examination"
* status = #active
* observationRequirement = "ObservationDefinition/Physical-examination-Observations"
* observationResultRequirement = "ObservationDefinition/Physical-examination-Observations"

Instance: H2Q-MC-LZZT-Adverse-events
InstanceOf: ActivityDefinition
Description: "Planned Activity [Adverse events]"
Usage: #example
Title: "Adverse events"
* status = #active
* identifier[+].value = "F.AE_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Adverse-events-Observations"
* observationResultRequirement = "ObservationDefinition/Adverse-events-Observations"

Instance: H2Q-MC-LZZT-Patient-number-assigned
InstanceOf: ActivityDefinition
Description: "Planned Activity [Patient number assigned]"
Usage: #example
Title: "Patient number assigned"
* status = #active
* identifier[+].value = "F.DM_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Patient-number-assigned-Observations"
* observationResultRequirement = "ObservationDefinition/Patient-number-assigned-Observations"

Instance: H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure
InstanceOf: PlanDefinition
Description: "Planned Activity [Heart Rate and Blood Pressure]"
Usage: #example
Title: "Vital Signs: Heart Rate and Blood Pressure"
* status = #active
* identifier[+].value = "F.VS_4"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* action[+].title = "Supine Pulse"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE"
* action[+].title = "Supine Systolic BP"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE"
* action[+].title = "Supine Diastolic BP"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE"
* action[+].title = "Pulse (after 3m standing)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING"
* action[+].title = "Systolic BP (after 3m standing)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING"
* action[+].title = "Diastolic BP (after 3m standing)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING"

Instance: H2Q-MC-LZZT-Vital-Signs-Height-PD
InstanceOf: PlanDefinition
Description: "Planned Activity [Vital signs] - Height"
Usage: #example
Title: "Vital signs/Height"
* status = #active
* identifier[+].value = "F.VS_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* action[+].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-HEIGHT"
* action[=].title = "Height"

Instance: H2Q-MC-LZZT-Vital-Signs-Weight-PD
InstanceOf: PlanDefinition
Description: "Planned Activity [Vital signs] - Weight"
Usage: #example
Title: "Vital signs/Weight"
* status = #active
* identifier[+].value = "F.VS_2"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* action[+].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-WEIGHT"
* action[=].title = "Weight"

Instance: H2Q-MC-LZZT-Vital-Signs-Temperature-PD
InstanceOf: PlanDefinition
Description: "Planned Activity [Vital signs] - Temperature"
Usage: #example
Title: "Vital signs/Temperature"
* status = #active
* identifier[+].value = "F.VS_3"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* action[+].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vitalsigns-Temperature"
* action[=].title = "Body Temperature"

Instance: H2Q-MC-LZZT-Medical-History
InstanceOf: ActivityDefinition
Description: "Planned Activity [Medical History]"
Usage: #example
Title: "Medical History"
* status = #active
* identifier[+].value = "F.MH_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Medical-History-Observations"
* observationResultRequirement = "ObservationDefinition/Medical-History-Observations"

Instance: H2Q-MC-LZZT-Chest-x-ray
InstanceOf: ActivityDefinition
Description: "Planned Activity [Chest x-ray]"
Usage: #example
Title: "Chest x-ray"
* status = #active
* identifier[+].value = "F.PR_CHESTXRAY"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Chest-x-ray-Observations"
* observationResultRequirement = "ObservationDefinition/Chest-x-ray-Observations"

Instance: H2Q-MC-LZZT-Placebo-TTS-test
InstanceOf: ActivityDefinition
Description: "Planned Activity [Placebo TTS test]"
Usage: #example
Title: "Placebo TTS test"
* status = #active
* observationRequirement = "ObservationDefinition/Placebo-TTS-test-Observations"
* observationResultRequirement = "ObservationDefinition/Placebo-TTS-test-Observations"

Instance: H2Q-MC-LZZT-CIBIC
InstanceOf: ActivityDefinition
Description: "Planned Activity [CIBIC+]"
Usage: #example
Title: "Clinician's Interview-Based Impression of Change"
* status = #active
* identifier[+].value = "F.CIBC+"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/CIBIC-Observations"
* observationResultRequirement = "ObservationDefinition/CIBIC-Observations"

Instance: H2Q-MC-LZZT-Laboratory-Chem
InstanceOf: ActivityDefinition
Description: "Planned Activity [Laboratory (Chem)]"
Usage: #example
Title: "Laboratory (Blood Chemistry)"
* status = #active
* identifier[+].value = "F.LB_CHEM"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Laboratory-Chem-Observations"
* observationResultRequirement = "ObservationDefinition/Laboratory-Chem-Observations"

Instance: H2Q-MC-LZZT-Laboratory-Hemat
InstanceOf: ActivityDefinition
Description: "Planned Activity [Laboratory (Hemat)]"
Usage: #example
Title: "Laboratory (Hematology)"
* status = #active
* identifier[+].value = "F.LB_HEM"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/Laboratory-Hemat-Observations"
* observationResultRequirement = "ObservationDefinition/Laboratory-Hemat-Observations"

Instance: H2Q-MC-LZZT-Apo-E-genotyping
InstanceOf: ActivityDefinition
Description: "Planned Activity [Apo E genotyping]"
Usage: #example
Title: "Apo E genotyping"
* status = #active
* observationRequirement = "ObservationDefinition/Apo-E-genotyping-Observations"
* observationResultRequirement = "ObservationDefinition/Apo-E-genotyping-Observations"

Instance: H2Q-MC-LZZT-TTS-Acceptability-Survey
InstanceOf: ActivityDefinition
Description: "Planned Activity [TTS Acceptability Survey]"
Usage: #example
Title: "TTS Acceptability Survey"
* status = #active
* identifier[+].value = "F.TTSACC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = "ObservationDefinition/TTS-Acceptability-Survey-Observations"
* observationResultRequirement = "ObservationDefinition/TTS-Acceptability-Survey-Observations"

/*
The Visit Date activity represents an initiating action with a planned event
*/
Instance: H2Q-MC-LZZT-Visit-Date
InstanceOf: ActivityDefinition
Description: "Planned Activity [Record Visit Date]"
Usage: #example
Title: "Visit Date"
* status = #active
* identifier[+].value = "F.DOV"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary


Instance: H2Q-MC-LZZT-Plasma-Specimen
InstanceOf: ActivityDefinition
Description: "Planned Activity [Plasma Specimen (Xanomeline)]"
Usage: #example
Title: "Plasma Specimen (Xanomeline)"
* status = #active
* observationRequirement = "ObservationDefinition/Plasma-Specimen-Observations"
* observationResultRequirement = "ObservationDefinition/Plasma-Specimen-Observations"

Instance: H2Q-MC-LZZT-Habits-Alcohol
InstanceOf: ActivityDefinition
Description: "Planned Activity [Habits - Alcohol]"
Usage: #example
Title: "Habits - Alcohol"
* status = #active
* identifier[+].value = "F.SU_ALCOHOL"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/Habits-Observations-Alcohol"
* observationResultRequirement = "ObservationDefinition/Habits-Observations-Alcohol"

Instance: H2Q-MC-LZZT-Habits-Caffeine
InstanceOf: ActivityDefinition
Description: "Planned Activity [Habits - Caffeine]"
Usage: #example
Title: "Habits - Caffeine"
* status = #active
* identifier[+].value = "F.SU_CAFFEINE"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/Habits-Observations-Caffeine"
* observationResultRequirement = "ObservationDefinition/Habits-Observations-Caffeine"

Instance: H2Q-MC-LZZT-Habits-Smoking
InstanceOf: ActivityDefinition
Description: "Planned Activity [Habits - Smoking]"
Usage: #example
Title: "Habits - Smoking"
* status = #active
* identifier[+].value = "F.SU_SMOKING"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/Habits-Observations-Smoking"
* observationResultRequirement = "ObservationDefinition/Habits-Observations-Smoking"

Instance: H2Q-MC-LZZT-Hemoglobin-A1C
InstanceOf: ActivityDefinition
Description: "Planned Activity [Hemoglobin A1C]"
Usage: #example
Title: "Hemoglobin A1C"
* status = #active
// TODO: separate out
* observationRequirement = "ObservationDefinition/Hemoglobin-A1C-Observations"
* observationResultRequirement = "ObservationDefinition/Hemoglobin-A1C-Observations"

Instance: H2Q-MC-LZZT-Study-drug-record
InstanceOf: ActivityDefinition
Description: "Planned Activity [Study drug record: Medications Dispensed/Returned]"
Usage: #example
Title: "Study drug record: Medications Dispensed/Returned: Medications Dispensed/Returned"
* status = #active
* identifier[+].value = "F.EX_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/Study-drug-record-Observations"
* observationResultRequirement = "ObservationDefinition/Study-drug-record-Observations"

Instance: H2Q-MC-LZZT-ADAS-Cog
InstanceOf: ActivityDefinition
Description: "Planned Activity [ADAS-Cog]"
Usage: #example
Title: "ADAS-Cog"
* status = #active
* identifier[+].value = "F.ADAS-COG"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/ADAS-Cog-Observations"
* observationResultRequirement = "ObservationDefinition/ADAS-Cog-Observations"

Instance: H2Q-MC-LZZT-CT-Scan
InstanceOf: ActivityDefinition
Description: "Planned Activity [CT Scan]"
Usage: #example
Title: "CT Scan"
* status = #active
* identifier[+].value = "F.PR_CTSCAN"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/CT-Scan-Observations"
* observationResultRequirement = "ObservationDefinition/CT-Scan-Observations"

Instance: H2Q-MC-LZZT-Hachinski-4
InstanceOf: ActivityDefinition
Description: "Planned Activity [Hachinski 4]"
Usage: #example
Title: "Hachinski 4"
* status = #active
* identifier[+].value = "F.MHIS-NACC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/Hachinski-4-Observations"
* observationResultRequirement = "ObservationDefinition/Hachinski-4-Observations"

Instance: H2Q-MC-LZZT-Patient-randomized
InstanceOf: ActivityDefinition
Description: "Planned Activity [Patient randomized]"
Usage: #example
Title: "Patient randomized"
* status = #active
* observationRequirement = "ObservationDefinition/Patient-randomized-Observations"
* observationResultRequirement = "ObservationDefinition/Patient-randomized-Observations"

Instance: H2Q-MC-LZZT-Ambulatory-ECG-placed
InstanceOf: ActivityDefinition
Description: "Planned Activity [Ambulatory ECG placed]"
Usage: #example
Title: "Ambulatory ECG placed"
* status = #active
* identifier[+].value = "F.PR_ECG_2"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/Ambulatory-ECG-placed-Observations"
* observationResultRequirement = "ObservationDefinition/Ambulatory-ECG-placed-Observations"

Instance: H2Q-MC-LZZT-Informed-Consent
InstanceOf: ActivityDefinition
Description: "Planned Activity [Informed Consent]"
Usage: #example
Title: "Informed Consent"
* status = #active
* identifier[+].value = "F.DS_IC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/Informed-Consent-Observations"
* observationResultRequirement = "ObservationDefinition/Informed-Consent-Observations"

Instance: H2Q-MC-LZZT-MMSE-10-23
InstanceOf: ActivityDefinition
Description: "Planned Activity [MMSE 10-23]"
Usage: #example
Title: "MMSE 10-23"
* status = #active
* identifier[+].value = "F.MMSE"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/MMSE-10-23-Observations"
* observationResultRequirement = "ObservationDefinition/MMSE-10-23-Observations"

Instance: H2Q-MC-LZZT-Concomitant-Medications
InstanceOf: ActivityDefinition
Description: "Planned Activity [Concomitant Medications]"
Usage: #example
Title: "Concomitant Medications"
* status = #active
* identifier[+].value = "F.CM_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/Concomitant-Medications-Observations"
* observationResultRequirement = "ObservationDefinition/Concomitant-Medications-Observations"

Instance: H2Q-MC-LZZT-ECG
InstanceOf: ActivityDefinition
Description: "Planned Activity [ECG]"
Usage: #example
Title: "ECG"
* status = #active
* identifier[+].value = "F.ECG_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/ECG-Observations"
* observationResultRequirement = "ObservationDefinition/ECG-Observations"

Instance: H2Q-MC-LZZT-NPI-X
InstanceOf: ActivityDefinition
Description: "Planned Activity [NPI-X]"
Usage: #example
Title: "Neuropsychiatric Inventory Questionnaire – Revised"
* status = #active
* identifier[+].value = "F.NPI-X"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = "ObservationDefinition/NPI-X-Observations"
* observationResultRequirement = "ObservationDefinition/NPI-X-Observations"

