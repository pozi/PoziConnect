call setenv_python.bat
REM Cleanup
rmdir /S /Q build
rmdir /S /Q dist
REM Build application logo
python app\PoziConnect\gui\gui_logo_build.py %~dp0\app\PoziConnect\gui\gui_logo.png

REM Convert to exe
python app\build.py py2exe

rmdir /S /Q build
del dist\w9xpopen.exe

copy "%PYTHON_DIR%\m*s*90*" dist

mkdir dist\vendor
for /f "delims=" %%a in ('dir vendor\*gdal* /B') do @set GDAL_NAME=%%a
xcopy /E "vendor\%GDAL_NAME%" dist\vendor\%GDAL_NAME%\

@rem the following line is to resolve the "Errno -1073741512" issue
copy "dist\vendor\%GDAL_NAME%\bin\libeay32.dll" "dist\vendor\%GDAL_NAME%\bin\gdal\apps\libeay32.dll"

copy PoziConnect.ini dist\
xcopy /E tasks dist\tasks\
xcopy /E recipes dist\recipes\
xcopy /E docs dist\docs\
mkdir dist\output
copy post-install.bat dist\

set /P cname=[Press ENTER to close window]

