// Hematology (CBC) panel — demonstrates ObservationDefinition.hasMember.
// Analytes are a representative subset; more are added during catalog population.

Instance: H2Q-MC-LZZT-Hematology-WBC-Obs
InstanceOf: ObservationDefinition
Usage: #definition
Title: "Leukocytes (WBC) - Observation"
Description: "White blood cell count, an analyte of the Hematology panel."
* insert VitalSignObservation(6690-2, [[Leukocytes]], 10*3/uL)

Instance: H2Q-MC-LZZT-Hematology-HGB-Obs
InstanceOf: ObservationDefinition
Usage: #definition
Title: "Hemoglobin - Observation"
Description: "Hemoglobin mass concentration, an analyte of the Hematology panel."
* insert VitalSignObservation(718-7, [[Hemoglobin]], g/dL)

Instance: H2Q-MC-LZZT-Hematology-PLT-Obs
InstanceOf: ObservationDefinition
Usage: #definition
Title: "Platelets - Observation"
Description: "Platelet count, an analyte of the Hematology panel."
* insert VitalSignObservation(777-3, [[Platelets]], 10*3/uL)

Instance: H2Q-MC-LZZT-Hematology-Panel-Obs
InstanceOf: ObservationDefinition
Usage: #definition
Title: "Hematology (CBC) panel - Observation"
Description: "Complete blood count panel; groups its analyte ObservationDefinitions."
* insert PanelObservation(58410-2, [[CBC panel]])
* hasMember[+] = Reference(H2Q-MC-LZZT-Hematology-WBC-Obs)
* hasMember[+] = Reference(H2Q-MC-LZZT-Hematology-HGB-Obs)
* hasMember[+] = Reference(H2Q-MC-LZZT-Hematology-PLT-Obs)
