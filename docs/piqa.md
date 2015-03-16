# PIQA

Each year, Victoria's [Department of Environment, Land, Water & Planning](http://www.depi.vic.gov.au/) (DELWP) requires councils to supply it with an extract of property and address information from their internal property systems to be used for an annual Property Information Quality Audit (PIQA).

The process of extracting, filtering and formatting this data is time consuming and often overwhelming for councils, and can require the participation and co-operation of council staff members across GIS, Rates and IT departments.

[Pozi Connect](http://www.groundtruth.com.au/pozi-connect/) (formerly known as PlaceLab) is a tool developed by Groundtruth, with financial support of DELWP, that enables councils to quickly and accurately compile their property and address information into the required PIQA format.

## Instructions For PIQA Participants

When DELWP requests you to submit a PIQA extract for your council, follow these five easy steps:

1. Download the [Pozi Connect installer](https://github.com/groundtruth/PoziConnect/releases/latest). (If you have a previous installation of Pozi Connect, please remove it before proceeding by deleting your existing `PoziConnect` or `PlaceLab` folder.)
2. Run the installer, and when it prompts you, specify a folder location. You can choose anywhere; somewhere like `C:\Temp\` or the desktop will be sufficient.
3. Navigate to the newly-created PoziConnect folder location, and run PoziConnect.exe by double-clicking it.
4. From the Task drop-down list, select the item that relates to your council (eg, Alpine Shire Council would choose 'Alpine PIQA'). If you are prompted for a database username and/or password, enter them. You may have your own credentials that you can use, or you may use the database administrator credentials. Then click OK and wait for the application to run (it can take several minutes).
5. Check the `PoziConnect\output` folder (or you may have specified your own location in the settings) for a newly created 'PIQA Export.zip' file. This file contains two CSV spreadsheets that have been generated from the council’s property and address data. Email the zip file to your DELWP contact.

If you experience any difficulties such as the Pozi Connect failing to start, please download and install the [Microsoft Visual C++ 2008 Redistributable Package (x86)](http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en), and try running Pozi Connect again.

For any issues that are not solved by installing this patch, please contact Groundtruth.

## FAQ

### How does Pozi Connect connect to the property system?

Pozi Connect uses your PC’s existing ODBC connection settings. It does not require any additional network or firewall configuration.

### Does Pozi Connect extract any confidential information?

Pozi Connect only extracts the tables and fields from your property system that contains information relevant to the PIQA. You can check for yourself what information will be sent to DEPI by opening up the CSV files located in the “Output” folder in Excel.

### Does Pozi Connect make any changes to the property system?

Pozi Connect does not perform any update on your property database. It simply reads data from the database tables via the PC’s ODBC connection, similar to the Import function in Access, Excel or Crystal Reports.

### How does Pozi Connect work?

Pozi Connect extracts tables from your council’s property database and imports them into a temporary SQLite database file. It then performs a series of queries (customised for each council) on this file to generate PIQA-compliant CSV files that contain the council’s address and parcel information required for the PIQA audits. These two CSV files are automatically zipped up for you, ready for emailing to DEPI.

### What else is Pozi Connect capable of?

Pozi Connect has other tricks up its sleeve. It generates map layers from corporate databases (spatial and non-spatial), performs spatial data analysis, converts between data formats (Esri SHP, MapInfo TAB, DXF, KML, and others), loads data into spatial databases (SQL Server 2008, PostGIS, Oracle Spatial), and generally automates many of the tasks that GIS Administrators find themselves doing on a regular basis.

Most importantly, it can [automate your M1 workflow](http://www.groundtruth.com.au/pozi-connect-for-m1s).

Contact Groundtruth to find out how you can put Pozi Connect to work in your council’s GIS.