# CDISC Operational Data Model (ODM)

## TLDR: Show me the schema!
The ODM Schema is available at: [ODM Schema](https://bitbucket.cdisc.org/projects/XML/repos/odm/browse/schema)

## What is the ODM
The CDISC Operational Data Model (ODM) is a XML-based model defined for the transport and archival of Clinical Trials Data; it is broadly made up of the following top-level elements
* Clinical Data - actual datapoints gathered on study participants
* Metadata - definitions used to capture and report the data collected
* Administrative Data - information regarding the collection of data (sites, personnel, etc)
* Reference Data - common data needed to interpret the collected data

Structures within the ODM have little semantic meaning; it is a format focused on the representation of planned and performed activities so captures relationships between elements moreso than the actual actual definition of the element itself; for example - there is no characterisation of a participant (in contrast to the Patient resource); there is a `SubjectData` element used to collect captured datapoints for an individual participant.  The `SubjectData` element includes attributes such as an OID as an identifier, but there is no information model that says the OID is an external identifier (eg Subject ID) or some other internal identifier (eg Primary Key from a Subjects table, as an example). 

Data collection is driven by Forms; forms group activities by type (ie all the Vital Signs observations for a single visit are usually grouped in a single form, irrespective of multiple planned timepoints for the elements).  Individual fields on a form are classed as Items in ODM parlance and have associated metadata pertaining to the allowable content (eg datatype, length, constrained values or allowable units for a value)


## 
Broadly the structure is as follows (for ODM 1.3.2):
* ODM
  * Study
    * MetaDataVersion
      * StudyEvent
        * Form
          * ItemGroup
            * Item
  * Study Data
    * SubjectData
      * StudyEventData
        * FormData
          * ItemGroupData
            * ItemData

The specification is distributed as an XML document, and as such can be extended through the use of vendor namespaces; examples where this has been done include:
* Study Design Model - extensions to cover topics such as workflow, study design concepts
* Dataset-XML - extensions to use for transporting datasets

The implementation of the Study Metadata follows a DEF-REF pattern.  We define a type of element (eg Visit, Form, Field) and then reference it one or more times within the corresponding element; as an example:
```xml
<StudyEventDef OID="SE.SCREENING_VISIT" Name="Screening Visit (Visit 1)" Repeating="No" Type="Scheduled">
  <Description>
    <TranslatedText xml:lang="en">Screening Visit at day -14</TranslatedText>
  </Description>
  <FormRef FormOID="F.DOV" Mandatory="Yes" OrderNumber="1"/>
  <FormRef FormOID="F.DS_IC" Mandatory="Yes" OrderNumber="2"/>
  <FormRef FormOID="F.IE" Mandatory="Yes" OrderNumber="3"/>
  ...
</StudyEventDef>
...
<FormDef OID="F.DOV" Name="Date of Visit" Repeating="No">
	<Description>
			<TranslatedText xml:lang="en-US">Subject Visits consolidates information about the timing of subject visits that is otherwise spread over domains that include the visit variables (VISITNUM and possibly VISIT and/or VISITDY).</TranslatedText>
	</Description>
	<ItemGroupRef ItemGroupOID="IG.DOV" Mandatory="Yes" OrderNumber="1"/>
</FormDef>
```



## How the schedule of activities implemented in ODM 
The entry point for the defined activities in the ODM is through the ODM>Study>MetaDataVersion; a MetaDataVersion is a defined set of study configuration; from this point


### Protocol
The Protocol lists the kinds of study events that can occur within a specific version of a Study. All clinical data must occur within one of these study events.


