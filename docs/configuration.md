# Pozi Connect Admin Guide

PoziConnect provides a simple interface for accessing, processing, analysing and exporting spatial and non-spatial data.

It uses the power of the popular open source [GDAL/OGR translator library](http://www.gdal.org/index.html), with these important enhancements:

* it provides a simple interface that exposes typical translation functions that administrators can preconfigure using INI files and enable users to select and adjust according to specific tasks
* it uses the bare minimum information required to complete a task; for example:
  * it doesn't care if a destination file or table already exists - it has the intelligence to create or overwrite as necessary
  * it uses the specified source and destination file extensions to determine the required translation settings
* it provides access to Python and database functions within the configuration for operations like indexing and file operations

---

## Installation

If you are installing Pozi Connect for the first time, or if your current version is less than than version 1.25, follow the steps for the full installation. If you have version 1.25 or above, skip the full installation, and instead follow the steps for updating your application and configuration files.

### Full Installation

1. download the full [Pozi Connect installer](https://dl.dropboxusercontent.com/u/401098/Pozi-Connect-Installer-1.31a.exe) (version: 1.31a, updated on 27 Dec 2014)
2. run the installer
3. when it prompts you, specify a folder location. You can choose anywhere; somewhere like `C:\` or `C:\Program Files\`, or even a folder on your network. A folder named ‘PoziConnect’ will be created for you within the folder you choose.

### Update Existing Installation

If you already have Pozi Connect v1.25 or above, you can easily update your application (or configuration for Groundtruth clients) by downloading the necessary files without re-installing the application.

#### Application

*Note: this requires the full installation of Pozi Connect before proceeding with the update.*

1. download the latest [Pozi Connect exe](https://dl.dropboxusercontent.com/u/401098/PoziConnect.exe) file (version 1.31)
2. save downloaded file into your `PoziConnect` folder, overwriting the existing file of the same name.

#### Configuration

Groundtruth maintains the configuration settings for its clients in an online repository. Groundtruth's clients can update their configuration to the latest version by following these steps.

*Note: if you have your own custom configuration (ie, you've written or modified INI or SQL files within the `PoziConnect\tasks` folder), the following process will zip up and archive any custom files. You'll need to manually restore these files or take steps beforehand and save them back into the updated `tasks` folder.*

1. close any applications (including Windows Explorer) that may be using or looking at files *inside* the `PoziConnect` application folder
2. download the latest [config zip file](https://github.com/groundtruth/PoziConnectConfig/archive/master.zip)
3. save the zip file into the `PoziConnect` application folder (don’t unzip it), and ensure the file name is **`PoziConnectConfig-master.zip`** (not any other variation like `PoziConnectConfig-master (1).zip`)
4. launch Pozi Connect - it will automatically extract the latest configuration files from the zip file

#### Running as a batch task

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

### Installation Troubleshooting

#### Pozi Connect fails to start.

Download and install the [Microsoft Visual C++ 2008 Redistributable Package (x86)](http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en), and try running Pozi Connect again.

#### Pozi Connect cannot connect to my DSN

You may need to set up your DSN with a 32 bit Windows driver. Run the 32 bit ODBC setup wizard (instead of the standard DSN wizard in the Control Panel). At the Windows Start menu, type in cmd, then at the command-line prompt, type or paste in the following, then hit 'Enter':

`C:\Windows\SysWOW64\odbcad32.exe`

Then set up a new DSN for property system, using the same settings as your existing one. It is recommended to use a different name for this 32 bit version. For example, if your existing DSN is called 'Proclaim', name it 'Proclaim32' or similar so it can be distinguished separately from the existing DSN.

Remember when you run PoziConnect, change the DSN name from Proclaim to Proclaim32.

#### Pozi Connect returns an error number 1073741512

Go into your `C:\Windows\System32` folder and see if there is a file called `libeay32.dll`. If so, rename it to `libeay32.bak`. Then try running Pozi Connect again.

(Rename the file back again when you’ve finished so that any other programs that may rely on it can use it.)

### Ready to Go

You're now ready to launch Pozi Connect.

Read on if you want to understand more and learn how to configure your own custom tasks.

---

## FAQ

### What user settings and permissions are required to install and run the application?

The Pozi Connect installation file is an exe file, which when run on any PC, will extract itself and create a folder called PoziConnect in a location of the user’s choosing. This ‘installation’ requires no administrator rights, and has no impact on the PC other than the creation of the PoziConnect folder and the application files within. No registry settings are changed, and the PoziConnect folder can be moved or deleted with no effect to the PC.

### How does Pozi Connect connect to my corporate database?

Pozi Connect uses your PC’s existing ODBC connection settings. It does not require any additional network or firewall configuration. It requires only that the user's PC has the appropriate DSN configured to access (read-only) the council's property database. Authentication can be based on a username/password or trusted connection (using Windows login name).

---

## Configuration

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

