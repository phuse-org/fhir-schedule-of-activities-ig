Instance: SYSBP
InstanceOf: ActivityDefinition
Title: "Systolic Blood Pressure"
Description: "Taking Systolic BP"
Usage: #example
* status = #active

Instance: DIABP
InstanceOf: ActivityDefinition
Title: "Diastolic Blood Pressure"
Description: "Taking Diastolic BP"
Usage: #example
* status = #active

Instance: PULSE
InstanceOf: ActivityDefinition
Title: "Pulse"
Description: "Taking Pulse"
Usage: #example
* status = #active


Instance: VitalSigns
InstanceOf: PlanDefinition
Title: "Vital Signs"
Description: "Vital Signs Assessment"
Usage: #example
* status = #active
* action[+].title = "Blood Pressure"
* action[=].action[+].title = "Systolic Blood Pressure"
* action[=].action[=].definitionUri = "ActivityDefinition/SYSBP"
* action[=].action[+].title = "Diastolic Blood Pressure"
* action[=].action[=].definitionUri = "ActivityDefinition/DIABP"
* action[+].title = "Pulse"
* action[=].action.title = "Pulse Rate"
* action[=].action.definitionUri = "ActivityDefinition/PULSE"



