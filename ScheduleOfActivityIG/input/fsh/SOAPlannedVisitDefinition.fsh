Profile:        SOAPlannedVisitDefinition
Parent:         ActivityDefinition
Id:             SOA-planned-visit-definition
Title:          "SOA Planned Visit Definition"
Description:    "An example of a planned visit definition for the study."
* extension contains PlannedStudyDay named plannedStudyDay 0..1 
* extension contains PlannedStudyWindow named plannedStudyWindow 0..1 
* extension contains StudyDesignOID named studyEventOID 0..1 
* extension[StudyDesignOID] MS
* extension[PlannedStudyDay] MS

Extension: PlannedStudyDay
Id: planned-visit-study-day
Title: "Planned Study Day of Visit"
Description: "Planned Study Day of Visit"
* value[x] only integer

Extension: PlannedStudyWindow
Id: planned-visit-study-windows
Title: "Planned Study Window of Visit"
Description: "Planned Study Window of Visit"
* value[x] only Range

Extension: PlannedStudyOffset
Id: planned-visit-study-offset
Title: "Planned Study Offset of Visit"
Description: "Planned Study Offset of Visit"
* value[x] only Quantity

Extension: StudyDesignOID
Id: planned-visit-study-oid
Title: "Study Event OID"
Description: "OID for Study Event in Design"
* value[x] only string


Instance: Visit1
InstanceOf: SOAPlannedVisitDefinition
Title: "Screening - Day -21"
Usage: #example
* status = #active
* extension[studyEventOID].valueString = "VISIT1"
* extension[plannedStudyDay].valueInteger = -21
* extension[plannedStudyWindow].valueRange.low.value = -22
* extension[plannedStudyWindow].valueRange.high.value = -20

Instance: Visit2
InstanceOf: SOAPlannedVisitDefinition
Title: "Screening - Day -1"
Usage: #example
* status = #active
* extension[studyEventOID].valueString =  "VISIT2"
* extension[plannedStudyDay].valueInteger = -1

Instance: Visit3
InstanceOf: SOAPlannedVisitDefinition
Title: "Treatment - Day 1"
Usage: #example
* status = #active
* extension[plannedStudyDay].valueInteger = 1
* extension[studyEventOID].valueString =  "VISIT3"
