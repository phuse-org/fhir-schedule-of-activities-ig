Instance: H2Q-MC-LZZT-Study-Visit-3
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-3"
Description: "Planned Visit [Visit-3]"
* identifier[+].value = "VISIT-3"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "SE.RANDOMIZATION_VISIT"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* extension[plannedStudyDay].valueInteger = 0
* status = #active
* action[+].title = "Record Visit Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Patient randomized "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Patient-randomized"
* action[+].title = "Vital signs/Temperature "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-signs/Temperature"
* action[+].title = "Ambulatory ECG removed "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Ambulatory-ECG-removed"
* action[+].title = "Concomitant Medications "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[+].title = "Laboratory (Urinalysis) "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-Urinalysis"
* action[+].title = "Plasma Specimen "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Plasma-Specimen"
* action[+].title = "Study drug record "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
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
