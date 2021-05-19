
Instance: ObservationDefinition-Supine-Systolic
InstanceOf: ObservationDefinition
Title: "Supine Systolic BP"
* status = #active
* code = #8641-6

Instance: ObservationDefinition-Supine-Diastolic
InstanceOf: ObservationDefinition
Title: "Supine Diastolic BP"
* status = #active
* code = #8455-8

Instance: ObservationDefinition-Supine-HeartRate
InstanceOf: ObservationDefinition
Title: "Supine HR"
* status = #active
* code = #68999-2

Instance: Supine-Vitals
InstanceOf: ActivityDefinition
Title: "Supine Vitals"
* status = #active
* observationRequirement[+] = Reference(ObservationDefinition-Supine-Systolic)
* observationRequirement[+] = Reference(ObservationDefinition-Supine-Diastolic)
* observationRequirement[+] = Reference(ObservationDefinition-Supine-HeartRate)

Instance: ObservationDefinition-Standing-Systolic
InstanceOf: ObservationDefinition
Title: "Standing Systolic BP"
* status = #active
* code = #8460-8

Instance: ObservationDefinition-Standing-Diastolic
InstanceOf: ObservationDefinition
Title: "Standing Diastolic BP"
* status = #active
* code = #8454-1

Instance: ObservationDefinition-Standing-HeartRate
InstanceOf: ObservationDefinition
Title: "Standing HR"
* status = #active
* code = #69001-6

Instance: Standing-Vitals
InstanceOf: ActivityDefinition
Title: "Standing Vitals"
* status = #active
* observationRequirement[+] = Reference(ObservationDefinition-Standing-Systolic)
* observationRequirement[+] = Reference(ObservationDefinition-Standing-Diastolic)
* observationRequirement[+] = Reference(ObservationDefinition-Standing-HeartRate)

Instance: H2Q-MC-LZZT-Vitalsigns-Screening
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Vital Signs"
Description: "Vital signs blood pressure and heart rate"
* status = #active
* identifier[+].value = "VitalSigns"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "F.VS_4"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].type.text = "OID"
* identifier[=].use = #secondary
* action[+].definitionUri = "ActivityDefinition/Supine-Vitals"
* action[=].title = "Supine Vitals"
* action[=].id = "supine"
* action[+].definitionUri = "ActivityDefinition/Standing-Vitals"
* action[=].id = "standing1"
* action[=].title = "3 min standing"
* action[=].relatedAction.targetId = "supine"
* action[=].relatedAction.relationship = #after
* action[=].relatedAction.offsetDuration.value = 3
* action[=].relatedAction.offsetDuration.unit = #min
* action[+].definitionUri = "ActivityDefinition/Standing-Vitals"
* action[=].id = "standing2"
* action[=].relatedAction.targetId = "standing1"
* action[=].relatedAction.relationship = #after
* action[=].relatedAction.offsetDuration.value = 2
* action[=].relatedAction.offsetDuration.unit = #min
