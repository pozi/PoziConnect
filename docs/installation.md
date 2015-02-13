<img src="http://i.imgur.com/TLMFPUa.png" alt="Groundtruth" width="200">

# Pozi Connect Installation

Latest version:
https://dl.dropboxusercontent.com/u/401098/PoziConnect-1.31.31.msi

Pozi Connect is now distributed as a Windows installer package. It updates the necessary program and configuration files without affecting the council’s data and M1 files. However, as a precaution, please make a backup of your existing PoziConnect folder before running this installer for the first time.

When you run the installer, it will prompt you for a path. Please change it from the default path of C:\PoziConnect to the existing PoziConnect folder on your network.

The new version organises the various output files as follows:

M1 Files: PoziConnect\output\M1
Audit Files: PoziConnect\output\Audits
Statistics Files: PoziConnect\output\Statistics
Spatial Files: PoziConnect\output\Spatial

The new audits are documented here:
https://github.com/groundtruth/PoziConnectConfig/blob/master/~Shared/Docs/Audits.md


## FAQ

#### What user settings and permissions are required to install and run the application?

The Pozi Connect installation file is an exe file, which when run on any PC, will extract itself and create a folder called PoziConnect in a location of the user’s choosing. This ‘installation’ requires no administrator rights, and has no impact on the PC other than the creation of the PoziConnect folder and the application files within. No registry settings are changed, and the PoziConnect folder can be moved or deleted with no effect to the PC.

#### How does Pozi Connect connect to my corporate database?

Pozi Connect uses your PC’s existing ODBC connection settings. It does not require any additional network or firewall configuration. It requires only that the user’s PC has the appropriate DSN configured to access (read-only) the council’s property database. Authentication can be based on a username/password or trusted connection (using Windows login name).
