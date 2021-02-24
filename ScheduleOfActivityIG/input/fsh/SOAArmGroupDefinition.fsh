Alias: NCIT = http://ncimeta.nci.nih.gov

Profile:        SOAArmGroupDefinition
Parent:         Group
Id:             SOA-armgroup-definition
Title:          "SOA Arm Definition"
Description: "Extension to define a Arm Group for a Research Study"
//* researchStudy only Reference(researchStudy)
* extension contains ArmResearchStudy named researchStudy 1..1 MS
* extension contains ArmStatus named status 1..1 MS


ValueSet: ArmStatusValueSet
Id: soa-arm-status-valueset
Title: "Arm Status Value Set"
Description: "Set of permitted values for Arm status"
* NCIT#C49069 "Open"
* NCIT#C49070 "Closed"


Extension: ArmStatus
Id: soa-arm-status
Title: "Arm Status"
Description: "Set of permitted values for Arm status"
* value[x] only CodeableConcept
* valueCodeableConcept from ArmStatusValueSet 


Extension: ArmResearchStudy
Id: SOA-arm-ResearchStudy
Title: "ResearchStudy Arm"
Description: "Reference to Study for Study Arm"
* value[x] 1..1
* value[x] only Reference(ResearchStudy)


Instance: LZZT-Research-Study
InstanceOf: ResearchStudy
Title: "H2Q-MC-LZZT"
Description: "Study"
Usage: #example
* status = #active


Instance: StudyArmStandardOfCare
InstanceOf: SOAArmGroupDefinition
Title: "Arm: Standard of Care"
Usage: #example
* type = #person
* actual = true
* extension[researchStudy].valueReference = Reference(LZZT-Research-Study)
* extension[status].valueCodeableConcept = NCIT#C49069 "Open"


