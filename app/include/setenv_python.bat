@echo off

SET BB_INCLUDE=%~dp0
REM Remove trailing backslash
SET BB_INCLUDE=%BB_INCLUDE:~0,-1%
ECHO BB_INCLUDE is %BB_INCLUDE% & echo.

SET PYTHON_DIR=%BB_INCLUDE%\Portable Python 2.7.3.2\App

PATH=%PYTHON_DIR%;%PYTHONPATH%;%PATH%
 
@echo on

