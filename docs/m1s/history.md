# Pozi Connect Release History

## Highlights

Here are some of the improvements and bug fixes. (For a complete history of all changes, see [here](
https://github.com/pozi/PoziConnectConfig/commits/master/~Shared/))

### Version 2.9 (Sep 2021)

* support for new Datashare data supplies
* prevent property number updates where existing address is a complex site
* include parcel pfi for proposed parcels
* populate floor type only if floor number exists
* don't trigger update for unit type if unit number doesn't exist
* improve handling of building/complex name changes
* ensure property_pfi is not empty for A edits
* remove distance_related_flag when house number is blank
* don't populate building names greater than 45 characters
* populate road name with existing road name from Vicmap if council road name is a close match but not an exact match
* remove rural address when house number is blank
* prevent Comments being null when address isn't perfectly formed
* update all references from Groundtruth to Pozi
* upgrade GDAL library to v3.1.4
* various bug fixes
* configuration updates for Frankston, Strathbogie, Wangaratta, Maribyrnong, West Wimmera, Campaspe, Melton, Warrnambool, Surf Coast, Murrindindi, Glen Eira, Manningham, Hobsons Bay, Kingston, Indigo, Latrobe, Hepburn, Swan Hill, Monash, Baw Baw, Mitchell, Mildura, Maroondah and Ballarat

### Version 2.8 (Feb 2020)

* improve performance of P edit query
* detect new distance-based addresses
* detect new floor and building details
* populate property_pfi for multi-property parcels
* enable Township parcels to be recognised in multi-assessments
* allow NCPRs to be replaced if address is the same
* allow invalid property numbers to be replaced with NCPR
* improve formatting of Pozi map links to better enable Excel to recognise them as links
* prevent locality conflict warning if name contains a bracket
* remove note about parcel linking to multiple properties
* enable user editing of database connection
* upgrade to GDAL 3.0.0
* various bug-fixes
* change branding from Groundtruth to Pozi
* configuration updates for Maribyrnong, Loddon, Mitchell, Moorabool, Murrindindi, Moira, Bass Coast, Northern Grampians, South Gippsland, Moonee Valley, Alpine, Colac Otway, Latrobe, Frankston, Hindmarsh, Bendigo, Mornington Peninsula, Ballarat, Melton, Towong, Swan Hill, Casey, Mount Alexander, Indigo, Baw Baw, Pyrenees

### Version 2.7 (Jun 2018)

* prevent overwriting addresses if there are multiple unique addresses already associated with that property number in Vicmap
* exclude from A edits any properties associated with current R edits
* improve detection of most appropriate pfi to use when updating multi-property parcels
* detect new hotel style addresses
* improve performance of Vicmap Property Address audit
* update M1 R edit comments to include all parcels that property will be later matched to
* add support for CP and PC plans in SPEAR report
* move Parcel Audit address field closer to front to improve readability
* update VMREFTAB look-up tables
* upgrade GDAL library to `release-1911-gdal-2-2-3-mapserver-7-0-7`
* switch application version numbering to Semantic Versioning standards
* configuration updates for Ballarat, Bass Coast, Buloke, Cardinia, Glen Eira, Golden Plains, Latrobe, Maribyrnong, Maroondah, Mitchell, Monash, Moonee Valley, Moreland, Nillumbik, Northern Grampians, South Gippsland, Stonnington, Swan Hill

### Version 2.06 (Oct 2017)

* prevent unneeded house number removal warning
* populate dist_rel field with Vicmap value if no Council vlaue found
* revert to old-style map link format to resolve incompatibility with older versions of Excel
* configuration updates for Monash, Hepburn

### Version 2.05 (Oct 2017)

* populate most suitable property_pfi for multi-property parcels
* enforce geometry types for output layers
* update Pozi web links to new format
* update Exception table generation
* upgrade GDAL library to `release-1800-gdal-2-1-3-mapserver-7-0-6`
* configuration updates for Hepburn, Glen Eira, Hindmarsh, Wangaratta, Moorabool

### Version 2.04 (Jun 2017)

* add support for M1 exception list
* prevent replacement of NCPR properties that contain addresses
* enable R edits on some previously excluded properties
* prevent Mt/Mount road name discrepancy triggering S edit
* improve parcel matching for Valuer General report
* update Valuer General report output format to CSV to avoid formatting issues
* upgrade GDAL library to `release-1800-gdal-2-1-3-mapserver-7-0-4`

### Version 2.02 (Feb 2017)

* prevent retirement of NCPR properties
* prevent retirement of properties for which the council doesn't have any parcel records
* re-add SPI attribute for all P edits
* fix audit message pointing to wrong field
* add crown status to Vicmap Parcel audit

### Jan 2017

* add Valuer General Reports for all councils
* upgrade GDAL library from `release-1600-gdal-1-11-1-mapserver-6-4-1` to `release-1800-gdal-2-1-2-mapserver-7-0-2`

### Dec 2016

* prompt user to confirm property_pfi for parcels that relate to multiple properties
* eliminate duplicate multi-assessment edits

### Nov 2016

* generate address updates only for valid road names
* improve readability of M1 by removing redundant attributes (plan_number and lot_number)

### Oct 2016

* warn user if building name exceeds valid length
* improve audit performance by removing `alt_spi_in_council` calculation
* improve comments for R edits involving NCPR properties
* update audit map links

### Aug 2016

* add parcel area output to Valuer General report

### Jun 2016

* fix SPI formula - cater for parcels with section but no allotment
* change default projection for distance-based addresses to VicGrid (because Jacobs can't handle lon/lat)
* support for multi-status addresses (to avoid reject "Property Identifier has multiple matches")
* prevent attempting to match to non-existent road properties

### May 2016

* update map links
* add generic Property.Gov extract task

### Apr 2016

* improve address validity check to detect invalid house suffix values

### Mar 2016

* improve performance of audit queries

### Feb 2016

* improve edit rules:
  * prevent "Property PFI is superseded" error
  * when updating distance-related addresses, populate with existing coordinates
  * ensure every invalid multi-assessment is retired

### Jan 2016

* improve edit rules:
  * prevent multi-assessments being added where property already exists in overlapping multi-lot parcel
* make task names easier to understand: rename 'VG Report' to 'Valuer General Report'
* improve comments
  * warn of house number being removed
  * warn of adding multi-assessment with different road name
  * warn of replacing distance-based address with non-distance-based address

### Dec 2015

* fix bug in generating map links
* fix bug that generated retirements when a spi value was blank
* fix bug that caused incorrect address to be displayed in comments on rare occasions

### Nov 2015

* reduce time taken for council parcel audit by up to two thirds
* reduce time taken for council property audit by up to one third
* re-enable retiring of invalid multi-assessments so they can be matched properly in subsequent M1 (bug fix)
* improve parcel audit results by checking for invalid section values

### Oct 2015

* improve edit rules:
  * prevent retiring properties created via SPEAR
* improve comments
  * warn of transfer of parcel that includes existing primary distance-based address

### Sep 2015

* improve edit rules:
  * exclude any address updates for proposed parcels if the address belongs to a property that is already being updated in another address edit

### Jul 2015

* improve edit rules:
  * exclude properties being matched to an approved parcel if the number is already matched to a proposed parcel

### Jun 2015

* improve edit rules:
  * resolution of 'gridlocked' properties - now P edits can replace a property if that property can be matched elsewhere
  * limit address updates for proposed parcels to one per property number
  * better detect overlapping parcels when dealing with muti-assessment retirements
  * better determining of when to use new_road flag
  * prevent retiring multi-assessment properties that can't be matched later to another valid parcel
* improve comments:
  * show if multi-assessments relate to proposed parcels
  * show if property updates involve new properties
  * explain why valid properties are being removed from multi-assessments (so they can be later matched to the correct parcel)

### May 2015

* improve address validity check to detect invalid ranges for unit and house numbers
* improve parcel validity check to detect missing parish
* improve speed of address update query
* improve support for hotel-style addressing
* improve comments to show original source of properties being removed

### Apr 2015

* fix bug in address match statistics
* improve accuracy of audits and statistics by excluding hyphens and apostrophes from road name comparisons

### Mar 2015

* improve QGIS integration by forcing refresh of spatial index
* upgrade to latest GDAL library `release-1600-gdal-1-11-1-mapserver-6-4-1` (up from `1-10-1`)
* improve comments on M1s to clarify which propnums and crefnos being replaced do not exist in council
* improve readability of documentation with new webpage template (`viewdocs-yeti`)
* add parcel area to Vicmap audit
* provide central location for latest releases: https://github.com/pozi/PoziConnect/releases/latest

### Feb 2015

* massively improve performance of council parcel audit for councils who don't maintain crefno (from 14 minutes down to 16 seconds)
* improve commenting to show if propnum being removed from parcel exists in council records, and also if property being matchecd is a proposed one
* clean up PIQA output by excluding non-primary address records

### Jan 2015

* improve warning on potentially conflicting locality
* include more address updates (eg, change in building name)
* improve reporting for discrepancies between Council addresses and Vicmap addresses

### Dec 2014

* package Pozi Connect into Windows installer
* prevent populating address attributes that violate M1 rules
* add Vicmap Property Address audit, including 'cohesion' setting to help find fragmented properties
* cater for Vicmap parcels without parcel-prop link

### Nov 2014

* improve processing logic to prevent rejects at SKM

### Oct 2014

* create separate subfolders for various output files
* fix spatial output by separately processing approved and proposed address updates

### Sep 2014

* document how to use audit spreadsheets
* commence tracking history of M1 edits
* improve comments, including adding address details and warning for conflicting localities
* improve logic for populating pfi values only when required

### Aug 2014

* add property statistics reporting
* add new retirement scenario
* eliminate duplicate records
* add Vicmap parcel audit

### Jul 2014

* check for invalid plan prefixes, invalid characters in address fields, SPI length
* improve comments

### Jun 2014

* standardise audit processes
* create Valuer General report

### May 2014

* spatialise M1 and Audit output - visualise audits and M1s as map layers
* add check for missing plan prefix, unit number, floor type
* cater for base property numbers

### Apr 2014

* detect invalid characters in parcel descriptions
* improve comments and address checking
* add addresses to multi-assessment updates

### Mar 2014

* check for valid road name and type

### Feb 2014

* introduce council property address audit
* check for out-of-range plan numbers
* check for invalid characters in parcel descriptions

### Jan 2014

* introduce council parcel audit
* check for valid property numbers

## Complete History

For a complete history of all changes, see:
https://github.com/pozi/PoziConnectConfig/commits/master/~Shared/
