@ECHO OFF

REM Needed for OCI driver
CALL vendor\release-1600-gdal-1-9-mapserver-6-2\SDKShell.bat setenv

CALL PoziConnect.exe

@ECHO ON