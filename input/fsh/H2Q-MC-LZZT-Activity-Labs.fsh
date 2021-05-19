Instance: UrinalysisSample
InstanceOf: SpecimenDefinition
Description: "Urine Sample"
* status = #active
* typeCollected = #UR
* collection = #73416001

Instance: BloodSample
InstanceOf: SpecimenDefinition
Description: "Blood Sample"
* status = #active
* typeCollected = #BLD
* collection = #129300006

Instance: ObservationDefinition-Urinalysis-Color
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #5778-6

Instance: ObservationDefinition-Urinalysis-SpecificGravity
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2965-2

Instance: ObservationDefinition-Urinalysis-pH
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2756-5

Instance: ObservationDefinition-Urinalysis-Protein
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2888-6

Instance: ObservationDefinition-Urinalysis-Ketones
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #33903-6

Instance: ObservationDefinition-Urinalysis-Glucose
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2350-7

Instance: ObservationDefinition-Urinalysis-Bilirubin
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #1977-8

Instance: ObservationDefinition-Urinalysis-Urobilinogen
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #3107-0

Instance: ObservationDefinition-Urinalysis-Blood
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #5794-3

Instance: ObservationDefinition-Urinalysis-Nitrite
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #5802-4

Instance: ObservationDefinition-Urinalysis-Sediment
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #11279-7

Instance: H2Q-MC-LZZT-Laboratory-Urinalysis
InstanceOf: ActivityDefinition
Description: "Planned Activity [Laboratory (Urinalysis)]"
Usage: #example
Title: "Laboratory (Urinalysis)"
* status = #active
* identifier[+].value = "F.LB_URINE"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* specimenRequirement = Reference(UrinalysisSample)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Color)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-SpecificGravity)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-pH)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Protein)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Glucose)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Ketones)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Bilirubin)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Urobilinogen)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Blood)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Nitrite)
* observationRequirement[+] = Reference(ObservationDefinition-Urinalysis-Sediment)


Instance: ObservationDefinition-Hemat-Hemoglobin
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #781-7

Instance: ObservationDefinition-Hemat-Hematocrit
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #4544-3

Instance: ObservationDefinition-Hemat-RBC
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #789-8

Instance: ObservationDefinition-Hemat-MCV
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #787-2

Instance: ObservationDefinition-Hemat-MCH
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #785-6

Instance: ObservationDefinition-Hemat-MCHC 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #786-4

Instance: ObservationDefinition-Hemat-WBC
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #6690-2

Instance: ObservationDefinition-Hemat-Neutrophils-segmented
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #30451-9

Instance: ObservationDefinition-Hemat-Neutrophils-bands
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #26507-4

Instance: ObservationDefinition-Hemat-Lymphocytes
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #26474-7

Instance: ObservationDefinition-Hemat-Monocytes
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #26484-6

Instance: ObservationDefinition-Hemat-Eosinophils
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #26449-9

Instance: ObservationDefinition-Hemat-Basophils
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #26444-0

Instance: ObservationDefinition-Hemat-Platelet
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #26515-7

Instance: ObservationDefinition-Hemat-Cell-morphology
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #6742-1

Instance: ObservationDefinition-Chem-Sodium
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2951-2

Instance: ObservationDefinition-Chem-Potassium
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2823-3

Instance: ObservationDefinition-Chem-Bicarbonate
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #1963-8

Instance: ObservationDefinition-Chem-Chloride
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2075-0

Instance: ObservationDefinition-Chem-Total-bilirubin
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #1975-2

Instance: ObservationDefinition-Chem-ALP 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #6768-6

Instance: ObservationDefinition-Chem-GGT 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2324-2

Instance: ObservationDefinition-Chem-SGPT 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #1742-6

Instance: ObservationDefinition-Chem-SGOT 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #1920-8

Instance: ObservationDefinition-Chem-BUN
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #3094-0

Instance: ObservationDefinition-Chem-Serum-creatinine 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2160-0

Instance: ObservationDefinition-Chem-Uric-acid 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #3084-1

Instance: ObservationDefinition-Chem-Phosphorus
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2777-1

Instance: ObservationDefinition-Chem-Calcium
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #17861-6

Instance: ObservationDefinition-Chem-Glucose-nonfasting 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2345-7

Instance: ObservationDefinition-Chem-Total-protein 
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2885-2

Instance: ObservationDefinition-Chem-Albumin
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #1751-7

Instance: ObservationDefinition-Chem-Cholesterol
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2093-3

Instance: ObservationDefinition-Chem-CK
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2157-6


Instance: ObservationDefinition-Chem-Free-thyroid-index
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #32215-6

Instance: ObservationDefinition-Chem-T3-Uptake
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #3050-2

Instance: ObservationDefinition-Chem-T4
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #3024-7

Instance: ObservationDefinition-Chem-TSH
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #3016-3


Instance: ObservationDefinition-Chem-Folate
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2284-8

Instance: ObservationDefinition-Chem-Vitamin-B12
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #2132-9

Instance: ObservationDefinition-Chem-Syphilis-screening
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #20507-0

Instance: ObservationDefinition-Chem-Hemoglobin-A1C
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #4548-4



Instance: H2Q-MC-LZZT-Laboratory-Hemat
InstanceOf: ActivityDefinition
Description: "Planned Activity [Laboratory (Hema)]"
Usage: #example
Title: "Laboratory (Hema)"
* status = #active
* identifier[+].value = "F.LB_HEM"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* specimenRequirement = Reference(BloodSample)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Hemoglobin)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Hematocrit)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-RBC)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-MCV)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-MCH)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-MCHC)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-WBC)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Neutrophils-segmented)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Neutrophils-bands)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Lymphocytes)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Monocytes)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Eosinophils)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Basophils)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Platelet)
* observationRequirement[+] = Reference(ObservationDefinition-Hemat-Cell-morphology)

Instance: H2Q-MC-LZZT-Laboratory-Chem-Visit1
InstanceOf: ActivityDefinition
Description: "Planned Activity [Laboratory (Chem)] - Screening"
Usage: #example
Title: "Laboratory (Chem)"
* status = #active
* identifier[+].value = "F.LB_CHEM"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* specimenRequirement = Reference(BloodSample)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Sodium)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Potassium)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Bicarbonate)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Chloride)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Total-bilirubin)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-ALP) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-GGT) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-SGPT) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-SGOT) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-BUN)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Serum-creatinine) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Uric-acid) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Phosphorus)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Calcium)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Glucose-nonfasting) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Total-protein) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Albumin)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Cholesterol)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-CK)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Free-thyroid-index)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-T3-Uptake)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-T4)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-TSH)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Folate)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Vitamin-B12)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Syphilis-screening)

Instance: H2Q-MC-LZZT-Laboratory-Chem
InstanceOf: ActivityDefinition
Description: "Planned Activity [Laboratory (Chem)]"
Usage: #example
Title: "Laboratory (Chem)"
* status = #active
* identifier[+].value = "F.LB_HEM"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* specimenRequirement = Reference(BloodSample)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Sodium)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Potassium)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Bicarbonate)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Chloride)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Total-bilirubin)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-ALP) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-GGT) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-SGPT) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-SGOT) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-BUN)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Serum-creatinine) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Uric-acid) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Phosphorus)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Calcium)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Glucose-nonfasting) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Total-protein) 
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Albumin)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Cholesterol)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-CK)

Instance: Apo-E-genotyping-Observations
InstanceOf: ObservationDefinition
Usage: #example
* status = #active
* code = #21619-2


Instance: H2Q-MC-LZZT-Apo-E-genotyping
InstanceOf: ActivityDefinition
Description: "Planned Activity [Apo E genotyping]"
Usage: #example
Title: "Apo E genotyping"
* status = #active
* specimenRequirement = Reference(BloodSample)
* observationRequirement = Reference(Apo-E-genotyping-Observations)
* observationResultRequirement = Reference(Apo-E-genotyping-Observations)

Instance: IDDM-Patients
InstanceOf: Group
Description: "Patients with IDDM"
Usage: #example
Title: "Patients with IDDM"
* type = #person
* actual = false
* name = "IDDM Patients"
* characteristic[0].code.text = "hasCondition"
* characteristic[0].valueCodeableConcept.coding = SCT#46635009 "Diabetes mellitus type 1 (disorder)"
* characteristic[0].exclude = false
// "extension": [
//         {
//           "url": "http://hl7.org/fhir/StructureDefinition/cqf-expression",
//           "valueExpression": {
//             "language": "text/cql",
//             "expression": "exists [Condition: Diabetes]"
//           }
//         }
//       ],

Instance: H2Q-MC-LZZT-Laboratory-Chem-HBA1C
InstanceOf: ActivityDefinition
Description: "HBA1C Test (for IDDM)"
Usage: #example
Title: "HBA1C Test"
* status = #active
* subjectReference = Reference(Group/IDDM-Patients)
* specimenRequirement = Reference(BloodSample)
* observationRequirement[+] = Reference(ObservationDefinition-Chem-Hemoglobin-A1C)
