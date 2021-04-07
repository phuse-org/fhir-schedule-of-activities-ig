Alias: NCIT = http://ncimeta.nci.nih.gov

Profile:        SOAStudyActivityDefinition
Parent:         ActivityDefinition
Id:             SOA-planned-study-activity-definition
Title:          "SOA Planned Study Activity Definition"
Description:    "Planned Study Activity Definition that allows tagging of milestones"
* extension contains SOAStudyMilestone named studyMilestone 0..* MS


ValueSet: StudyMilestoneValueset
Id: SOA-study-activity-milestone-valueset
Title: "Study Milestone"
* include codes from system NCIT where concept is-a #C114118

Extension: SOAStudyMilestone
Id: soa-study-activity-milestne
Title: "Study Milestone"
Description: "Categorization of Study Milestone"
* value[x] only CodeableConcept
* valueCodeableConcept from StudyMilestoneValueset

Instance: SubjectRandomizationDate
InstanceOf: SOAStudyActivityDefinition
Title: "Subject Randomization"
Usage: #example
* status = #active
* extension[studyMilestone].valueCodeableConcept = NCIT#C114209 "Subject is Randomized"
* extension[studyMilestone][1].valueCodeableConcept = NCIT#C161417 "Subject Entered Into Trial"

