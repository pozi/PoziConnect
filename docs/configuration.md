# Pozi Connect Configuration

PoziConnect provides a simple interface for accessing, processing, analysing and exporting spatial and non-spatial data.

It uses the power of the popular open source [GDAL/OGR translator library](http://www.gdal.org/index.html), with these important enhancements:

* it provides a simple interface that exposes typical translation functions that administrators can preconfigure using INI files and enable users to select and adjust according to specific tasks
* it uses the bare minimum information required to complete a task; for example:
  * it doesn't care if a destination file or table already exists - it has the intelligence to create or overwrite as necessary
  * it uses the specified source and destination file extensions to determine the required translation settings
* it provides access to Python and database functions within the configuration for operations like indexing and file operations

---

## Running as a batch task

To run multiple Pozi Connect tasks sequetially and avoid having to open up Pozi Connect and pick and run individual tasks, you can configure a 'recipe' for Pozi Connect to follow. This is useful if you have a series of tasks you regularly need to run (for example, M1s) or for setting up as a scheduled task.

Here we will use the Melton M1 tasks as an example.

Create a text file...

`PoziConnect\recipes\Melton M1.txt`

…with the following text…

    Melton\Melton M1 - 1 - Import Authority.ini
    Melton\Melton M1 - 2 - Import Vicmap.ini
    Melton\Melton M1 - 3 - Generate M1.ini

Then create a batch file or scheduled task with the following target:

`PoziConnect.exe --recipe="recipes\Melton M1.txt"`

(You may need to specify the full path to the exe file instead of just `PoziConnect.exe`.)

This will launch Pozi Connect and run all the tasks specified in the recipe.

---

## Configuration

Pozi Connect is controlled using INI files. You can edit these files in a text editor.

If using Windows Notepad, the line returns in existing files may not display correctly. Notepad++ is recommended for editing these files.

### User Settings

Notes:

* If key name ends with 'folder', the interface offers the user a button to launch an Open Folder dialog.
* If key name ends with 'file', the interface offers the user a button to launch an Open File dialog
* If key name ends with 'password', the interface displays dummy characters in place of the populated or typed characters

Examples:

    [User Settings]
    Vicmap_Address_Folder:
    Vicmap_Property_Folder:
    LGA_Code: 302
    Database_File: Output\Ballarat.sqlite

    [User Settings]
    Pathway_DSN: pthprod
    Pathway_User_ID:
    Pathway_Password:
    Pathway_Table_Prefix: pthdbo.

### General Settings

Example:

    [General Settings]
    Description:
        Extract Pathway address and parcel
        information into Pozi Connect database
    Pathway_Connection: ODBC:DSN={Pathway_DSN};UID={Pathway_User_ID};PWD={Pathway_Password}
    Database_File: Output\Ballarat.sqlite

---

## Parameters

### Source/Destination

#### Files

* SHP
* TAB
* CSV
* DXF
* DGN
* GML
* KML
* GPX
* VRT
* XLS, XLSX
* JSON, GeoJSON
* DBF
* MIF
* XML (GeoRSS)

#### Databases

*Note: specify file path or connection, then comma, then table name*

* SQLite (.sqlite, .db)
* PostGIS
* Oracle
* ODBC

#### Web Service

* WFS

#### Examples:

    Source: C:\Temp\Road.tab
    Source: C:\Temp\Vicmap.sqlite,Road
    Destination: PG:host='server.pozi.com' port='5432' dbname='councilgis' user='opengeo' password='abc123',Road
    Destination: OCI:gisadmin/abc123@127.0.0.1,Road

## If

Notes:

* the execution of any section can be made conditional
* use a Python expression to return true or false

Example

    If: os.path.exists('{Input_Folder}/ConquestRoads.TAB')

### Select

Notes:

* Comma-delimited list of fields from input layer to copy to the new layer. A field is skipped if mentioned previously in the list even if the input layer has duplicate field names. (Defaults to all; any field is skipped if a subsequent field with same name is found.) Starting with OGR 2.0, geometry fields can also be specified in the list.
* equates to `-select` parameter in ogr2ogr

Example:

    Select: ogc_fid as fid, prop_propnum as propnum, ezi_address as address, transform(ST_SimplifyPreserveTopology(transform(the_geom, 28355), 1),4326) as the_geom

### Where

Notes:

* Attribute query (like SQL WHERE)
* equates to `-where` parameter in ogr2ogr

Examples:

    Where: prop_propnum is not null and prop_propnum <> ''
    Where: OGR_GEOMETRY='POINT'

### SQL

Notes:

* SQL statement to execute. The resulting table/layer will be saved to the output.
* equates to `-sql` parameter in ogr2ogr

Examples:

    SQL: SELECT * FROM pthdbo.cnacomp (NOLOCK)
    SQL: select RURAL_NO, RDNAME, RDTYPE, PROPNUM, COMMENTS, PRIMARY as IS_PRIMARY, HOUSE, ID, RA_Complete, XCOORD, YCOORD, PROPERTYNA, DATE from Rural_Address_Original_GJ
    SQL: select * from ADDRESS where lga_code = '{LGA_Code}'

### SQLFile

Example:

    SQLFile: {Shared_SQL_Folder}\M1 R Edits.sql

### Native SQLite Processing

When performing operations where the source and destination are the same SQLite database, you can take advantage of SQLite's native query processing rather than OGR's. This may help for some complex queries.

Example:

    SQLProcessing: SQLite


### TransformCoordSys

Notes:

* reproject/transform to this SRS on output
* equates to `-t_srs` parameter in ogr2ogr

Example:

    TransformCoordSys: EPSG:4326

### AssignCoordSys

Notes:

* assign an output SRS
* equates to `-a_srs` parameter in ogr2ogr

Example:

    AssignCoordSys: EPSG:28355

### OverrideCoordSys

Notes:

* override source SRS
* equates to `-s_srs` parameter in ogr2ogr

Example:

    OverrideCoordSys: EPSG:28355

### GeometryType

Notes:

* Define the geometry type for the created layer. One of NONE, GEOMETRY, POINT, LINESTRING, POLYGON, GEOMETRYCOLLECTION, MULTIPOINT, MULTIPOLYGON or MULTILINESTRING.
* equates to `-nlt` parameter in ogr2ogr

Example:

    GeometryType: None

### Index

Example:

    Index: status,tpklpatitl

### SpatialIndex

Example:

    SpatialIndex: No

### Commands

Examples:

    Command: startfile('{Output_Folder}\\')
    Command: DSNList()
    PostCommand: system('ogrinfo {Pathway_Connection}')
    Command: startfile('output\PoziConnect.log')

### SkipInfo

By default, Pozi Connect obtains information about a table and writes it to the log before importing the table's contents. In some circumstatnces, this adds a significant load to the source server. Use `SkipInfo` to prevent Pozi Connect from obtaining the table info.

Example:

    SkipInfo: true

### OGRInfoOnly

Special case used where usual source-destination is not relevant. For example, if updating an existing table.

Example:

    OGRInfoOnly: true

---

## Usage

### Import MapInfo TAB file into SQLite database

    [Vicmap Address]
    Source: {Vicmap_Address_Folder}\ADDRESS.tab
    SQL: select * from ADDRESS where lga_code = '{LGA_Code}'
    Destination: {Database_File},VMADD_ADDRESS
    Index: property_pfi

### Specify destination coordsys and geometry type

    [Vicmap Features of Interest - Polygon]
    Source: {Vicmap_Features_of_Interest_Folder}\FOI_POLYGON.tab
    Destination: {Database_File},vmfeat_foi_polygon
    GeometryType: MULTIPOLYGON
    TransformCoordSys: EPSG:4326

### Filter by geometry type during import

    [Vicmap Features of Interest - Point]
    Source: {Vicmap_Features_of_Interest_Folder}\FOI_POINT.tab
    Where: OGR_GEOMETRY='POINT'
    Destination: {Database_File},vmfeat_foi_point

### Translate MapInfo table to CSV

    [Vicmap Reference Table - VMADD_ACCESS_TYPE]
    Source: {Vicmap_Reference_Folder}\ADDRESS_ACCESS_TYPE.tab
    Destination: {Output_CSV_Folder}\VMADD_ACCESS_TYPE.csv

### Import non-spatial MapInfo TAB file into SQLite database

    [Vicmap Parcel-Property]
    Source: {Vicmap_Property_Folder}\PARCEL_PROPERTY.tab
    Destination: {Database_File},VMPROP_PARCEL_PROPERTY
    GeometryType: NONE
    SpatialIndex: NO
    Index: parcel_pfi,property_pfi

### Update an existing SQLite table

    [Update PC_Council_Property_Address]
    OGRInfoOnly: true
    Destination: {Database_File},dummy
    SQLFile: Tasks\Swan Hill\SQL\Swan Hill PC Council Rural Address.sql

### Delete a table from a SQLite file

    [Vicmap Vegetation - Remove Tree Density]
    OGRInfoOnly: true
    SQL: drop table vmveg_tree_density
    Destination: {Database_File},dummy

### Zip up output

    [General Settings]
    ZipFilePath: {Output_Folder}/PIQA Export.zip
    ZipSession: ZipFile('{ZipFilePath}', 'a', ZIP_DEFLATED)

    [PIQA Parcel Export]
    Source: {PlaceLabDB}
    SQLFile: {ParcelSQLFile}
    Destination: {Output_Folder}/PIQA Parcel Export.CSV
    PostCommand: {ZipSession}.write('{Destination}')

    [PIQA Zip Finalisation]
    Command: {ZipSession}.close()
    [Display in Windows Explorer]
    Command: startfile('{Output_Folder}\\')

