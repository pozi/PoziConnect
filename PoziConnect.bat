@ECHO OFF
SET ARGS=%*

CALL app\include\setenv_python.bat

CALL python app\PoziConnect.py %ARGS%



