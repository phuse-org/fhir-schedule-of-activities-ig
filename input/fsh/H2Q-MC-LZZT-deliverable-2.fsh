Instance: H2Q-MC-LZZT-Bundle-2
InstanceOf: Bundle
Usage: #example
Title: "H2Q-MC-LZZT Bundle 2"
Description: "First Deliverable for the PHUSE Project"
* type = #transaction
* entry[+].resource = EliLillyAndCompany
* entry[=].request.method = #POST
* entry[=].request.url = "Organization"
* entry[+].resource = SamGetWell
* entry[=].request.method = #POST
* entry[=].request.url = "Practitioner"
* entry[+].resource = LZZT-Study-Definition
* entry[=].request.method = #POST
* entry[=].request.url = "SOAPlanDefinition"
* entry[+].resource = H2Q-MC-LZZT-ResearchStudy
* entry[=].request.method = #POST
* entry[=].request.url = "ResearchStudy"
