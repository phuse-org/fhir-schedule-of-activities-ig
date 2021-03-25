Instance: H2Q-MC-LZZT-Study-Visit-2
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-2"
Description: "Planned Visit [Visit-2]"
* identifier[+].value = "VISIT-2"
* extension[plannedStudyDay].valueInteger = 0
* status = #active
* action[+].title = "Visit"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit"
* action[+].title = "Vital signs/Temperature "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-signs/Temperature"
* action[+].title = "Ambulatory ECG placed "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Ambulatory-ECG-placed"
* action[+].title = "Adverse events "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
