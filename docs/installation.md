# Pozi Connect Installation

Latest version:
https://github.com/groundtruth/PoziConnect/releases/latest

Pozi Connect is now distributed as a Windows installer package. It is designed to update the necessary application and configuration files without affecting the associated data (such as M1 files). However, before running this installer for the first time, please make a backup of your existing PoziConnect folder.

When you run the installer, it will prompt you for a path. Please change it from the default path of C:\PoziConnect to the existing PoziConnect folder on your network.

The new version organises the various output files as follows:

```
M1 Files: PoziConnect\output\M1
Audit Files: PoziConnect\output\Audits
Statistics Files: PoziConnect\output\Statistics
Spatial Files: PoziConnect\output\Spatial
```

The new audits are documented here:
http://groundtruth.viewdocs.io/poziconnect/m1s/audits


## Subscribe

https://github.com/groundtruth/PoziConnect/subscription

## FAQ

#### How does Pozi Connect connect to my corporate database?

Pozi Connect uses your PC’s existing ODBC connection settings. It does not require any additional network or firewall configuration. It requires only that the user’s PC has the appropriate DSN configured to access (read-only) the council’s property database. Authentication can be based on a username/password or trusted connection (using Windows login name).

## Troubleshooting

### Pozi Connect fails to start

Download and install the [Microsoft Visual C++ 2008 Redistributable Package (x86)](http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en), and try running Pozi Connect again.

### Cannot connect to data source

*In this example, we'll assume that we're trying to connect to a DSN called 'pthprod'.*

Run the 32 bit ODBC setup wizard (instead of the standard DSN wizard in the Control Panel). At the Windows Start menu, type in cmd, then at the command-line prompt, type or paste in the following, then hit 'Enter':

`C:\Windows\SysWOW64\odbcad32.exe`

In the System DSN tab, check if there is a data source for 'pthprod'. If not, add a new DSN, using the same settings as your existing 64 bit one. It is recommended to use a different name for the new 32 bit DSN. For example, name it 'pthprod32' or similar so it can be distinguished from the existing DSN.

Open the Pozi Connect config file in a text editor and update the DSN name:

```
Pathway_DSN: pthprod32
```
