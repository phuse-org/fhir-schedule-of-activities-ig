Instance: H2Q-MC-LZZT-ProtocolDesign
InstanceOf: SOAPlanDefinition
Description: "H2Q-MC-LZZT-Protocol Schedule of Activities"
Usage: #example
* status = #active
* version = "LZZT_1"
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-1"
* action[=].title = "Visit-1"
* action[=].description = "Planned Visit [Visit-1]"
* action[=].id = "H2Q-MC-LZZT-Study-Visit-1"
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-2"
* action[=].title = "Visit-2"
* action[=].description = "Planned Visit [Visit-2]"
* action[=].id = "H2Q-MC-LZZT-Study-Visit-2"
* action[=].relatedAction[+].actionId = "H2Q-MC-LZZT-Study-Visit-1"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 14
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-3"
* action[=].title = "Visit-3"
* action[=].description = "Planned Visit [Visit-3]"
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-4"
* action[=].title = "Visit-4"
* action[=].description = "Planned Visit [Visit-4]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-5"
* action[=].title = "Visit-5"
* action[=].description = "Planned Visit [Visit-5]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-6"
* action[=].title = "Visit-6"
* action[=].description = "Planned Visit [Visit-6]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-7"
* action[=].title = "Visit-7"
* action[=].description = "Planned Visit [Visit-7]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-8"
* action[=].title = "Visit-8"
* action[=].description = "Planned Visit [Visit-8]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-9"
* action[=].title = "Visit-9"
* action[=].description = "Planned Visit [Visit-9]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-10"
* action[=].title = "Visit-10"
* action[=].description = "Planned Visit [Visit-10]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-11"
* action[=].title = "Visit-11"
* action[=].description = "Planned Visit [Visit-11]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-12"
* action[=].title = "Visit-12"
* action[=].description = "Planned Visit [Visit-12]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-13"
* action[=].title = "Visit-13"
* action[=].description = "Planned Visit [Visit-13]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-ET-14"
* action[=].title = "ET-14"
* action[=].description = "Planned Visit [ET-14]"

* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-RT-15"
* action[=].title = "RT-15"
* action[=].description = "Planned Visit [RT-15]"

