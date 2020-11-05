# Pozi Connect: Victorian Council Data Audits

Pozi Connect generates parcel and property/address audits when it creates an M1. Use these audit reports to uncover anomalies in your council's data.

Described below are techniques for filtering the audits to narrow down the records to show only the ones that require further attention.

### Opening Audit

When opening a spreadsheet:

##### split window to freeze column headings

* place cursor in A2 cell, then `ALT` + `W` + `S` (doesn't work on all versions of Excel)
  or
* manually drag split pane control down past the first row

##### set autofilter on/off

* keyboard shortcut `ALT` + `D` + `F` + `F`

##### expand columns

* click top left corner to highlight all rows, then double-click on any column divider)

### Filtering Audit

*Example filter to select only `0` values*

![](http://i.imgur.com/rjvYdGt.png)


## Council Parcel

Audit file: `Audit - Council Parcels.csv`

### Structure

Column|Description|Usage
:--|:--|:--
`spi`|council parcel description (in SPI format) constructed from council parcel attributes|
`crefno`|council parcel id|
`propnum`|council property number|
`summary`|council-maintained combined address (council reference only)
`status`|council parcel status
`spi_validity`|description of any detected instances of SPI not meeting Vicmap rules|filter on `NOT (Blank)` to list non-compliant parcel descriptions
`spi_in_council`|number of properties in Council that share this SPI
`council_propnums`|list of property numbers in Council that share this SPI
`spi_in_vicmap`|number of parcels in Vicmap that match this SPI|filter on `0` to list Council parcel descriptions that don't exist in Vicmap
`spi_propnum_in_vicmap`|number of parcels in Vicmap that match this SPI and property number
`vicmap_propnums`|list of property numbers in Vicmap that share this SPI
`partial_spi_in_vicmap`|number of parcels in Vicmap that match on `plan_numeral` but not `plan_prefix`|filter on `NOT 0` to list parcels with potentially incorrect plan prefix
`alt_spi_in_vicmap`|number of parcels in Vicmap that match on `further_description` field instead of `spi`|filter by `NOT 0` to list parcels with potentially incorrect plan prefix
`suggested_spi`|Vicmap SPI that matches closely to Council parcel based on existing `crefno` or partial SPI match|filter on `NOT (Blank)` to list potential easy fixes for invalid parcel descriptions
`propnum_in_council`|number of Council parcel records that share this `propnum`
`propnum_in_vicmap`|number of Vicmap parcel records that matched to this `propnum`|**filter on `0` to list unmatched properties, ie, CRITICAL**
`crefno_in_vicmap`|number of Vicmap parcel records that matched to this `crefno`|**filter on `0` to list unmatched parcels, ie, CRITICAL**
`m1_edit_code`|update pending for this parcel|filter on `(Blank)` to list records not already flagged for update in current M1
`m1_comments`|comments for pending update

### Examples

#### Unmatched parcels, with suggested parcel description fixes (critical, easy)

The most valuable records to target, as they will result in new matches and are likely to be easily solved.

* `propnum_in_vicmap`: 0
* `spi_in_vicmap`: 0
* `suggested_spi`: NOT (Blank)

#### Plan Prefix Anomalies

Likely to be easily solved by updating a plan prefix. See `suggested_spi` field for a hint of the correct plan prefix.

* `spi_in_vicmap`: 0
* `partial_spi_in_vicmap`: NOT 0

#### Gridlocked Records

These are parcels that should be matched to Vicmap, but Pozi Connect cannot match them due to conflicting associations on the target  Vicmap parcel.

It's possible these will clear up in subsequent M1s after Pozi Connect removes any redundant records. Alternatively, if these remain unresolved, they should be manually inspected to determine if changes in the council property system are required to break the deadlock.

* `m1_edit_code`: (Blank)
* `propnum_in_vicmap`: 0
* `spi_in_vicmap`: NOT 0

#### Parish and Township Codes

The `suggested_spi` field will often contain a parish/township code. To find the parish/township names that correspond with the codes, use the following lists.

Parish codes (PP2..., PP3..., PP4...):
https://github.com/pozi/PoziConnectConfig/blob/master/~Shared/Reference/VMADMIN_PARISH.csv

Township codes (PP5...):
https://github.com/pozi/PoziConnectConfig/blob/master/~Shared/Reference/VMADMIN_TOWNSHIP.csv

You can type the code (without the 'PP') into the 'Search this file...' section to quickly find the parish or township name.

## Council Property Address

Audit file: `Audit - Council Property Address.csv`

### Structure

Column|Description|Usage
:--|:--|:--
`propnum`|council property number
`status`|council property status
`address`|combined council address constructed from council address attributes
`locality`|council locality
`summary`|council-maintained combined address (council reference only)
`address_validity`|description of any detected instances of address not meeting Vicmap rules|filter on `NOT (Blank)` to list non-compliant addresses
`parcels_in_council`|number of parcels in Council that share this propnum
`council_parcels`|list of parcels in Council that share this propnum
`parcels_in_vicmap`|number of parcels in Vicmap that match this propnum
`vicmap_parcels`|list of parcels in Vicmap that match this propnum
`vicmap_address`|address of property in Vicmap that matches this propnum
`vicmap_locality`|locality of property in Vicmap that matches this propnum|filter on `N` to list wrong locality in Council
`propnum_in_vicmap`|Council property number exists in Vicmap (Y/N)
`address_match_in_vicmap`|Council address matches Vicmap address (Y/N)
`locality_match_in_vicmap`|Council locality matches Vicmap locality (Y/N)
`road_locality_in_vicmap`|Council road name/locality combination exists in Vicmap (Y/N)
`current_m1_edit_code`|update pending for this parcel|filter on `(Blank)` to list records not already flagged for update in current M1
`current_m1_comments`|comments for pending update

### Examples

#### Locality Anomalies

Filter

* `locality_match_in_vicmap`: N
* `is_primary`: not N
* `house_number_1`: not blank

## Vicmap Property address

### Examples

#### Fragmented Properties

* `cohesion`: < 0.001
* `propnum`: not blank
