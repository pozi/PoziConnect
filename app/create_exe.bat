call include\setenv_python.bat
python create_exe.py py2exe

xcopy /s /y dist\* ..\app2\