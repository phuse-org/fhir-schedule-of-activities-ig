Instance: H2Q-MC-LZZT-ResearchStudy-Inclusion
InstanceOf: Group
Title: "H2Q-MC-LZZT Inclusion Criteria"
Description: "H2Q-MC-LZZT Inclusion Criteria"
Usage: #example
* type = #person
* actual = false
* identifier[+].value = "H2Q-MC-LZZT-InclusionCriteria" 
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* characteristic[+].code.text = "Males and postmenopausal females at least 50 years of age."
* characteristic[=].exclude = false
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Diagnosis of probable AD as defined by National Institute of Neurological and Communicative Disorders and Stroke (NINCDS) and the Alzheimer’s Disease and Related Disorders Association (ADRDA) guidelines"
// This is purely for record basis - not validated
* characteristic[=].extension.url = "http://hl7.org/fhir/StructureDefinition/cqf-expression"
* characteristic[=].extension.valueExpression.language = #text/cql
* characteristic[=].extension.valueExpression.expression = "exists [Condition: Alzheimer's disease]"
* characteristic.exclude = false
* characteristic[=].exclude = false
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "MMSE score of 10 to 23."
* characteristic[=].exclude = false
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Hachinski Ischemic Scale score of ≤4"
* characteristic[=].exclude = false
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "CNS imaging (CT scan or MRI of brain) compatible with AD within past 1 year."
* characteristic[=].exclude = false
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Investigator has obtained informed consent signed by the patient (and/or legal representative) and by the caregiver."
* characteristic[=].exclude = false
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Geographic proximity to investigator’s site that allows adequate follow-up."
* characteristic[=].exclude = false
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A reliable caregiver who is in frequent or daily contact with the patient and who will accompany the patient to the office and/or be available by telephone at designated times, will monitor administration of prescribed medications, and will be responsible for the overall care of the patient at home. The caregiver and the patient must be able to communicate in English and willing to comply with 26 weeks of transdermal therapy."
* characteristic[=].exclude = false
* characteristic[=].valueBoolean = true

Instance: H2Q-MC-LZZT-ResearchStudy-Exclusion
InstanceOf: Group
Title: "H2Q-MC-LZZT Exclusion Criteria"
Description: "H2Q-MC-LZZT Exclusion Criteria"
Usage: #example
* type = #person
* actual = false
* identifier[+].value = "H2Q-MC-LZZT-ExclusionCriteria" 
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* characteristic[+].code.text = "Persons who have previously completed or withdrawn from this study or any other study investigating xanomeline TTS or the oral formulation of xanomeline."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Use of any investigational agent or approved Alzheimer’s therapeutic medication within 30 days prior to enrollment into the study."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Serious illness which required hospitalization within 3 months of screening."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Stroke or vascular dementia documented by clinical history and/or radiographic findings interpretable by the investigator as indicative of these disorders"
* characteristic[=].valueBoolean = true
* characteristic[=].exclude = true
* characteristic[+].code.text = "Seizure disorder other than simple childhood febrile seizures"
* characteristic[=].valueBoolean = true
* characteristic[=].exclude = true
* characteristic[+].code.text = "Severe head trauma resulting in protracted loss of consciousness within the last 5 years, or multiple episodes of head trauma"
* characteristic[=].valueBoolean = true
* characteristic[=].exclude = true
* characteristic[+].code.text = "Parkinson’s disease"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Multiple sclerosis"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Amyotrophic lateral sclerosis"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Myasthenia gravis"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Episode of depression meeting DSM-IV criteria within 3 months of screening."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Schizophrenia."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Bipolar Disease."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Ethanol or psychoactive drug abuse or dependence."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history of syncope within the last 5 years."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Evidence from ECG recording of Left bundle branch block."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Evidence from ECG recording of Bradycardia ≤50 beats per minute"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Evidence from ECG recording of Sinus pauses >2 seconds"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Evidence from ECG recording of Second or third degree heart block unless treated with a pacemaker"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Evidence from ECG recording of Wolff-Parkinson-White syndrome"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Evidence from ECG recording of Sustained supraventricular tachyarrhythmia including SVT≥10 sec, atrial fibrillation, atrial flutter."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "Evidence from ECG recording of Ventricular tachycardia at a rate of ≥120 beats per minute lasting ≥10 seconds."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Clinically significant arrhythmia"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Symptomatic sick sinus syndrome not treated with a pacemaker"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Congestive heart failure refractory to treatment"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Angina except angina controlled with PRN nitroglycerin"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Resting heart rate <50 or >100 beats per minute, on physical exam"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of Uncontrolled hypertension."
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
* characteristic[+].code.text = "A history within the last 5 years of a serious gastrointestinal disorder"
* characteristic[=].exclude = true
* characteristic[=].valueBoolean = true
