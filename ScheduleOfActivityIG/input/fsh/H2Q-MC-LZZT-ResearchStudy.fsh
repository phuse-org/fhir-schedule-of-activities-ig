Alias: NCIT = http://ncimeta.nci.nih.gov
Alias: SCT = http://snomed.info/sct
// TODO: Fix this
Alias: MEDDRA = http://snomed.info/sct
// TODO: Fix this
Alias: ICD10 = http://snomed.info/sct
// TODO: Fix this
Alias: MESH = http://purl.bioontology.org/ontology/MESH/

Instance: EliLillyAndCompany
InstanceOf: Organization
Title: "Eli Lilly and Company"
* identifier[0].value = "Eli Lilly and Company"
* identifier[0].use = #official
* type = #crs

Instance: SamGetWell
InstanceOf: Practitioner
Title: "Samuel Home, M.D."
* identifier[0].value = "ABC123"
* identifier[0].type = #UPIN
* identifier[0].use = #official
* active = true
* name[0].use = #usual
* name[0].family = "Home"
* name[0].given = "Samuel"
* name[0].prefix = "Dr"
* name[0].suffix[0] = "M.D."
* gender = #male
* telecom.value = "555-123-5467"
* telecom.system = #phone
* telecom.use = #work

Instance: H2Q-MC-LZZT-ResearchStudy
InstanceOf: ResearchStudy
Title: "H2Q-MC-LZZT Research Study"
Usage: #example
* identifier[0].use = #usual
* identifier[0].value = "H2Q-MC-LZZT" 
* identifier[1].use = #official
* identifier[1].value = "NCTA12313212"
* identifier[1].system = "https://clinicaltrials.gov/show/"
* identifier[2].use = #secondary
* identifier[2].type = #PLAC
* identifier[2].value = "NCTA12313212"
* title = "Safety and Efficacy of the Xanomeline Transdermal Therapeutic System (TTS) in Patients with Mild to Moderate Alzheimer’s Disease"
* protocol[PlanDefinition] = Reference(LZZT-Study-Definition)
* status = #completed
* primaryPurposeType = #treatment
* phase = #phase-3
* category[0] = NCIT#C98388 "Interventional Study"
* category[1] = NCIT#C15417 "Randomized Clinical Trial"
* category[2] = NCIT#C15228 "Double Blind Study"
* category[3] = NCIT#C49648 "Placebo Control"
* category[4] = NCIT#C82639 "Parallel Study"
* focus[0] = NCIT#C152926 "Xanomeline"
* focus[1] = NCIT#C149996 "Transdermal Patch Dosage Form"
* condition[0] = SCT#26929004 "Alzheimer's Disease (Disorder)"
* condition[1] = ICD10#G30 "Alzheimer's disease"
* condition[2] = MEDDRA#10001896 "Alzheimer's disease"
// TODO: Contact should include an address and URL
* contact[0].name = "Bob James, Ph.D."
* contact[0].telecom.value = "555-555-5555"
* contact[0].telecom.system = #phone
* contact[0].telecom.use = #work
* relatedArtifact[+].type = #documentation
* relatedArtifact[=].label = "Protocol H2Q-MC-LZZT(c)"
* relatedArtifact[=].url = "https://clinicaltrials.gov/show/NCTA12313212/Lzzt_protocol_redacted.pdf"
* keyword[+].text = "Selective M1 muscarinic agonists"
* keyword[=].coding[+] = MESH#D018721
//* location[+] =   
* description = """# Xanomeline (LY246708)
# Protocol H2Q-MC-LZZT(c) 
Safety and Efficacy of the Xanomeline Transdermal Therapeutic System (TTS) in Patients with Mild to Moderate Alzheimer’s Disease
"""
// TODO: Collaborator also?
* sponsor[Organization] = Reference(EliLillyAndCompany)
* principalInvestigator[Practitioner] = Reference(SamGetWell)
//* reasonStopped = #accrual-goal-met 
* arm[+].name = "Placebo"
* arm[=].type = NCIT#C49648
* arm[=].description = "Placebo arm"
* arm[+].name = "Low-dose xanomeline arm"
* arm[=].type = NCIT#C174266
* arm[=].description = "Low-dose xanomeline arm (50 cm2 TTS Formulation E, 54 mg xanomeline)"
* arm[+].name = "High-dose xanomeline arm"
* arm[=].type = NCIT#C174266
* arm[=].description = "High-dose xanomeline arm (75 cm2 TTS Formulation E, 81 mg xanomeline)"
* objective[+].name = "To determine if there is a statistically significant relationship (overall Type 1 error rate, α=.05) between the change in both ADAS-Cog and CIBIC+ scores, and drug dose (0, 50 cm2 [54 mg], and 75 cm2 [81 mg])."
* objective[=].type = #primary
* objective[+].name = "To document the safety profile of the xanomeline TTS."
* objective[=].type = #primary
* objective[+].name = "To assess the dose-dependent improvement in behavior. Improved scores on the Revised Neuropsychiatric Inventory (NPI-X) will indicate improvement in these areas."
* objective[=].type = #secondary
* objective[+].name = "To assess the dose-dependent improvements in activities of daily living. Improved scores on the Disability Assessment for Dementia (DAD) will indicate improvement in these areas."
* objective[=].type = #secondary
* objective[+].name = "To assess the dose-dependent improvements in an extended assessment of cognition that integrates attention/concentration tasks. The Alzheimer’s Disease Assessment Scale-14 item Cognitive Subscale, hereafter referred to as ADAS-Cog (14), will be used for this assessment."
* objective[=].type = #secondary
* objective[+].name = "To assess the treatment response as a function of Apo E genotype."
* objective[=].type = #secondary

