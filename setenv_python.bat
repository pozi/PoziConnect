@echo off

SET ROOT_BACKSLASH=%~dp0
SET ROOT=%ROOT_BACKSLASH:~0,-1%
ECHO ROOT is %ROOT%

SET VENDOR=%ROOT%\vendor
ECHO VENDOR is %VENDOR%

SET PYTHON_DIR=%VENDOR%\Portable Python 2.7.3.2\App
ECHO PYTHON_DIR is %PYTHON_DIR%

PATH=%PYTHON_DIR%;%PATH%
ECHO PATH is %PATH%

REM Needed for OCI driver
CALL %VENDOR%\release-1911-gdal-3-1-4-mapserver-7-6-1\SDKShell.bat setenv

@echo on
