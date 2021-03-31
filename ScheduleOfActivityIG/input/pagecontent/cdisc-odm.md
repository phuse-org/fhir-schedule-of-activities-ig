# CDISC Operational Data Model

The CDISC Operational Data Model (ODM) is a XML-based model defined for the transport and archival of Clinical Trials Data; it is broadly made up of the following top-level elements
* Clinical Data - actual datapoints gathered on study participants
* Metadata - definitions used to capture and report the data collected
* Administrative Data - information regarding the collection of data (sites, personnel, etc)
* Reference Data - common data needed to interpret the collected data

Structures within the ODM have little semantic meaning; it is a format focused on the representation of planned and performed activities so captures relationships between elements moreso than the actual actual definition of the element itelf; for example - there is no characterisation of a participant (in contrast to the Patient resource); there is a `SubjectData` element used to collect captured datapoints for an individual participant.  The `SubjectData` element includes attributes such as an OID as an identifier, but there is no information model that says the OID is an external identifier (eg Subject ID) or some other internal identifier (eg Primary Key from a Subjects table, as an example). 

Broadly the structure is as follows (for ODM 1.3.2):
* ODM
  * Study
    * MetadataVersion
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