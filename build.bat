call app\include\setenv_python.bat
python app\build.py py2exe

xcopy /s /y app\dist\PoziConnect.exe .

ECHO Process completed. 

SET /P cname=[Press ENTER to close window]

