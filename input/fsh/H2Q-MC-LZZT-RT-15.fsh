Instance: H2Q-MC-LZZT-Study-RT-15
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "RT-15"
Description: "Planned Visit [RT-15]"
* identifier[+].value = "RT-15"
* extension[plannedStudyDay].valueInteger = 0
* status = #active
* action[+].title = "RT"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-RT"
* action[+].title = "Vital signs/Temperature "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-signs/Temperature"
* action[+].title = "Concomitant Medications "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[+].title = "ADAS-Cog "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ADAS-Cog"
* action[+].title = "CIBIC+ "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-CIBIC+"
* action[+].title = "DAD "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-DAD"
* action[+].title = "NPI-X "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[+].title = "Adverse events "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
