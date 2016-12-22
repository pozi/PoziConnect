@ECHO OFF
SET ARGS=%*
REM Setup environment
CALL setenv_python.bat
REM Build application logo
python app\PoziConnect\gui\gui_logo_build.py %~dp0\app\PoziConnect\gui\gui_logo.png
REM Start Application
CALL python app\PoziConnect.py %ARGS%

