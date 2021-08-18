Instance: H2Q-MC-LZZT-Bundle-1
InstanceOf: Bundle
Usage: #example
Title: "H2Q-MC-LZZT Bundle 1"
Description: "First Deliverable for the PHUSE Project"
* type = #transaction
* entry[+].resource = SamGetWell
* entry[=].fullUrl = "Practioner/SamGetWell"
* entry[=].request.method = #POST
* entry[=].request.url = "SamGetWell"
* entry[+].resource = EliLillyAndCompany
* entry[=].fullUrl = "Organization/EliLillyAndCompany"
* entry[=].request.method = #POST
* entry[=].request.url = "Organization"
* entry[+].resource = H2Q-MC-LZZT-ProtocolDesign
* entry[=].fullUrl = "SOAPlanDefinition/H2Q-MC-LZZT-ProtocolDesign"
* entry[=].request.method = #POST
* entry[=].request.url = "PlanDefinition"
* entry[+].resource = H2Q-MC-LZZT-ResearchStudy
* entry[=].fullUrl = "ResearchStudy/H2Q-MC-LZZT-ResearchStudy"
* entry[=].request.method = #POST
* entry[=].request.url = "ResearchStudy"

