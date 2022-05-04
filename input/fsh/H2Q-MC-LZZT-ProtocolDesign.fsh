Instance: H2Q-MC-LZZT-ProtocolDesign
InstanceOf: PlanDefinition
Description: "H2Q-MC-LZZT-Protocol Schedule of Activities"
Usage: #example
* status = #active
* version = "LZZT_1"
* identifier[+].value = "H2Q-MC-LZZT-ProtocolDesign-1"
* identifier[=].type = #PLAC
* identifier[=].use = #usual
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-1"
* action[=].title = "Visit-1"
* action[=].description = "Planned Visit [Visit-1]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #before
* action[=].relatedAction[=].offsetRange.low.value = 12
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 15
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-2"
* action[=].title = "Visit-2"
* action[=].description = "Planned Visit [Visit-2]"
* action[=].id = "H2Q-MC-LZZT-Study-Visit-2"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #before
* action[=].relatedAction[=].offsetRange.low.value = 1
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-3"
* action[=].id = "Index-Activity-Event"
* action[=].title = "Visit-3"
* action[=].description = "Planned Visit [Visit-3]"
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-4"
* action[=].title = "Visit-4"
* action[=].description = "Planned Visit [Visit-4]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 12
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 15
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-5"
* action[=].title = "Visit-5"
* action[=].description = "Planned Visit [Visit-5]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 26
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 30
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-6"
* action[=].title = "Visit-6"
* action[=].description = "Planned Visit [Visit-6]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 33
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 37
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-7"
* action[=].title = "Visit-7"
* action[=].description = "Planned Visit [Visit-7]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 40
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 44
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-8"
* action[=].title = "Visit-8"
* action[=].description = "Planned Visit [Visit-8]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 54
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 58
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-8-1"
* action[=].title = "Visit-8.1"
* action[=].description = "Telephone Contact [Post Visit-8]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 68
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 72
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-9"
* action[=].title = "Visit-9"
* action[=].description = "Planned Visit [Visit-9]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 82
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 86
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-9-1"
* action[=].title = "Visit-9.1"
* action[=].description = "Telephone Contact Visit [Post Visit-9]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 96
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 100
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-10"
* action[=].title = "Visit-10"
* action[=].description = "Planned Visit [Visit-10]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 110
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 112
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-10-1"
* action[=].title = "Visit-10.1"
* action[=].description = "Telephone Contact Visit [Post Visit-10]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 124
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 126
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-11"
* action[=].title = "Visit-11"
* action[=].description = "Planned Visit [Visit-11]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 138
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 142
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-11-1"
* action[=].title = "Visit-11.1"
* action[=].description = "Telephone Contact Visit [Post Visit-11]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 152
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 156
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-12"
* action[=].title = "Visit-12"
* action[=].description = "Planned Visit [Visit-12]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 166
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 170
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-13"
* action[=].title = "Visit-13"
* action[=].description = "Planned Visit [Visit-13]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[=].relatedAction[=].offsetRange.low.value = 180
* action[=].relatedAction[=].offsetRange.low.code = #d
* action[=].relatedAction[=].offsetRange.high.value = 184
* action[=].relatedAction[=].offsetRange.high.code = #d
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-ET-14"
* action[=].title = "ET-14"
* action[=].description = "Planned Visit [ET-14]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after
* action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-RT-15"
* action[=].title = "RT-15"
* action[=].description = "Planned Visit [RT-15]"
* action[=].relatedAction[+].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #after

