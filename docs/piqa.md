<img src="http://i.imgur.com/TLMFPUa.png" alt="Groundtruth" width="200">

# PIQA

Each year, Victoria's [Department of Environment, Land, Water & Planning][1] (DELWP) requires councils to supply it with an extract of property and address information from their internal property systems to be used for an annual Property Information Quality Audit (PIQA).

[1]: http://www.depi.vic.gov.au/

The process of extracting, filtering and formatting this data is time consuming and often overwhelming for councils, and can require the participation and co-operation of council staff members across GIS, Rates and IT departments.

[Pozi Connect][2] (formerly known as PlaceLab) is a tool developed by Groundtruth, with financial support of DELWP, that enables councils to quickly and accurately compile their property and address information into the required PIQA format.

[2]: /pozi-connect

## Instructions For PIQA Participants

When DEPI requests you to submit a PIQA extract for your council, follow these five easy steps:

1. Download the [Pozi Connect installer](https://dl.dropboxusercontent.com/u/401098/Pozi-Connect-Installer-1.30g.exe). (If you have a previous installation of Pozi Connect, please remove it before proceeding by deleting your existing Pozi Connect or PlaceLab folder.)
2. Run the installer, and when it prompts you, specify a folder location. You can choose anywhere; somewhere like `C:\Program Files\` or `C:\Temp\` or the desktop will be sufficient. A folder named ‘PoziConnect’ will be created for you within the folder you choose.
3. Navigate to the newly-created PoziConnect folder location, and run PoziConnect.exe by double-clicking it.
4. From the Task drop-down list, select the item that relates to your council (eg, Alpine Shire Council would choose ‘PIQA Export – Alpine’). If you are prompted for a database username and/or password, enter them. You may have your own credentials that you can use, or you may use the database administrator credentials. Then click OK and wait for the application to run (it can take several minutes).
5. Check the `PoziConnect\Output` folder (or you may have specified your own location in the settings) for a newly created “PIQA Export.zip” file. This file contains two CSV spreadsheets that have been generated from the council’s property and address data. Email the zip file to your DEPI contact.

If you experience any difficulties such as the Pozi Connect failing to start, please download and install the [Microsoft Visual C++ 2008 Redistributable Package (x86)][2], and try running Pozi Connect again.

[2]: http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en

For any issues that are not solved by installing this patch, please contact Groundtruth.