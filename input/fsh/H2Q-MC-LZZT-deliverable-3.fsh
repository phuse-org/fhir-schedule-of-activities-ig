Instance: H2Q-MC-LZZT-Bundle-3
InstanceOf: Bundle
Usage: #example
Title: "H2Q-MC-LZZT Bundle 3"
Description: "Third Deliverable for the PHUSE Project"
* type = #transaction
* entry[+].resource = SamGetWell
* entry[=].fullUrl = "Practitioner/SamGetWell"
* entry[=].request.method = #PUT
* entry[=].request.url = "Practitioner?identifier=ABC1234"
* entry[=].request.ifNoneExist = "identifier=ABC1234"
* entry[+].resource = EliLillyAndCompany
* entry[=].fullUrl = "Organization/EliLillyAndCompany"
* entry[=].request.url = "Organization?identifier=Eli%20Lilly%20and%20Company%20Inc"
* entry[=].request.method = #PUT
* entry[=].request.ifNoneExist = "identifier=Eli%20Lilly%20and%20Company"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-1
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-1"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.SCREENING_VISIT"
* entry[+].resource = H2Q-MC-LZZT-Visit-Date
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Visit-Date"
* entry[+].resource = H2Q-MC-LZZT-Chest-x-ray
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Chest-x-ray"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Chest-x-ray"
* entry[+].resource = H2Q-MC-LZZT-Informed-Consent
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Informed-Consent"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Informed-Consent"
* entry[+].resource = H2Q-MC-LZZT-Patient-number-assigned
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Patient-number-assigned"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Patient-number-assigned"
* entry[+].resource = H2Q-MC-LZZT-Hachinski-4
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Hachinski-4"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Hachinski-4"
* entry[+].resource = H2Q-MC-LZZT-MMSE-10-23
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-MMSE-10-23"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-MMSE-10-23"
* entry[+].resource = H2Q-MC-LZZT-Physical-examination
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Physical-examination"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Physical-examination"
* entry[+].resource = H2Q-MC-LZZT-Placebo-TTS-test
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Placebo-TTS-test"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Placebo-TTS-test"
* entry[+].resource = H2Q-MC-LZZT-Medical-History
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Medical-History"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Medical-History"
* entry[+].resource = H2Q-MC-LZZT-Habits-Alcohol
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Habits-Alcohol"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Habits-Alcohol"
* entry[+].resource = H2Q-MC-LZZT-Habits-Caffeine
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Habits-Caffeine"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Habits-Caffeine"
* entry[+].resource = H2Q-MC-LZZT-Habits-Smoking
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Habits-Smoking"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Habits-Smoking"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-HEIGHT
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-HEIGHT"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-HEIGHT"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-Height-PD
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-Height-PD"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-Height-PD"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-WEIGHT
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-WEIGHT"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-WEIGHT"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-Weight-PD
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-Weight-PD"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-Weight-PD"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-TEMP
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-TEMP"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-TEMP"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-Temperature-PD
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-Temperature-PD"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-PULSE-SUPINE"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-SYSBP-SUPINE"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-DIABP-SUPINE"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-PULSE-STANDING"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-SYSBP-STANDING"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-DIABP-STANDING"
* entry[+].resource = H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Vital-Signs-HeartRate-BloodPressure"
* entry[+].resource = H2Q-MC-LZZT-ECG
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-ECG"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-ECG"
* entry[+].resource = H2Q-MC-LZZT-CT-Scan
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-CT-Scan"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-CT-Scan"
* entry[+].resource = H2Q-MC-LZZT-Concomitant-Medications
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Concomitant-Medications"
* entry[+].resource = H2Q-MC-LZZT-Laboratory-Hemat
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Hemat"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Laboratory-Hemat"
* entry[+].resource = H2Q-MC-LZZT-Laboratory-Chem
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Chem"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Laboratory-Chem"
* entry[+].resource = H2Q-MC-LZZT-Laboratory-Urinalysis
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Urinalysis"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Laboratory-Urinalysis"
* entry[+].resource = H2Q-MC-LZZT-Hemoglobin-A1C
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Hemoglobin-A1C"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Hemoglobin-A1C"
* entry[+].resource = H2Q-MC-LZZT-ADAS-Cog
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-ADAS-Cog"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-ADAS-Cog"
* entry[+].resource = H2Q-MC-LZZT-CIBIC
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-CIBIC"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-CIBIC"
* entry[+].resource = H2Q-MC-LZZT-DAD
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-DAD"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-DAD"
* entry[+].resource = H2Q-MC-LZZT-NPI-X
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-NPI-X"
* entry[+].resource = H2Q-MC-LZZT-Adverse-events
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Adverse-events"
* entry[+].resource = H2Q-MC-LZZT-Ambulatory-ECG-placed
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Ambulatory-ECG-placed"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Ambulatory-ECG-placed"
* entry[+].resource = H2Q-MC-LZZT-Ambulatory-ECG-removed
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Ambulatory-ECG-removed"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Ambulatory-ECG-removed"
* entry[+].resource = H2Q-MC-LZZT-Patient-randomized
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Patient-randomized"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Patient-randomized"
* entry[+].resource = H2Q-MC-LZZT-Plasma-Specimen
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Plasma-Specimen"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Plasma-Specimen"
* entry[+].resource = H2Q-MC-LZZT-Study-drug-record
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Study-drug-record"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-2
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-2"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.AMB_ECG_VISIT"
* entry[+].resource = H2Q-MC-LZZT-Adverse-events
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Adverse-events"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-3
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-3"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.RANDOMIZATION_VISIT"
* entry[+].resource = H2Q-MC-LZZT-Apo-E-genotyping
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-Apo-E-genotyping"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-Apo-E-genotyping"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-4
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-4"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_01"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-5
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-5"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_02"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-6
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-6"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_03"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-7
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-7"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_04"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-8
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-8"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_05"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-9
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-9"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_06"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-10
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-10"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_07"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-11
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-11"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_08"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-12
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-12"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_09"
* entry[+].resource = H2Q-MC-LZZT-Study-Visit-13
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-13"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.TRT_VISIT_10"
* entry[+].resource = H2Q-MC-LZZT-TTS-Acceptability-Survey
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-TTS-Acceptability-Survey"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-TTS-Acceptability-Survey"
* entry[+].resource = H2Q-MC-LZZT-Study-ET-14
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-ET-14"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.EARLY_TERM_VISIT"
* entry[+].resource = H2Q-MC-LZZT-Study-RT-15
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-RT-15"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=H2Q-MC-LZZT-Study-RT-15"
* entry[+].resource = H2Q-MC-LZZT-PT-SUMMARY
* entry[=].fullUrl = "ActivityDefinition/H2Q-MC-LZZT-PT-SUMMARY"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition?identifier=H2Q-MC-LZZT-PT-SUMMARY"
* entry[+].resource = H2Q-MC-LZZT-Study-RT-15
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-Study-RT-15"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=SE.RETRIEVAL_TERM_VISIT"
* entry[+].resource = H2Q-MC-LZZT-ResearchStudy-Inclusion
* entry[=].fullUrl = "Group/H2Q-MC-LZZT-ResearchStudy-Inclusion"
* entry[=].request.method = #PUT
* entry[=].request.url = "Group?identifier=H2Q-MC-LZZT-InclusionCriteria"
* entry[+].resource = H2Q-MC-LZZT-ResearchStudy-Exclusion
* entry[=].fullUrl = "Group/H2Q-MC-LZZT-ResearchStudy-Exclusion"
* entry[=].request.method = #PUT 
* entry[=].request.url =  "Group?identifier=H2Q-MC-LZZT-InclusionCriteria"
* entry[+].resource = H2Q-MC-LZZT-ProtocolDesign
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-ProtocolDesign"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition?identifier=H2Q-MC-LZZT-ProtocolDesign"
* entry[+].resource = H2Q-MC-LZZT-ResearchStudy
* entry[=].fullUrl = "ResearchStudy/H2Q-MC-LZZT-ResearchStudy"
* entry[=].request.method = #PUT
* entry[=].request.url = "ResearchStudy?identifier=H2Q-MC-LZZT"
* entry[=].request.ifNoneExist = "identifier=H2Q-MC-LZZT"