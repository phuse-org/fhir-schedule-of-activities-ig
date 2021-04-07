Profile:        SOAUnPlannedVisitDefinition
Parent:         ActivityDefinition
Id:             SOA-unplanned-visit-definition
Title:          "SOA Unplanned Visit Definition"
Description:    "An example of a unplanned visit definition for the study."
* extension contains UnPlannedStudyWindow named unplannedStudyWindow 0..1
* extension contains StudyDesignOID named studyEventOID 0..1
* extension[StudyDesignOID] MS

Extension: UnPlannedStudyWindow
Id: unplanned-visit-study-window
Title: "Unplanned Study Visit Range"
Description: "Unplanned Study Visit Range [Day.min() to Day.max() of SoA]"
* value[x] only Range

Extension: StudyDesignOID
Id: study-event-oid
Title: "Study Event OID"
Description: "OID for Study Event in Design"
* value[x] only string
