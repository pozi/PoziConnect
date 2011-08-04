@ECHO OFF
SET ARGS=%*

CALL app\include\setenv_python.bat

CALL python app\PlaceLab.py %ARGS%



