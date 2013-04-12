@ECHO OFF
SET ARGS=%*

CALL setenv_python.bat
CALL python app\PoziConnect.py %ARGS%

