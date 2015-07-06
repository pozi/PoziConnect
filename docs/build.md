resolve the "Errno -1073741512" error by copying the libeay32.dll file from `PoziConnect\vendor\release-xxxx-gdal-x-xx-mapserver-x-x\bin\` to `PoziConnect\vendor\release-xxxx-gdal-x-xx-mapserver-x-x\bin\gdal\apps\`

## New Release

A Pozi Connect 'release' consists of files from multiple sources, including

* PoziConnect GitHub repo
* PoziConnectConfig GitHub repo

To create a new release:

* commit and sync changes in PoziConnectConfig
* make at least one edit in PoziConnect repo (eg, update `docs\m1\history.md`), then commit and sync (this forces GitHub Releases to recognise that something has changed since the last release)
* update PoziConnectConfig (`PoziConnect\tasks`)
  * open C:\Temp\PoziConnect\PoziConnect.exe (this is a separate installation of the application, and not linked to the development version)
  * click on dot to download latest PoziConnectConfig zip
  * close PoziConnect, reopen PoziConnect, proceed with update
  * close PoziConnect
  * delete `PoziConnect\backup` folder
  * delete `PoziConnect\output\PoziConnect.log` file
* update `PoziConnect\docs` by copying files from development version of Pozi Connect
* launch Advanced Installer
* update version number (and when given the option, choose new version, not update)
* build new version - new msi file is created in C:\Temp\
* go to https://github.com/groundtruth/PoziConnect/releases, and create new release
* update
  * tag (eg v1.32.14)
  * release name (eg Release 1.32.14)
  * upload new msi
  * notes (use previous releases as examples of what to write)
* publish
* notify relevant users to download from https://github.com/groundtruth/PoziConnect/releases/latest