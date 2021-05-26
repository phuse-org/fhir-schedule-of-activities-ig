Instance: Activity-VitalSignsTemperature
InstanceOf: ActivityDefinition
Description: "Planned Activity [Vital signs/Temperature]"
Usage: #example
Title: "Vital Signs/Temperature"

* status = #active
* identifier[+].value = "F.VS_3"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary

* observationRequirement = Reference(Temperature-Observation-SNOMED)
* observationResultRequirement = Reference(Temperature-Observation-LOINC)

* observationRequirement = Reference(VitalSigns-Observation)
* observationResultRequirement = Reference(VitalSigns-Observation)
* observationRequirement = Reference(VitalSigns-Observation)
* observationResultRequirement = Reference(VitalSigns-Observation)
* observationRequirement = Reference(VitalSigns-Observation)
* observationResultRequirement = Reference(VitalSigns-Observation)