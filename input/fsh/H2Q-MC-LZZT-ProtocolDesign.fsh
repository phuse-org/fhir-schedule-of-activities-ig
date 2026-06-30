Instance: H2Q-MC-LZZT-ProtocolDesign
InstanceOf: SOAPlanDefinition
Description: "H2Q-MC-LZZT-Protocol Schedule of Activities"
Usage: #example
* status = #active
* version = "LZZT_1"

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-1"
  * title = "Visit-1"
  * description = "Planned Visit [Visit-1]"
  * id = "H2Q-MC-LZZT-Study-Visit-1"

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-2"
  * title = "Visit-2"
  * description = "Planned Visit [Visit-2]"
  * id = "H2Q-MC-LZZT-Study-Visit-2"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 28
    * offsetRange.low.code = #d
    * offsetRange.high.value = 14
    * offsetRange.high.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-3"
  * title = "Visit-3"
  * description = "Planned Visit [Visit-3]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-2"
    * relationship = #after
    * offsetRange.low.value = 1
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-4"
  * title = "Visit-4"
  * description = "Planned Visit [Visit-4]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-3"
    * relationship = #after
    * offsetRange.low.value = 14
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-5"
  * title = "Visit-5"
  * description = "Planned Visit [Visit-5]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-3"
    * relationship = #after
    * offsetRange.low.value = 28
    * offsetRange.low.code = #d

// * action[+].definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-6"
// * action[=].title = "Visit-6"
// * action[=].description = "Planned Visit [Visit-6]"
// * action[=].relatedAction[+].targetId = "H2Q-MC-LZZT-Study-Visit-1"
// * action[=].relatedAction[=].relationship = #after
// * action[=].relatedAction[=].offsetRange.low.value = 42
// * action[=].relatedAction[=].offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-7"
  * title = "Visit-7"
  * description = "Planned Visit [Visit-7]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 42
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-8"
  * title = "Visit-8"
  * description = "Planned Visit [Visit-8]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 56
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-9"
  * title = "Visit-9"
  * description = "Planned Visit [Visit-9]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 84
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-10"
  * title = "Visit-10"
  * description = "Planned Visit [Visit-10]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 112
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-11"
  * title = "Visit-11"
  * description = "Planned Visit [Visit-11]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 140
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-12"
  * title = "Visit-12"
  * description = "Planned Visit [Visit-12]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 168
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-Visit-13"
  * title = "Visit-13"
  * description = "Planned Visit [Visit-13]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 182
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-ET-14"
  * title = "ET-14"
  * description = "Planned Visit [ET-14]"
  * relatedAction[+]
    * targetId = "H2Q-MC-LZZT-Study-Visit-1"
    * relationship = #after
    * offsetRange.low.value = 14
    * offsetRange.low.code = #d

* action[+]
  * definitionUri = "PlanDefinition/H2Q-MC-LZZT-Study-RT-15"
  * title = "RT-15"
  * description = "Planned Visit [RT-15]"

