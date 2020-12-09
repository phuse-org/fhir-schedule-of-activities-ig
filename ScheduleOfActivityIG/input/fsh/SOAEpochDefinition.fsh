Alias: NCIT = http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl

Profile:        SOAEpochDefinition
Parent:         PlanDefinition
Id:             SOA-epoch-definition
Title:          "SOA Epoch Defintion"
Description:    "An example of a study epoch definition for the study."
* ^status = #deprecated
* extension contains SOAEpochType named epochType 0..1 MS

ValueSet:  SOAEpochTypes
Id: soa-epoch-epochtype-value-set
Title: "Epoch Type Value Set"
Description: "Set of permitted values for Epoch"
* NCIT#C125938 "BASELINE"
* NCIT#C101526 "BLINDED TREATMENT"
* NCIT#C16032 "LONG-TERM FOLLOW-UP"
* NCIT#C123453 "INDUCTION TREATMENT"
* NCIT#C123452 "CONTINUATION TREATMENT"
* NCIT#C98779 "RUN-IN"
* NCIT#C48262 "SCREENING"
* NCIT#C101526 "TREATMENT"
* NCIT#C99158 "FOLLOW-UP"
* NCIT#C165873 "OBSERVATION"
* NCIT#C102255 "BLINDED TREATMENT"
* NCIT#C102256 "OPEN LABEL TREATMENT"
* NCIT#C42872 "WASHOUT"

Extension: SOAEpochType
Id: soa-epoch-epochtype
Title: "Epoch Type"
Description: "Categorization of Epoch Type"
* value[x] only CodeableConcept
* valueCodeableConcept from SOAEpochTypes 


Instance: ScreeningEpoch
InstanceOf: SOAEpochDefinition
Title: "Screening Visit"
* status = #active
* extension[SOAEpochType].valueCodeableConcept = NCIT#C48262 "SCREENING"
