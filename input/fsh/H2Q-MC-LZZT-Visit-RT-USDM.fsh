// H2Q-MC-LZZT-Visit-RT-USDM.fsh
// Hand-authored: the Retrieval visit is absent from the USDM source
// (present only as NarrativeContentItem_43). It is modelled here from the
// protocol text (section 3.10.1.1):
//
//   "If possible, patients who have terminated early will be retrieved on
//    the date which would have represented Visit 12 (Week 24). Vital signs,
//    temperature, use of concomitant medications, adverse events, and
//    efficacy measure assessment will be gathered at this visit."
//
// Key design decisions:
//   - soaTimePointSubType = retreatment  (conditional/recovery visit)
//   - soaPlannedTimePoint = 168d from Baseline (E3), same as Week 24 (E12)
//   - soaRepeatAllowed = false
//   - Incoming transition: ET → RT (retreatment edge)
//   - Activities: VS+temp, concomitant meds, adverse events,
//                 ADAS-Cog, CIBIC+, DAD, NPI-X
//   - Uses USDM-derived ActivityDefinition / Questionnaire references

Instance: H2Q-MC-LZZT-RT-USDM
InstanceOf: SOAPlanDefinition
Usage: #definition
Title: "Retrieval Visit (Week 24)"
Description: "Optional retrieval visit for patients who terminated early. Scheduled on the date that would have represented Visit 12 (Week 24, Day 168 from Baseline). Per protocol section 3.10.1.1."
* status = #active
* action[+]
  * id = "RT"
  * title = "Retrieval Visit (Week 24)"
  * extension[soaTimepoint]
    * extension[soaTimePointType].valueString = "interaction"
    * extension[soaTimePointSubType].valueString = "retrieval"
    * extension[soaPlannedTimePoint].valueQuantity
      * value = 168
      * code = #d
      * system = "http://unitsofmeasure.org"
    * extension[soaReferenceTimePoint].valueString = "E3"
    * extension[soaRepeatAllowed].valueBoolean = false

// --- Activity actions for RT ---

// Vital signs and temperature (per protocol: "vital signs, temperature")
* action[+]
  * title = "Vital Signs and Temperature"
  * definitionUri = "ActivityDefinition/usdm-act-vital-signs-and-temperature"
  * relatedAction[+]
    * targetId = "RT"
    * relationship = #after

// Concomitant medications
* action[+]
  * title = "Concomitant medications"
  * definitionUri = "ActivityDefinition/usdm-act-concomitant-medications"
  * relatedAction[+]
    * targetId = "RT"
    * relationship = #after

// Adverse events (per protocol: "adverse events")
* action[+]
  * title = "Check adverse events"
  * definitionUri = "ActivityDefinition/usdm-act-check-adverse-events"
  * relatedAction[+]
    * targetId = "RT"
    * relationship = #after

// Efficacy measures (per protocol: "efficacy measure assessment")
* action[+]
  * title = "ADAS-Cog"
  * definitionCanonical = Canonical(usdm-q-adas-cog)
  * participant[+].type = #practitioner
  * relatedAction[+]
    * targetId = "RT"
    * relationship = #after

* action[+]
  * title = "CIBIC+"
  * definitionCanonical = Canonical(usdm-q-cibic-plus)
  * participant[+].type = #practitioner
  * relatedAction[+]
    * targetId = "RT"
    * relationship = #after

* action[+]
  * title = "DAD"
  * definitionCanonical = Canonical(usdm-q-dad)
  * participant[+].type = #relatedperson
  * relatedAction[+]
    * targetId = "RT"
    * relationship = #after

* action[+]
  * title = "NPI-X"
  * definitionCanonical = Canonical(usdm-q-npi-x)
  * participant[+].type = #relatedperson
  * relatedAction[+]
    * targetId = "RT"
    * relationship = #after
