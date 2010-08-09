call include\setenv_python.bat
python create_exe2.py py2exe

xcopy /s /y dist\PlaceLab.exe ..
REM xcopy /s /y ..\bb.ini ..\PlaceLab.ini

include\upx.exe ..\PlaceLab.exe

ECHO.
ECHO Process completed. 


SET /P cname=[Press ENTER to close window]
