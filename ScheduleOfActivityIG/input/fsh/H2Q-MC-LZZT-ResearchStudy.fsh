Alias: NCIT = http://ncimeta.nci.nih.gov
Alias: SCT = http://snomed.info/sct
Alias: PUBMED = https://pubmed.ncbi.nlm.nih.gov
Alias: PUBCHEM = https://pubchem.ncbi.nlm.nih.gov


Instance: EliLillyAndCompany
InstanceOf: Organization
Title: "Eli Lilly and Company"
* identifier[0].value = "Eli Lilly and Company"
* identifier[0].use = #official
* contact[+].purpose = #ADMIN
* contact[=].telecom[+].system = #url
* contact[=].telecom[=].value = "https://www.lilly.com"
* type = #crs


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
// TODO: Update this when applicable
* identifier[2].value = "NCTA12313212"
* identifier[3].type = #PUBCHEM
* identifier[3].value = "60809"
* title = "Safety and Efficacy of the Xanomeline Transdermal Therapeutic System (TTS) in Patients with Mild to Moderate Alzheimer’s Disease"
* protocol[PlanDefinition] = Reference(H2Q-MC-LZZT-ProtocolDesign)
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
* focus[2] = PUBMED#9109749 "Effects of xanomeline, a selective muscarinic receptor agonist, on cognitive function and behavioral symptoms in Alzheimer disease"
* condition[0] = SCT#26929004 "Alzheimer's Disease (Disorder)"
// TODO: Contact should include an address and URL
* contact[0].name = "Bob James, Ph.D."
* contact[0].telecom.value = "555-555-5555"
* contact[0].telecom.system = #phone
* contact[0].telecom.use = #work
* relatedArtifact[0].type = #documentation
* relatedArtifact[0].label = "Arch Neurol.1997;54(4):465-473"
* relatedArtifact[0].display = "Arch Neurol.1997;54(4):465-473"
* relatedArtifact[0].citation = "Bodick NC, Offen WW, Levey AI, et al. Effects of xanomeline, a selective muscarinic receptor agonist, on cognitive function and behavioral symptoms in Alzheimer disease. Arch Neurol. 1997;54(4):465-473. doi:10.1001/archneur.1997.00550160091022"
// * keyword[0].
// * location[0]
* description = """
# Primary Objectives
The primary objectives of this study are:
* To determine if there is a statistically significant relationship (overall Type 1 error rate, α=.05) between the change in both ADAS-Cog (see Attachment LZZT.2) and CIBIC+ (see Attachment LZZT.3) scores, and drug dose (0, 50 cm2 [54 mg], and 75 cm2 [81 mg]).
* To document the safety profile of the xanomeline TTS.
"""
// * inclusion/exclusion criteria
* enrollment = Reference(H2Q-MC-LZZT-InclusionExclusion)
* sponsor[Organization] = Reference(EliLillyAndCompany)
