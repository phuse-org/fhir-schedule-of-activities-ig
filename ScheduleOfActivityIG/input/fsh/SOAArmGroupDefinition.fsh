Profile:        SOAArmGroupDefinition
Parent:         Group
Id:             SOA-armgroup-definition
Title:          "SOA Arm Defintion"
Description: "Extension to define a Arm Group for a Research Study"
//* researchStudy only Reference(researchStudy)
* extension contains ArmResearchStudy named researchStudy 1..1 MS
* extension contains ArmStatus named status 1..1 MS


ValueSet: ArmStatus
Id: soa-arm-status
Title: "Arm Status Value Set"
Description: "Set of permitted values for Arm status"



Extension: ArmResearchStudy
Id: SOA-arm-ResearchStudy
Title: "ResearchStudy Arm"
* value[x] 1..1
* value[x] only Reference(ResearchStudy)


Instance: LZZT-Research-Study
InstanceOf: ResearchStudy
Title: "H2Q-MC-LZZT"
Description: "Study"
* status = #active


Instance: StudyArmStandardOfCare
InstanceOf: SOAArmGroupDefinition
Title: "Arm: Standard of Care"
Usage: #example
* type = #person
* actual = true
* extension[researchStudy].valueReference = Reference(LZZT-Research-Study)



