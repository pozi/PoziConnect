call include\setenv_python.bat
python create_exe2.py py2exe

xcopy /s /y dist\PoziConnect.exe ..
REM xcopy /s /y ..\bb.ini ..\PoziConnect.ini

include\upx.exe ..\PoziConnect.exe

ECHO.
ECHO Process completed. 


SET /P cname=[Press ENTER to close window]
