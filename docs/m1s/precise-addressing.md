# Precise Addressing

By default, property addresses positions are determined by DELWP. Based on information provided by the council (such as what parcels are occupied by the property, and the address attributes), address points are placed automatically inside the property boundary, typically at eight metres inside the centre of the property frontage.

Councils have the option of specifying the exact location in their M1s. This is the basis of rural (distance-based) addressing, but it can also be used within urban areas to make addresses more usable. It is especially useful to specify separate address locations for multi-assessment properties, where each property can have its own separate entrance.

Pozi Connect can be configured to obtain address coordinates from a data source maintained by the council. The location information can be stored within the property system itself, or in an external file like a CSV, TAB or SHP file. The coordinates are read or derived from the source, and appended to the existing address attributes already obtained from the property system. Address locations are optional, so a council needs only to maintain address location information for the addresses it wants to change from the default or existing location in Vicmap.

## Prerequisites

Acceptable formats:

* MapInfo TAB
* Esri SHP
* CSV
* Property System (eg, Pathway, Authority)

Spatial tables must contain point geometries. Non-point geometries will be ignored.

The following fields are used by Pozi Connect. The names of the fields in the point table can be different to the names specified here.

#### Required field:

* `propnum`

#### Optional fields:

* `house_number_1` (if not specified, Pozi Connect will assume it's the council's primary address)
* `is_primary` (if not specified, Pozi Connect will assume it's a primary address)
* `outside_property` (if not specified, Pozi Connect will assume it's inside the property)
* `distance_related_flag` (if not specified, Pozi Connect will populate the value based on the council's preferred default)

#### For non-spatial sources (eg, property system, CSV):

* `easting`
* `northing`
* `datum_proj` (if not specified, Pozi Connect will populate the value based on the council's preferred default)

#### For spatial sources (eg, TAB, SHP):

Pozi Connect will obtain the coordinates from the spatial point object itself. Councils do not have to populate coordinates manually. The coordinates will be extracted in the pre-determined coordinate system, and rounded to the nearest metre along each axis.

## Pozi Connect Configuration

If your council has a support and software maintenance arrangement for Pozi Connect, Groundtruth will configure the Precise Addressing functionality for you. Send your address point table to Groundtruth to get started.

What to provide to Groundtruth:

* zipped address point table (TAB, SHP or CSV)
* exact file path of the address point table on your network
* preferred value for `distance_related_flag`
* preferred value for `datum_proj` (if using non-spatial source)

The new configuration will returned to you.

#### Before

```
Swan Hill M1 - 1 - Import Authority
Swan Hill M1 - 2 - Import Vicmap
Swan Hill M1 - 3 - Generate M1
```

#### After

```
Swan Hill M1 - 1 - Import Authority
Swan Hill M1 - 2 - Import Rural Addresses
Swan Hill M1 - 3 - Import Vicmap
Swan Hill M1 - 4 - Generate M1
```

## Use Cases

* **Rural address**: place point at property entrance, eight metres inside the boundary, and populate the property number
* **Differentiate property entrance locations for multi-assessments**: place point at each entrance, and populate each with the respective property number
* **Shared rural driveways**: as above, and maintain a field for `outside_property` and populate it with 'N' in any of the records where the address point is not within its own property boundary

## Limitations

There are some limitations of support for precise addressing in Pozi Connect.

Councils can choose to fund development of Pozi Connect to provide the functionality they require. Contact Groundtruth for a quote.

##### Updating Address Locations

Pozi Connect bases its updates on non-spatial criteria. It doesn't compare coordinates of Vicmap vs coordinates in the council's point table. Therefore, differences in address point locations are not currently detected by Pozi Connect.

##### Secondary Adresses

Pozi Connect currently supports updating of only one address per property. There is no support for updating secondary addresses.

Any addresses in the point table that are specified as non-primary will be filtered out and ignored by Pozi Connect.

If you require secondary addresses to be added, updated or removed in Vicmap, it is recommended to add this information manually to your next M1.

