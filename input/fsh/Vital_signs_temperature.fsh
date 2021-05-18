Instance: H2Q-MC-LZZT-Vitalsigns-Temperature
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "VitalSigns/Temperature"
Description: "Vital signs including temperature, blood pressure and heart rate"
* identifier[+].value = "VitalSigns"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "F.VS_4"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].type.text = "OID"
* identifier[=].use = #secondary
* extension[plannedStudyDay].valueInteger = -14
* status = #active
* action[+].title = "Heart Rate"
* action[=].definitionUri = "ActivityDefinition/Heart_Rate"

* action[+].title = "Temperature"
* action[=].definitionUri = "ActivityDefinition/Temperature"

* action[+].title = "Blood Pressure"
* action[=].definitionUri = "ActivityDefinition/Blood_Pressure"