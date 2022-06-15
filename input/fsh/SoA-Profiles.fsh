Extension: RangeTarget
Id: soa-plan-target
Title: "Range Target"
Description: "Provides a fixed target date for a Range."
// Limit the context to Range
* ^context[+].type = #element
* ^context[=].expression = "Range"
* value[x] 1..1
* value[x] only SimpleQuantity

Profile:        SOAPlanDefinition
Parent:         PlanDefinition
Id:             SOA-PlanDefinition
Title:          "SOA PlanDefinition"
Description:    "Schedule of Activities PlanDefinition Extensions"
* action.relatedAction.offsetRange.extension contains RangeTarget named target 0..1

Instance: Visit1PlanDefinition
InstanceOf: SOA-PlanDefinition
Title: "Screening - Day -21"
Description: "Screening Visit - Day -21"
Usage: #example
* status = #active
* action[+].relatedAction[+].offsetRange.low.value = 19
* action[=].relatedAction[=].offsetRange.low.unit = #d
* action[=].relatedAction[=].offsetRange.high.value = 24
* action[=].relatedAction[=].offsetRange.low.unit = #d
* action[=].relatedAction[=].offsetRange.extension[soa-plan-target].valueQuantity.value = 21
* action[=].relatedAction[=].offsetRange.extension[soa-plan-target].valueQuantity.unit = #d
* action[=].relatedAction[=].actionId = "Index-Activity-Event"
* action[=].relatedAction[=].relationship = #before
* action[+].id = "Index-Activity-Event"
