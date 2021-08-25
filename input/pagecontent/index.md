### Background

# Schedule of Activities Project

This IG is intended to provide a roadmap for adopters looking to use FHIR resources in order to support the planning and implementing Clinical Research designs.  This is intended to primarily facilitate high level components.

As it is used commonly, part of the design of this IG will illustrate patterns and examples for reusing design concepts from the [CDISC ODM](cdisc-odm.html).

The ODM used is available in the [H2Q-MC-LZZT Study Design](h2q-mc-lzzt.html) file.

## Design
{%include high-level-overview.svg%}

## Deliverables

The output and test for this project is the creation of a set of FHIR [Bundle](http://hl7.org/fhir/bundle.html) which can be used to load in data to an EHR system

* Bundle 1 - Shell for Study and Study Design
* Bundle 2 - Study Design with Study Activties
* Bundle 3 - Study Design with Scheduled Activities (taking Chest X-ray as an example)
* Bundle 4 - Study Design with all Scheduled Activities 

Part of the process of delivering the bundles depends on ensuring that the content has been tested.  Owing to the way the IG builds, the Bundle Resources are not currently available in the UI, so the user needs to run `sushi` and look in the `fsh-generated/resources` folder to locate the bundles.






