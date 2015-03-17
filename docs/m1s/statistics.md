# Pozi Connect: M1 Statistics

## Usage

After generating your M1 in Pozi Connect, visit the [Pozi Connect Property Health Dashboard](http://dashboard.pozi.com/property/).

![Pozi Connect Property Health Dashboard](http://i.imgur.com/kOlywWO.png)

In Windows Explorer, navigate to your `PoziConnect\output\Statistics\` folder, and drag your property statistics .json file from the folder and drop it into the Property Health Dashboard web page.

View your statistics.

Optionally download a PDF report by clicking the red button.

#### Troubleshooting

If you experience problems with seeing the result in Internet Explorer, try using a different web browser.

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

## FAQ

#### Why are there items like `vicmap_parcels_no_propnum`, and not `vicmap_properties_no_propnum`?

Pozi Connect treats properties as council-defined entities. In a council-centric view, a 'property' is created when the council assigns a property number to one or more parcels. (Although Vicmap does create property records with null property numbers, Pozi Connect doesn't see these as having any real meaning to the council.)

Statistics items like `vicmap_parcels_no_propnum` are measures of the number of parcels to which the council should assign a property number.
