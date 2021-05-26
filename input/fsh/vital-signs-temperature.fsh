Instance: VitalSignsTiming
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Vitalsigns-HeartRate-Blood-Pressure"
Description: "Vital signs blood pressure and heart rate (repeated)"
* identifier[+].value = "VitalSignsHRBP"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "F.VS_4"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].type.text = "OID"
* identifier[=].use = #secondary
* status = #active
* version = "V1 - Amendment X"

// SU (5 mins)
* action[+].title = "SUPINE-Timing-Delay-5"
* action[=].timingDuration = #5min

* action[+].title = "Vital Signs"
* action[=].definitionUri = "ActivityDefinition/VitalSigns"
* action[=].relatedAction.actionId = "SUPINE-Timing-Delay-5"
* action[=].relatedAction.relationship = #after

// ST (1 mins)
* action[+].title = "STANDING-Timing-Delay-1"
* action[=].timingDuration = #1min
* action[=].relatedAction.actionId = "SUPINE-Timing-Delay-5"
* action[=].relatedAction.relationship = #after

* action[+].title = "Vital Signs"
* action[=].definitionUri = "ActivityDefinition/VitalSigns"
* action[=].relatedAction.actionId = "STANDING-Timing-Delay-1"
* action[=].relatedAction.relationship = #after

// ST (3 mins)
* action[+].title = "STANDING-Timing-Delay-3"
* action[=].timingDuration = #3min
* action[=].relatedAction.actionId = "SUPINE-Timing-Delay-1"
* action[=].relatedAction.relationship = #after

* action[+].title = "Vital Signs"
* action[=].definitionUri = "ActivityDefinition/VitalSigns"
* action[=].relatedAction.actionId = "STANDING-Timing-Delay-3"
* action[=].relatedAction.relationship = #after