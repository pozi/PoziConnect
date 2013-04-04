@echo off

SET BB_INCLUDE=%~dp0
REM Remove trailing backslash
SET BB_INCLUDE=%BB_INCLUDE:~0,-1%
ECHO BB_INCLUDE is %BB_INCLUDE% & echo.

SET OLD_CD=%CD%
REM CD %BB_INCLUDE%\release-1500-gdal-1-6-mapserver-5-6\
CD %BB_INCLUDE%\release-1310-gdal-1-6-mapserver-5-6\
REM CD %BB_INCLUDE%\release-1310-gdal-1-7-mapserver-5-6\
CALL SDKShell.bat setenv
CD %OLD_CD%

SET GDAL_DIR=%GDAL_DRIVER_PATH%\..
SET GDAL_APP_DIR=%GDAL_DIR%\apps

SET PYTHON_DIR=%BB_INCLUDE%\PortablePython_1.1_py2.6.1\App

PATH=%PYTHON_DIR%;%PYTHONPATH%;%PATH%
 
@echo on

