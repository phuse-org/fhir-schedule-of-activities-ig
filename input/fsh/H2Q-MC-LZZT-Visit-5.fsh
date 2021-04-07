Instance: H2Q-MC-LZZT-Study-Visit-5
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-5"
Description: "Planned Visit [Visit-5]"
* identifier[+].value = "VISIT-5"
* extension[plannedStudyDay].valueInteger = 21
* status = #active
* action[+].title = "Visit"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit"
* action[+].title = "Vital signs/Temperature "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-signs/Temperature"
* action[+].title = "ECG "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ECG"
* action[+].title = "Concomitant Medications "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[+].title = "Laboratory (Chem/Hemat)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-(Chem/Hemat)"
* action[+].title = "Plasma Specimen "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Plasma-Specimen"
* action[+].title = "Study drug record "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
* action[+].title = "NPI-X "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[+].title = "Adverse events "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
