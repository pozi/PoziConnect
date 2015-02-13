<img src="http://i.imgur.com/TLMFPUa.png" alt="Groundtruth" width="200">

# Configuration for Pozi Connect for M1s

Obtain from Council

* any status codes for filtering properties?
* number of properties at date of extract
* example retired/cancelled/historic/dummy property numbers
* assign 'NCPR' to all common properties?
* SHP or TAB?
* rural addressing (separate table and/or flag in property system)

Start Configuration

* obtain council data
* order and download Vicmap data
* create new folder _Council Name_ based on client name
* copy INI and SQL files from similar site (based on an existing site using the same property system) into new folder
* replace references to previous council SQLite file name with new council name
* look up [LGA code](https://github.com/groundtruth/PoziConnectConfig/blob/master/~Shared/Reference/VMADMIN_LGA.csv) and update INI settings in Process Vicmap task and both SQL files

For each of Parcel and Property/Address SQL:

* if using council's existing PIQA SQL as starting point:
  * replace tabs with spaces (4)
  * convert upper case SQL syntax to lower case (edit manually or try [Instant SQL Formatter](http://www.dpriver.com/pp/sqlformat.htm))
  * replace old field names
  * add expression for num_road_address/ezi_address or spi/simple_spi
* include any necessary expression in road name standardise with Vicmap
  * replace (apostrophe) with (blank)
  * replace & with AND
  * replace ' - ' with '-'
  * etc
* ensure propnum and crefno fields are character fields
* remove any unneeded fields
* eliminate null values (replace with blanks if appropriate), *especially spi, propnum*
* test query against council's data
* check that address values comply with:
  * [BLG_UNIT_TYPE](https://github.com/groundtruth/PoziConnectConfig/blob/master/~Shared/Reference/VMADD_BLG_UNIT_TYPE.csv)
  * [FLOOR_TYPE](https://github.com/groundtruth/PoziConnectConfig/blob/master/~Shared/Reference/VMADD_FLOOR_TYPE.csv)
  * [LOCATION_DESCRIPTOR](https://github.com/groundtruth/PoziConnectConfig/blob/master/~Shared/Reference/VMADD_LOCATION_DESCRIPTOR.csv)
* test if the Parcel and Property/Address queries return the same set of property numbers
  * check for parcels without properties: `select * from pc_council_parcel where propnum not in ( select propnum from pc_council_property_address )`
  * check for properties without parcels: `select * from pc_council_property_address where propnum not in ( select propnum from pc_council_parcel )`
* check for blank values in road_type field: `select * from pc_council_property_address where road_type = ''`
* generate 'sampler' query (10 records from each edit code)
* copy/paste results into audit template and email to council