Profile:        SOAVisitPlanDefinition
Parent:         PlanDefinition
Id:             SOA-visit-plan-definition
Title:          "SOA Visit Plan Defintion"
Description:    "A profile on the plan definition resource to define the planned events for a visit."
* action.definitionCanonical = Canonical(SOAPlannedVisitDefinition|1.0.1)
* extension contains PlannedStudyDay named plannedStudyDay 0..1 
* extension contains PlannedStudyWindow named plannedStudyWindow 0..1 
* extension contains StudyDesignOID named studyEventOID 0..1 