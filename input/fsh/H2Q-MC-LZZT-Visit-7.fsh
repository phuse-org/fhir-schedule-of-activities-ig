Instance: H2Q-MC-LZZT-Study-Visit-7
InstanceOf: SOAPlanDefinition
Usage: #example
Title: "Visit-7"
Description: "Planned Visit [Visit-7]"
* identifier[+].value = "VISIT-7"
* extension[plannedStudyDay].valueInteger = 42
* identifier[+].value = "SE.TRT_VISIT_04"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/StudyDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* status = #active
* action[+].title = "Record Visit Date"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Visit-Date"
* action[+].title = "Vital signs/Temperature "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Vital-signs/Temperature"
* action[+].title = "ECG "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-ECG"
* action[+].title = "Concomitant Medications "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Concomitant-Medications"
* action[+].title = "Laboratory (Chem/Hemat)"
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Laboratory-(Chem/Hemat)"
* action[+].title = "Plasma Specimen (Xanomeline) "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Plasma-Specimen"
* action[+].title = "Study drug record: Medications Dispensed/Returned "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Study-drug-record"
* action[+].title = "NPI-X "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-NPI-X"
* action[+].title = "Adverse events "
* action[=].definitionUri = "ActivityDefinition/H2Q-MC-LZZT-Adverse-events"
