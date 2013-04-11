# PoziConnect

PoziConnect provides you with a simple interface for accessing, processing,
analysing and exporting your organisation's spatial and non-spatial data.


## Distribution and execution

PoziConnect can be executed from the Python source code, or it can be compiled
into a Windows binary. See below for the directory layout of a public release.

It can be executed in several modes:

* __Interactive mode__:
  is entered when PoziConnect launched without command-line parameters. It is
  used for running tasks ad hoc.
    
* __Silent mode__:
  entered when launched with the `--recipe` command-line paramater (see below)
  This is used to run multiple tasks unattended (i.e. nightly,
  scheduled processing).

### Release structure

- `app`: contains coding resources (developer-only area)
- `app/include`: contains the GDAL binaries and (and Python, on Windows)
- `recipes`: contains the recipes (text files listing successive tasks)
- `SQL`: contains SQL query files referenced by tasks
- `tasks`: contains the tasks INI files
- `PoziConnect.ini`: sets some environment variables
- `PoziConnect.bat`: wrapper to run from source on Windows
- `PoziConnect.sh`: wrapper to run from source on Mac/UNIX


## Running on Mac

GDAL should be installed with Postgres support, and is best done via
[homebrew](https://github.com/mxcl/homebrew):

    brew update && brew install gdal --with-postgres

After this, the output of `ogrinfo --formats` should include
`-> "PostgreSQL" (read/write)`.

Python libraries will need to be installed:

* definitely `pyodbc` (e.g. `sudo easy_install pyodbc`)
* maybe [`wxPython`](http://stackoverflow.com/questions/9205317/how-do-i-install-wxpython-on-mac-os-x)

Launch PoziConnect using the `PoziConnect.sh` bash script.


## Running on Windows

### Install GDAL binaries

Install [GDAL binaries](http://www.gisinternals.com/sdk/) into a subdirectory of
`PoziConnect\app\include`.

You may need to match the architecture of the binaries (32 or 64-bit) with that
of the operating system on which you will run PoziConnect. We have a tested
(32-bit) version saved here:
[release-1600-gdal-1-9-mapserver-6-2](https://s3.amazonaws.com/poziconnect/release-1600-gdal-1-9-mapserver-6-2.zip).

The `GDAL_BASE` variable in `PoziConnect.ini` must point to the GDAL `bin`
directory. For example:

    GDAL_BASE: app/include/release-1600-gdal-1-9-mapserver-6-2/bin

### Install Python

Install [Portable Python](http://www.portablepython.com/wiki/Download) into a
subdirectory of `PoziConnect\app\include`. This is the only Python that
PoziConnect will use - you don't need a system install of Python. We have a
tested version saved here:
[Portable Python 2.7.3.2](https://s3.amazonaws.com/poziconnect/PortablePython_2.7.3.2.exe).

Choose the following modules during installation:

* PyWin32
* Py2Exe
* wxPython
* PyODBC

Make sure that `PYTHON_DIR` is set correctly in
`PoziConnect\app\include\setenv_python.bat`. For example:

    SET PYTHON_DIR=%BB_INCLUDE%\Portable Python 2.7.3.2\App

### Run it

Launch `PoziConnect.bat` to run PoziConnect from the source code.


## Compiling on Windows

To compile PoziConnect into a Windows binary for public release, perform all of
the steps in the previous section, then run `PoziConnect\app\create_exe2.bat`.




* needed to copy...

        \app\include\Portable Python 2.7.3.2\App\msvc*90.dll
        \app\include\Portable Python 2.7.3.2\App\Microsoft.VC90.CRT.manifest

  into the directory where PoziExplorer.exe is going to be run from.






Producing a new version of the PoziConnect executable:

1.  code new features / fix bugs
2.  in a Windows environment, create the PoziConnect executable by running: `app/create_exe2.bat`
3.  the resulting PoziConnect.exe file is in: `app/dist`
4.  copy it to the `POZI_CONNECT_ROOT`

Changing the logo:

1.  transform the logo image file into a base64 string
2.  put that string in: app/lib/gui/PlaceLabBanner.py, in the imageBase64 variable (within triple double quotes)
3.  produce a new version of PoziConnect

Other notes and thoughts:

* Additional logging can be activated by setting the LOG level to DEBUG in logger.py script
* Sometimes, changes to the source code (.py) are not reflected in the corresponding compiled code (.pyc). Delete the .pyc files to force the interpreter/compiler recreates them.
* The work of renaming PlaceLab into PoziConnect in the entire codebase has not been undertaken (only visible bits have been renamed)


## Using recipes

Recipes are invoked using the `--recipe` flag eg:

    app/PlaceLab.py --recipe=recipes/example_01.txt

Where, `recipies/example_01.txt` is just a text file with a list of tasks
to run (ie. tasks found in the tasks directory).



Groundtruth &copy; 2009-2013
