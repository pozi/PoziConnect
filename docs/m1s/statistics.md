# Pozi Connect: M1 Statistics

## Usage

After generating your M1 in Pozi Connect, visit the [Pozi Connect Property Health Dashboard](http://dashboard.pozi.com/property/).

![Pozi Connect Property Health Dashboard](http://i.imgur.com/kOlywWO.png)

In Windows Explorer, navigate to your `PoziConnect\output\Statistics\` folder, and drag your property statistics .json file from the folder and drop it into the Property Health Dashboard web page.

View your statistics.

Optionally download a PDF report by clicking the red button.

## Statistics Items

Item|Description
:--|:--
`lga_code`|
`vicmap_properties`|
`vicmap_parcels`|
`vicmap_parcel_properties`|
`council_properties`|
`council_parcels`|
`council_parcel_properties`|
`council_properties_in_vicmap`|
`council_properties_not_in_vicmap`|
`vicmap_parcels_no_propnum`|
`vicmap_parcels_no_propnum_ps600000+`|
`vicmap_parcels_no_propnum_tp`|
`vicmap_parcels_no_propnum_other_plan`|
`vicmap_parcels_no_propnum_cm`|
`vicmap_parcels_no_propnum_res`|
`vicmap_parcels_no_propnum_crown_parcel`|
`vicmap_parcels_no_propnum_plan_related`|
`vicmap_parcels_no_propnum_crown_desc`|
`vicmap_propnum_not_in_council`|
`vicmap_propnum_not_in_council_approved`|
`vicmap_propnum_not_in_council_proposed`|
`vicmap_address_in_council`|
`vicmap_address_not_in_council`|
`vicmap_properties_cm_address`|
`vicmap_parcels_ncpr`|
`council_address_in_vicmap`|
`council_address_in_vicmap`|

## Data Health Indicators

The three main statistics displayed at the top of the report will give you a good idea of the health of the council's data. We expect these statistics to improve as the council submits its M1s. The tips below will enable you to proactively target the issues behind the remaining issues to further improve the statistics.

### Council properties not in Vicmap

Open your `Audit - Council Parcel.csv` spreadsheet, and filter by:

* propnum_in_vicmap = 0
* m1_edit_code = (blank)

This will give you all the properties that aren't in Vicmap and aren't being matched by Pozi Connect. You'll probably need to fix the parcel descriptions in your property system in order for Pozi Connect to find a match.

### Vicmap parcels without propnum

Open your `Audit - Vicmap Parcel.csv` spreadsheet, and filter by:

* propnum_in_council = 0

This will give you all the parcels that don't have a property number. You'll need to allocate the parcel descriptions to the appropriate properties in your property system in order for Pozi Connect to find a match.

### Vicmap propnum not in Council

There is no need to do anything about these. They will be removed on the
next M1.

## FAQ

#### Why are there items like `vicmap_parcels_no_propnum`, and not `vicmap_properties_no_propnum`?

Pozi Connect treats properties as council-defined entities. In a council-centric view, a 'property' is created when the council assigns a property number to one or more parcels. (Although Vicmap does create property records with null property numbers, Pozi Connect doesn't see these as having any real meaning to the council.)

Statistics items like `vicmap_parcels_no_propnum` are measures of the number of parcels to which the council should assign a property number.

#### I've just updated Vicmap, and now I want to see my latest stats.

To generate updated statistics, Pozi Connect needs to import the council's latest property data and the latest version of Vicmap. It re-calculates the statistics when it generates the M1.

Follow the usual three (or four) steps that you do for doing an M1. At the end of the step 3, Pozi Connect automatically launches the [webpage](http://dashboard.pozi.com/property/) in your browser and you can drag the `PoziConnect\output\Statistics\[your council] Property Statistics.json` file into the webpage.

Whether you choose to submit the M1 that gets created is optional.

#### Troubleshooting

If you experience problems with seeing the result in Internet Explorer, try using a different web browser.


