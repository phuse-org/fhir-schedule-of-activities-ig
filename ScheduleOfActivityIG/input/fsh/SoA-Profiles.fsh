Profile:        SOAPlanDefinition
Parent:         PlanDefinition
Id:             SOA-PlanDefinition
Title:          "SOA PlanDefinition"
Description:    "Schedule of Activities PlanDefinition Extensions"
* extension contains PlannedStudyDay named plannedStudyDay 0..1
* extension[PlannedStudyDay] MS
* extension contains PlannedStudyDayWindow named plannedStudyDayWindow 0..1

Extension: PlannedStudyDay
Id: plannedStudyDay
Title: "Planned Study Day"
Description: "Planned Study Day (Time)"
* value[x] only integer

Extension: PlannedStudyDayWindow
Id: plannedStudyDayWindow
Title: "Planned Study Day Window"
Description: "Planned Study Day Window (Times)"
* value[x] only Range

Profile:        ResearchStudyInclusionExclusion
Parent:         Group
Id:             ResearchStudy-Inclusion-Exclusion
Title:          "Research Study Inclusion Exclusion"
Description:    "Research Study Inclusion Exclusion Criteria"

