Instance: H2Q-MC-LZZT-Bundle-4
InstanceOf: Bundle
Usage: #example
Title: "H2Q-MC-LZZT Bundle 4 — USDM-derived resources"
Description: "Fourth Deliverable — all resources generated from the USDM source (CDISC_Pilot_Study_v4_FIXED.json). Includes the ResearchStudy, visit PlanDefinitions with soaTimepoint timing and soaTransition graph edges, all ActivityDefinitions, ObservationDefinitions, Questionnaires, and eligibility Groups."
* type = #transaction

// ── Organization ------------------------------------------------

* entry[+].resource = Organization-1
* entry[=].fullUrl = "Organization/Organization-1"
* entry[=].request.method = #PUT
* entry[=].request.url = "Organization/Organization-1"

// ── Practitioner ------------------------------------------------

* entry[+].resource = Pers-001
* entry[=].fullUrl = "Practitioner/Pers-001"
* entry[=].request.method = #PUT
* entry[=].request.url = "Practitioner/Pers-001"

// ── ResearchStudy -----------------------------------------------

* entry[+].resource = H2Q-MC-LZZT-ResearchStudy-USDM
* entry[=].fullUrl = "ResearchStudy/H2Q-MC-LZZT-ResearchStudy-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "ResearchStudy/H2Q-MC-LZZT-ResearchStudy-USDM"

// ── Group -------------------------------------------------------

* entry[+].resource = H2Q-MC-LZZT-ResearchStudy-Inclusion-USDM
* entry[=].fullUrl = "Group/H2Q-MC-LZZT-ResearchStudy-Inclusion-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "Group/H2Q-MC-LZZT-ResearchStudy-Inclusion-USDM"

* entry[+].resource = H2Q-MC-LZZT-ResearchStudy-Exclusion-USDM
* entry[=].fullUrl = "Group/H2Q-MC-LZZT-ResearchStudy-Exclusion-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "Group/H2Q-MC-LZZT-ResearchStudy-Exclusion-USDM"

// ── ActivityDefinition ------------------------------------------

* entry[+].resource = usdm-act-adverse-events
* entry[=].fullUrl = "ActivityDefinition/usdm-act-adverse-events"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-adverse-events"

* entry[+].resource = usdm-act-ambulatory-ecg-placed
* entry[=].fullUrl = "ActivityDefinition/usdm-act-ambulatory-ecg-placed"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-ambulatory-ecg-placed"

* entry[+].resource = usdm-act-ambulatory-ecg-removed
* entry[=].fullUrl = "ActivityDefinition/usdm-act-ambulatory-ecg-removed"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-ambulatory-ecg-removed"

* entry[+].resource = usdm-act-check-adverse-events
* entry[=].fullUrl = "ActivityDefinition/usdm-act-check-adverse-events"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-check-adverse-events"

* entry[+].resource = usdm-act-chemistry
* entry[=].fullUrl = "ActivityDefinition/usdm-act-chemistry"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-chemistry"

* entry[+].resource = usdm-act-chest-x-ray
* entry[=].fullUrl = "ActivityDefinition/usdm-act-chest-x-ray"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-chest-x-ray"

* entry[+].resource = usdm-act-concomitant-medications
* entry[=].fullUrl = "ActivityDefinition/usdm-act-concomitant-medications"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-concomitant-medications"

* entry[+].resource = usdm-act-ct-scan
* entry[=].fullUrl = "ActivityDefinition/usdm-act-ct-scan"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-ct-scan"

* entry[+].resource = usdm-act-ecg
* entry[=].fullUrl = "ActivityDefinition/usdm-act-ecg"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-ecg"

* entry[+].resource = usdm-act-habits
* entry[=].fullUrl = "ActivityDefinition/usdm-act-habits"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-habits"

* entry[+].resource = usdm-act-hematology
* entry[=].fullUrl = "ActivityDefinition/usdm-act-hematology"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-hematology"

* entry[+].resource = usdm-act-hemoglobin-a1c
* entry[=].fullUrl = "ActivityDefinition/usdm-act-hemoglobin-a1c"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-hemoglobin-a1c"

* entry[+].resource = usdm-act-inclusion-and-exclusion-criteria
* entry[=].fullUrl = "ActivityDefinition/usdm-act-inclusion-and-exclusion-criteria"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-inclusion-and-exclusion-criteria"

* entry[+].resource = usdm-act-informed-consent
* entry[=].fullUrl = "ActivityDefinition/usdm-act-informed-consent"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-informed-consent"

* entry[+].resource = usdm-act-medical-history
* entry[=].fullUrl = "ActivityDefinition/usdm-act-medical-history"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-medical-history"

* entry[+].resource = usdm-act-patient-number-assigned
* entry[=].fullUrl = "ActivityDefinition/usdm-act-patient-number-assigned"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-patient-number-assigned"

* entry[+].resource = usdm-act-patient-randomised
* entry[=].fullUrl = "ActivityDefinition/usdm-act-patient-randomised"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-patient-randomised"

* entry[+].resource = usdm-act-physical-examination
* entry[=].fullUrl = "ActivityDefinition/usdm-act-physical-examination"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-physical-examination"

* entry[+].resource = usdm-act-plasma-specimen-xanomeline
* entry[=].fullUrl = "ActivityDefinition/usdm-act-plasma-specimen-xanomeline"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-plasma-specimen-xanomeline"

* entry[+].resource = usdm-act-study-drug-record-medications-dispensed-medicati-bf9d38
* entry[=].fullUrl = "ActivityDefinition/usdm-act-study-drug-record-medications-dispensed-medicati-bf9d38"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-study-drug-record-medications-dispensed-medicati-bf9d38"

* entry[+].resource = usdm-act-subject-standing
* entry[=].fullUrl = "ActivityDefinition/usdm-act-subject-standing"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-subject-standing"

* entry[+].resource = usdm-act-subject-supine
* entry[=].fullUrl = "ActivityDefinition/usdm-act-subject-supine"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-subject-supine"

* entry[+].resource = usdm-act-tts-acceptability-survey
* entry[=].fullUrl = "ActivityDefinition/usdm-act-tts-acceptability-survey"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-tts-acceptability-survey"

* entry[+].resource = usdm-act-uninalysis
* entry[=].fullUrl = "ActivityDefinition/usdm-act-uninalysis"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-uninalysis"

* entry[+].resource = usdm-act-vital-signs-and-temperature
* entry[=].fullUrl = "ActivityDefinition/usdm-act-vital-signs-and-temperature"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-vital-signs-and-temperature"

* entry[+].resource = usdm-act-vital-signs-while-standing
* entry[=].fullUrl = "ActivityDefinition/usdm-act-vital-signs-while-standing"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-vital-signs-while-standing"

* entry[+].resource = usdm-act-vital-signs-while-supine
* entry[=].fullUrl = "ActivityDefinition/usdm-act-vital-signs-while-supine"
* entry[=].request.method = #PUT
* entry[=].request.url = "ActivityDefinition/usdm-act-vital-signs-while-supine"

// ── Questionnaire -----------------------------------------------

* entry[+].resource = usdm-q-adas-cog
* entry[=].fullUrl = "Questionnaire/usdm-q-adas-cog"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-adas-cog"

* entry[+].resource = usdm-q-apo-e-genotype
* entry[=].fullUrl = "Questionnaire/usdm-q-apo-e-genotype"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-apo-e-genotype"

* entry[+].resource = usdm-q-cibic-plus
* entry[=].fullUrl = "Questionnaire/usdm-q-cibic-plus"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-cibic-plus"

* entry[+].resource = usdm-q-dad
* entry[=].fullUrl = "Questionnaire/usdm-q-dad"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-dad"

* entry[+].resource = usdm-q-date-of-birth
* entry[=].fullUrl = "Questionnaire/usdm-q-date-of-birth"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-date-of-birth"

* entry[+].resource = usdm-q-haschinski-ischemic-scale
* entry[=].fullUrl = "Questionnaire/usdm-q-haschinski-ischemic-scale"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-haschinski-ischemic-scale"

* entry[+].resource = usdm-q-mmse
* entry[=].fullUrl = "Questionnaire/usdm-q-mmse"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-mmse"

* entry[+].resource = usdm-q-npi-x
* entry[=].fullUrl = "Questionnaire/usdm-q-npi-x"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-npi-x"

* entry[+].resource = usdm-q-placebo-tts-test
* entry[=].fullUrl = "Questionnaire/usdm-q-placebo-tts-test"
* entry[=].request.method = #PUT
* entry[=].request.url = "Questionnaire/usdm-q-placebo-tts-test"

// ── ObservationDefinition ---------------------------------------

* entry[+].resource = usdm-obs-vscat1-panel-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-vscat1-panel-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-vscat1-panel-obs"

* entry[+].resource = usdm-obs-vscat2-panel-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-vscat2-panel-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-vscat2-panel-obs"

* entry[+].resource = usdm-obs-vital-signs-and-temperature-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-vital-signs-and-temperature-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-vital-signs-and-temperature-obs"

* entry[+].resource = usdm-obs-vital-signs-while-supine-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-vital-signs-while-supine-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-vital-signs-while-supine-obs"

* entry[+].resource = usdm-obs-vital-signs-while-standing-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-vital-signs-while-standing-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-vital-signs-while-standing-obs"

* entry[+].resource = usdm-obs-hematology-lab-panel
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-hematology-lab-panel"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-hematology-lab-panel"

* entry[+].resource = usdm-obs-hemoglobin
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-hemoglobin"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-hemoglobin"

* entry[+].resource = usdm-obs-hematocrit
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-hematocrit"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-hematocrit"

* entry[+].resource = usdm-obs-rbc
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-rbc"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-rbc"

* entry[+].resource = usdm-obs-mcv
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-mcv"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-mcv"

* entry[+].resource = usdm-obs-mch
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-mch"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-mch"

* entry[+].resource = usdm-obs-mchc
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-mchc"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-mchc"

* entry[+].resource = usdm-obs-wbc
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-wbc"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-wbc"

* entry[+].resource = usdm-obs-neutrophils-seg
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-neutrophils-seg"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-neutrophils-seg"

* entry[+].resource = usdm-obs-neutrophils-bands
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-neutrophils-bands"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-neutrophils-bands"

* entry[+].resource = usdm-obs-lymphocytes
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-lymphocytes"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-lymphocytes"

* entry[+].resource = usdm-obs-monocytes
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-monocytes"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-monocytes"

* entry[+].resource = usdm-obs-eosinophils
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-eosinophils"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-eosinophils"

* entry[+].resource = usdm-obs-basophils
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-basophils"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-basophils"

* entry[+].resource = usdm-obs-platelet
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-platelet"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-platelet"

* entry[+].resource = usdm-obs-cell-morphology
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-cell-morphology"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-cell-morphology"

* entry[+].resource = usdm-obs-chemistry-lab-panel
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-chemistry-lab-panel"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-chemistry-lab-panel"

* entry[+].resource = usdm-obs-sodium
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-sodium"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-sodium"

* entry[+].resource = usdm-obs-potassium
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-potassium"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-potassium"

* entry[+].resource = usdm-obs-bicarbonate
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-bicarbonate"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-bicarbonate"

* entry[+].resource = usdm-obs-chloride
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-chloride"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-chloride"

* entry[+].resource = usdm-obs-total-bilirubin
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-total-bilirubin"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-total-bilirubin"

* entry[+].resource = usdm-obs-alp
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-alp"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-alp"

* entry[+].resource = usdm-obs-ggt
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-ggt"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-ggt"

* entry[+].resource = usdm-obs-alt-sgpt
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-alt-sgpt"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-alt-sgpt"

* entry[+].resource = usdm-obs-ast-sgot
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-ast-sgot"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-ast-sgot"

* entry[+].resource = usdm-obs-bun
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-bun"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-bun"

* entry[+].resource = usdm-obs-creatinine
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-creatinine"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-creatinine"

* entry[+].resource = usdm-obs-uric-acid
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-uric-acid"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-uric-acid"

* entry[+].resource = usdm-obs-phosphorus
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-phosphorus"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-phosphorus"

* entry[+].resource = usdm-obs-calcium
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-calcium"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-calcium"

* entry[+].resource = usdm-obs-glucose-nonfasting
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-glucose-nonfasting"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-glucose-nonfasting"

* entry[+].resource = usdm-obs-total-protein
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-total-protein"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-total-protein"

* entry[+].resource = usdm-obs-albumin
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-albumin"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-albumin"

* entry[+].resource = usdm-obs-cholesterol
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-cholesterol"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-cholesterol"

* entry[+].resource = usdm-obs-ck
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-ck"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-ck"

* entry[+].resource = usdm-obs-uninalysis-lab-panel
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-uninalysis-lab-panel"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-uninalysis-lab-panel"

* entry[+].resource = usdm-obs-color
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-color"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-color"

* entry[+].resource = usdm-obs-specific-gravity
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-specific-gravity"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-specific-gravity"

* entry[+].resource = usdm-obs-ph
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-ph"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-ph"

* entry[+].resource = usdm-obs-protein
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-protein"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-protein"

* entry[+].resource = usdm-obs-glucose
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-glucose"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-glucose"

* entry[+].resource = usdm-obs-ketones
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-ketones"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-ketones"

* entry[+].resource = usdm-obs-bilirubin
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-bilirubin"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-bilirubin"

* entry[+].resource = usdm-obs-urobilinogen
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-urobilinogen"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-urobilinogen"

* entry[+].resource = usdm-obs-blood
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-blood"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-blood"

* entry[+].resource = usdm-obs-nitrite
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-nitrite"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-nitrite"

* entry[+].resource = usdm-obs-sediment-microscopy
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-sediment-microscopy"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-sediment-microscopy"

* entry[+].resource = usdm-obs-thyroid-lab-panel
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-thyroid-lab-panel"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-thyroid-lab-panel"

* entry[+].resource = usdm-obs-free-thyroid-index
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-free-thyroid-index"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-free-thyroid-index"

* entry[+].resource = usdm-obs-t3-uptake
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-t3-uptake"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-t3-uptake"

* entry[+].resource = usdm-obs-t4
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-t4"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-t4"

* entry[+].resource = usdm-obs-tsh
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-tsh"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-tsh"

* entry[+].resource = usdm-obs-other-lab-panel
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-other-lab-panel"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-other-lab-panel"

* entry[+].resource = usdm-obs-folate
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-folate"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-folate"

* entry[+].resource = usdm-obs-vitamin-b12
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-vitamin-b12"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-vitamin-b12"

* entry[+].resource = usdm-obs-syphilis-screening
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-syphilis-screening"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-syphilis-screening"

* entry[+].resource = usdm-obs-hba1c
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-hba1c"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-hba1c"

* entry[+].resource = usdm-obs-informed-consent-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-informed-consent-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-informed-consent-obs"

* entry[+].resource = usdm-obs-physical-examination-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-physical-examination-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-physical-examination-obs"

* entry[+].resource = usdm-obs-medical-history-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-medical-history-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-medical-history-obs"

* entry[+].resource = usdm-obs-habits-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-habits-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-habits-obs"

* entry[+].resource = usdm-obs-ecg-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-ecg-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-ecg-obs"

* entry[+].resource = usdm-obs-concomitant-medications-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-concomitant-medications-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-concomitant-medications-obs"

* entry[+].resource = usdm-obs-hemoglobin-a1c-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-hemoglobin-a1c-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-hemoglobin-a1c-obs"

* entry[+].resource = usdm-obs-adverse-events-obs
* entry[=].fullUrl = "ObservationDefinition/usdm-obs-adverse-events-obs"
* entry[=].request.method = #PUT
* entry[=].request.url = "ObservationDefinition/usdm-obs-adverse-events-obs"

// ── PlanDefinition ----------------------------------------------

* entry[+].resource = H2Q-MC-LZZT-ProtocolDesign-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-ProtocolDesign-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-ProtocolDesign-USDM"

* entry[+].resource = H2Q-MC-LZZT-E1-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E1-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E1-USDM"

* entry[+].resource = H2Q-MC-LZZT-E2-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E2-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E2-USDM"

* entry[+].resource = H2Q-MC-LZZT-E3-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E3-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E3-USDM"

* entry[+].resource = H2Q-MC-LZZT-E4-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E4-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E4-USDM"

* entry[+].resource = H2Q-MC-LZZT-E5-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E5-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E5-USDM"

* entry[+].resource = H2Q-MC-LZZT-E7-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E7-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E7-USDM"

* entry[+].resource = H2Q-MC-LZZT-E8-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E8-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E8-USDM"

* entry[+].resource = H2Q-MC-LZZT-E9-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E9-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E9-USDM"

* entry[+].resource = H2Q-MC-LZZT-E10-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E10-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E10-USDM"

* entry[+].resource = H2Q-MC-LZZT-E11-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E11-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E11-USDM"

* entry[+].resource = H2Q-MC-LZZT-E12-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E12-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E12-USDM"

* entry[+].resource = H2Q-MC-LZZT-E13-USDM
* entry[=].fullUrl = "PlanDefinition/H2Q-MC-LZZT-E13-USDM"
* entry[=].request.method = #PUT
* entry[=].request.url = "PlanDefinition/H2Q-MC-LZZT-E13-USDM"
