@echo off

@rem This is a sample file. It should be maintained in the M1 repo. 
@rem A batch file called post-install.bat gets run after the files have been extracted.
@rem This gives the M1 maintainer an oppertunity to run some commands after the zip file has been extracted.

@echo M1PostInstall starting

@echo M1PostInstall: Setting folder and file permissions for %~dp0output and %~dp0tasks
@rem *S-1-1-0 === Everyone

if not exist "%~dp0output" (
  mkdir "%~dp0output"
)

@icacls "%~dp0output" /t /grant "*S-1-1-0":(OI)(CI)F /q
@icacls "%~dp0tasks" /t /grant "*S-1-1-0":(OI)(CI)F /q

@echo M1PostInstall: Adding desktop shortcut for PoziConnect.exe

@if "%public%"=="" (
  @echo Cannot find valid userprofile to save PoziConnect.exe shortcut.
  goto skipMkLink
)

@if exist "%public%\Desktop\Pozi Connect.lnk" (
  @echo PoziConnect.exe shortcut already created.
  goto skipMkLink
)

@rem @mklink "%public%\Desktop\Pozi Connect" "%~dp0PoziConnect.exe"

cd "%~dp0"
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%public%\Desktop\Pozi Connect.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%~dp0PoziConnect.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Description = "Pozi Connect" >> CreateShortcut.vbs
echo oLink.IconLocation = "%~dp0PoziConnect.exe" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

:skipMkLink

@echo M1PostInstall finished

:end