# Pozi Connect for M1s Release History

### Complete History

For a complete history of all changes, see:
https://github.com/groundtruth/PoziConnectConfig/commits/master/~Shared/

### Highlights

Here are some of the important developments.

##### May 2015

* improve address validity check to detect invalid ranges for unit and house numbers

##### Apr 2015

* fix bug in address match statistics
* improve accuracy of audits and statistics by excluding hyphens and apostrophes from road name comparisons

##### Mar 2015

* improve QGIS integration by forcing refresh of spatial index
* upgrade to latest GDAL library `release-1600-gdal-1-11-1-mapserver-6-4-1` (up from `1-10-1`)
* improve comments on M1s to clarify which propnums and crefnos being replaced do not exist in council
* improve readability of documentation with new webpage template (`viewdocs-yeti`)
* add parcel area to Vicmap audit
* provide central location for latest releases: https://github.com/groundtruth/PoziConnect/releases/latest

##### Feb 2015

* massively improve performance of council parcel audit for councils who don't maintain crefno (from 14 minutes down to 16 seconds)
* improve commenting to show if propnum being removed from parcel exists in council records, and also if property being matchecd is a proposed one
* clean up PIQA output by excluding non-primary address records

##### Jan 2015

* improve warning on potentially conflicting locality
* include more address updates (eg, change in building name)
* improve reporting for discrepancies between Council addresses and Vicmap addresses

##### Dec 2014

* package Pozi Connect into Windows installer
* prevent populating address attributes that violate M1 rules
* add Vicmap Property Address audit, including 'cohesion' setting to help find fragmented properties
* cater for Vicmap parcels without parcel-prop link

##### Nov 2014

* improve processing logic to prevent rejects at SKM

##### Oct 2014

* create separate subfolders for various output files
* fix spatial output by separately processing approved and proposed address updates

##### Sep 2014

* document how to use audit spreadsheets
* commence tracking history of M1 edits
* improve comments, including adding address details and warning for conflicting localities
* improve logic for populating pfi values only when required

##### Aug 2014

* add property statistics reporting
* add new retirement scenario
* eliminate duplicate records
* add Vicmap parcel audit

##### Jul 2014

* check for invalid plan prefixes, invalid characters in address fields, SPI length
* improve comments

##### Jun 2014

* standardise audit processes
* create Valuer General report

##### May 2014

* spatialise M1 and Audit output - visualise audits and M1s as map layers
* add check for missing plan prefix, unit number, floor type
* cater for base property numbers

##### Apr 2014

* detect invalid characters in parcel descriptions
* improve comments and address checking
* add addresses to multi-assessment updates

##### Mar 2014

* check for valid road name and type

##### Feb 2014

* introduce council property address audit
* check for out-of-range plan numbers
* check for invalid characters in parcel descriptions

##### Jan 2014

* introduce council parcel audit
* check for valid property numbers

### Future Development

Here's what is on the cards for the next twelve months:

* improve documentation
* working closer with SKM to improve M1 loads
* QGIS integration