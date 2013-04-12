call setenv_python.bat

rmdir /S /Q build
rmdir /S /Q dist

python app\build.py py2exe

rmdir /S /Q build
del dist\w9xpopen.exe

copy "%PYTHON_DIR%\m*s*90*" dist

mkdir dist\vendor
for /f "delims=" %%a in ('dir vendor\*gdal* /B') do @set GDAL_NAME=%%a
xcopy /E "vendor\%GDAL_NAME%" dist\vendor\%GDAL_NAME%\

copy PoziConnect.ini dist\
xcopy /E tasks dist\tasks\
xcopy /E recipes dist\recipes\
mkdir dist\input
mkdir dist\output

