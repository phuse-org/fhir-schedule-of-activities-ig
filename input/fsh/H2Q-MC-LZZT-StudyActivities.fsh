Instance: H2Q-MC-LZZT-DAD
InstanceOf: ActivityDefinition
Description: "Planned Activity [DAD]"
Usage: #example
Title: "DAD"
* status = #active
* identifier[+].value = "F.DAD"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(DAD-Observations)
* observationResultRequirement = Reference(DAD-Observations)

Instance: H2Q-MC-LZZT-Medications-returned
InstanceOf: ActivityDefinition
Description: "Planned Activity [Medications returned]"
Usage: #example
Title: "Medications returned"
* status = #active
* observationRequirement = Reference(Medications-returned-Observations)
* observationResultRequirement = Reference(Medications-returned-Observations)

Instance: H2Q-MC-LZZT-Medications-dispensed
InstanceOf: ActivityDefinition
Description: "Planned Activity [Medications dispensed]"
Usage: #example
Title: "Medications dispensed"
* status = #active
* identifier[+].value = "F.EX_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(Medications-dispensed-Observations)
* observationResultRequirement = Reference(Medications-dispensed-Observations)

Instance: H2Q-MC-LZZT-Ambulatory-ECG-removed
InstanceOf: ActivityDefinition
Description: "Planned Activity [Ambulatory ECG removed]"
Usage: #example
Title: "Ambulatory ECG removed"
* status = #active
* identifier[+].value = "F.PR_ECG_2"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(Ambulatory-ECG-removed-Observations)
* observationResultRequirement = Reference(Ambulatory-ECG-removed-Observations)


Instance: H2Q-MC-LZZT-Physical-examination
InstanceOf: ActivityDefinition
Description: "Planned Activity [Physical examination]"
Usage: #example
Title: "Physical examination"
* status = #active
* observationRequirement = Reference(Physical-examination-Observations)
* observationResultRequirement = Reference(Physical-examination-Observations)

Instance: H2Q-MC-LZZT-Adverse-events
InstanceOf: ActivityDefinition
Description: "Planned Activity [Adverse events]"
Usage: #example
Title: "Adverse events"
* status = #active
* identifier[+].value = "F.AE_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(Adverse-events-Observations)
* observationResultRequirement = Reference(Adverse-events-Observations)

Instance: H2Q-MC-LZZT-Patient-number-assigned
InstanceOf: ActivityDefinition
Description: "Planned Activity [Patient number assigned]"
Usage: #example
Title: "Patient number assigned"
* status = #active
* identifier[+].value = "F.DM_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(Patient-number-assigned-Observations)
* observationResultRequirement = Reference(Patient-number-assigned-Observations)

Instance: H2Q-MC-LZZT-Vital-signs-Temperature
InstanceOf: ActivityDefinition
Description: "Planned Activity [Vital signs/Temperature]"
Usage: #example
Title: "Vital signs/Temperature"
* status = #active
* identifier[+].value = "F.VS_3"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* code.coding[+].code = #56342008
* code.coding[=].system = "http://snomed.info/sct"
* code.coding[=].display = "Temperature taking (procedure)"
* observationRequirement = Reference(Vital-signs-Temperature-Observations)
* observationResultRequirement = Reference(Vital-signs-Temperature-Observations)

Instance: H2Q-MC-LZZT-Medical-History
InstanceOf: ActivityDefinition
Description: "Planned Activity [Medical History]"
Usage: #example
Title: "Medical History"
* status = #active
* identifier[+].value = "F.MH_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(Medical-History-Observations)
* observationResultRequirement = Reference(Medical-History-Observations)

Instance: H2Q-MC-LZZT-Chest-x-ray
InstanceOf: ActivityDefinition
Description: "Planned Activity [Chest x-ray]"
Usage: #example
Title: "Chest x-ray"
* status = #active
* identifier[+].value = "F.PR_CHESTXRAY"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(Chest-x-ray-Observations)
* observationResultRequirement = Reference(Chest-x-ray-Observations)

Instance: H2Q-MC-LZZT-Placebo-TTS-test
InstanceOf: ActivityDefinition
Description: "Planned Activity [Placebo TTS test]"
Usage: #example
Title: "Placebo TTS test"
* status = #active
* observationRequirement = Reference(Placebo-TTS-test-Observations)
* observationResultRequirement = Reference(Placebo-TTS-test-Observations)

Instance: H2Q-MC-LZZT-CIBIC
InstanceOf: ActivityDefinition
Description: "Planned Activity [CIBIC+]"
Usage: #example
Title: "CIBIC+"
* status = #active
* identifier[+].value = "F.CIBC+"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(CIBIC-Observations)
* observationResultRequirement = Reference(CIBIC-Observations)


Instance: H2Q-MC-LZZT-TTS-Acceptability-Survey
InstanceOf: ActivityDefinition
Description: "Planned Activity [TTS Acceptability Survey]"
Usage: #example
Title: "TTS Acceptability Survey"
* status = #active
* identifier[+].value = "F.TTSACC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary
* observationRequirement = Reference(TTS-Acceptability-Survey-Observations)
* observationResultRequirement = Reference(TTS-Acceptability-Survey-Observations)

Instance: H2Q-MC-LZZT-Visit-Date
InstanceOf: ActivityDefinition
Description: "Planned Activity [Record Visit Date]"
Usage: #example
Title: "Visit Date"
* status = #active
* identifier[+].value = "F.DOV"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* identifier[=].use = #secondary


Instance: H2Q-MC-LZZT-Plasma-Specimen
InstanceOf: ActivityDefinition
Description: "Planned Activity [Plasma Specimen]"
Usage: #example
Title: "Plasma Specimen"
* status = #active
* observationRequirement = Reference(Plasma-Specimen-Observations)
* observationResultRequirement = Reference(Plasma-Specimen-Observations)

Instance: H2Q-MC-LZZT-Habits-Alcohol
InstanceOf: ActivityDefinition
Description: "Planned Activity [Habits - Alcohol]"
Usage: #example
Title: "Habits - Alcohol"
* status = #active
* identifier[+].value = "F.SU_ALCOHOL"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(Habits-Observations-Alcohol)
* observationResultRequirement = Reference(Habits-Observations-Alcohol)

Instance: H2Q-MC-LZZT-Habits-Caffeine
InstanceOf: ActivityDefinition
Description: "Planned Activity [Habits - Caffeine]"
Usage: #example
Title: "Habits - Caffeine"
* status = #active
* identifier[+].value = "F.SU_CAFFEINE"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(Habits-Observations-Caffeine)
* observationResultRequirement = Reference(Habits-Observations-Caffeine)

Instance: H2Q-MC-LZZT-Habits-Smoking
InstanceOf: ActivityDefinition
Description: "Planned Activity [Habits - Smoking]"
Usage: #example
Title: "Habits - Smoking"
* status = #active
* identifier[+].value = "F.SU_SMOKING"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(Habits-Observations-Smoking)
* observationResultRequirement = Reference(Habits-Observations-Smoking)

Instance: H2Q-MC-LZZT-Hemoglobin-A1C
InstanceOf: ActivityDefinition
Description: "Planned Activity [Hemoglobin A1C]"
Usage: #example
Title: "Hemoglobin A1C"
* status = #active
// TODO: separate out
* observationRequirement = Reference(Hemoglobin-A1C-Observations)
* observationResultRequirement = Reference(Hemoglobin-A1C-Observations)

Instance: H2Q-MC-LZZT-Study-drug-record
InstanceOf: ActivityDefinition
Description: "Planned Activity [Study drug record]"
Usage: #example
Title: "Study drug record"
* status = #active
* identifier[+].value = "F.EX_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(Study-drug-record-Observations)
* observationResultRequirement = Reference(Study-drug-record-Observations)

Instance: H2Q-MC-LZZT-ADAS-Cog
InstanceOf: ActivityDefinition
Description: "Planned Activity [ADAS-Cog]"
Usage: #example
Title: "ADAS-Cog"
* status = #active
* identifier[+].value = "F.ADAS-COG"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(ADAS-Cog-Observations)
* observationResultRequirement = Reference(ADAS-Cog-Observations)

Instance: H2Q-MC-LZZT-CT-Scan
InstanceOf: ActivityDefinition
Description: "Planned Activity [CT Scan]"
Usage: #example
Title: "CT Scan"
* status = #active
* identifier[+].value = "F.PR_CTSCAN"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(CT-Scan-Observations)
* observationResultRequirement = Reference(CT-Scan-Observations)

Instance: H2Q-MC-LZZT-Hachinski-4
InstanceOf: ActivityDefinition
Description: "Planned Activity [Hachinski 4]"
Usage: #example
Title: "Hachinski 4"
* status = #active
* identifier[+].value = "F.MHIS-NACC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(Hachinski-4-Observations)
* observationResultRequirement = Reference(Hachinski-4-Observations)

Instance: H2Q-MC-LZZT-Patient-randomized
InstanceOf: ActivityDefinition
Description: "Planned Activity [Patient randomized]"
Usage: #example
Title: "Patient randomized"
* status = #active
* observationRequirement = Reference(Patient-randomized-Observations)
* observationResultRequirement = Reference(Patient-randomized-Observations)

Instance: H2Q-MC-LZZT-Ambulatory-ECG-placed
InstanceOf: ActivityDefinition
Description: "Planned Activity [Ambulatory ECG placed]"
Usage: #example
Title: "Ambulatory ECG placed"
* status = #active
* identifier[+].value = "F.PR_ECG_2"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(Ambulatory-ECG-placed-Observations)
* observationResultRequirement = Reference(Ambulatory-ECG-placed-Observations)

Instance: H2Q-MC-LZZT-Informed-Consent
InstanceOf: ActivityDefinition
Description: "Planned Activity [Informed Consent]"
Usage: #example
Title: "Informed Consent"
* status = #active
* identifier[+].value = "F.DS_IC"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(Informed-Consent-Observations)
* observationResultRequirement = Reference(Informed-Consent-Observations)

Instance: H2Q-MC-LZZT-MMSE-10-23
InstanceOf: ActivityDefinition
Description: "Planned Activity [MMSE 10-23]"
Usage: #example
Title: "MMSE 10-23"
* status = #active
* identifier[+].value = "F.MMSE"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(MMSE-10-23-Observations)
* observationResultRequirement = Reference(MMSE-10-23-Observations)

Instance: H2Q-MC-LZZT-Concomitant-Medications
InstanceOf: ActivityDefinition
Description: "Planned Activity [Concomitant Medications]"
Usage: #example
Title: "Concomitant Medications"
* status = #active
* identifier[+].value = "F.CM_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(Concomitant-Medications-Observations)
* observationResultRequirement = Reference(Concomitant-Medications-Observations)

Instance: H2Q-MC-LZZT-ECG
InstanceOf: ActivityDefinition
Description: "Planned Activity [ECG]"
Usage: #example
Title: "ECG"
* status = #active
* identifier[+].value = "F.ECG_1"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(ECG-Observations)
* observationResultRequirement = Reference(ECG-Observations)

Instance: H2Q-MC-LZZT-NPI-X
InstanceOf: ActivityDefinition
Description: "Planned Activity [NPI-X]"
Usage: #example
Title: "NPI-X"
* status = #active
* identifier[+].value = "F.NPI-X"
* identifier[=].system = "http://www.cdisc.org/ns/odm/v1.3/FormDef#"
* identifier[=].type.coding[0].system = "http://www.cdisc.org/ns/odm/v1.3#"
* identifier[=].type.coding[0].display = "OID"
* observationRequirement = Reference(NPI-X-Observations)
* observationResultRequirement = Reference(NPI-X-Observations)

