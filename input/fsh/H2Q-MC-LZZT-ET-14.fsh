Instance: H2Q-MC-LZZT-Study-ET-14
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "ET-14"
Description: "Planned Visit [ET-14]"
* identifier[+].value = "ET-14"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* identifier[+].value = "SE.EARLY_TERM_VISIT"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* extension[plannedStudyDay].valueInteger = 0
* status = #active
* action[+].title = "Record Visit Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "ET"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ET"
* action[+].title = "Physical examination "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Physical-examination"
* action[+].title = "Vital signs/Temperature "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-signs/Temperature"
* action[+].title = "ECG "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ECG"
* action[+].title = "Concomitant Medications "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[+].title = "Laboratory (Chem/Hemat)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-(Chem/Hemat)"
* action[+].title = "Laboratory (Urinalysis) "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-(Urinalysis)"
* action[+].title = "Study drug record: Medications Dispensed/Returned "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
* action[+].title = "TTS Acceptability Survey"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-TTS-Acceptability-Survey"
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
