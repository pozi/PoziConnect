# PoziConnect

PoziConnect provides you with a simple interface for accessing, processing,
analysing and exporting your organisation's spatial and non-spatial data.

It can be executed from the Python source code, or it can be compiled into
a Windows binary release.


## Running on Windows

### Install Python

Install [Portable Python](http://www.portablepython.com/wiki/Download) into a
subdirectory of `vendor`. This is the only Python that PoziConnect will use -
you don't need a system install of Python. We have a tested version saved here:
[Portable Python 2.7.3.2](https://s3.amazonaws.com/poziconnect/PortablePython_2.7.3.2.exe).

Choose the following modules during installation:

* PyWin32
* Py2Exe
* wxPython
* PyODBC

Make sure that `PYTHON_DIR` is set correctly in `setenv_python.bat`. For example:

    SET PYTHON_DIR=%VENDOR%\Portable Python 2.7.3.2\App

### Install GDAL binaries

Install [GDAL binaries](http://www.gisinternals.com/sdk/) into a subdirectory of
`vendor`.

You may need to match the architecture of the binaries (32 or 64-bit) with that
of the operating system on which you will run PoziConnect. We have a tested
(32-bit) version saved here:
[release-1600-gdal-1-9-mapserver-6-2](https://s3.amazonaws.com/poziconnect/release-1600-gdal-1-9-mapserver-6-2.zip).

The `GDAL_BASE` variable in `PoziConnect.ini` must point to the GDAL `bin`
directory. For example:

    GDAL_BASE: vendor\release-1600-gdal-1-9-mapserver-6-2\bin

### Run it

Launch `PoziConnect.bat` to run PoziConnect from the source code.


## Compiling on Windows

To compile PoziConnect into a Windows binary for public release, perform the
steps in the previous section, then run `build.bat`.

A full release of PoziConnect will be output to the `dist` directory. It should
contain `PoziConnect.exe`, additional DLLs, GDAL (from `vendor\*gdal*`), and
runtime directories and configuration taken from the top level of this repository.

#### To build with an alternate logo:

1.  Transform the desired image file into a base64 string.
2.  Put that string in: `app/PoziConnect/gui/PlaceLabBanner.py`,
    in the imageBase64 variable (within triple double quotes).
3.  Perform the build as usual.

#### Other notes:

* Additional logging can be activated by setting the log level in `logger.py`
* Sometimes, changes to the source code (`*.py`) are not correctly reflected in
  the corresponding compiled code (`*.pyc`). Delete the `*.pyc` files to force their
  regeneration.

  
## Running on Mac/UNIX

GDAL should be installed with Postgres support. On Mac, this is best done via
[homebrew](https://github.com/mxcl/homebrew):

    brew update && brew install gdal --with-postgres

After this, the output of `ogrinfo --formats` should include
`-> "PostgreSQL" (read/write)`.

Python libraries will need to be installed:

* Definitely `pyodbc` (e.g. `sudo easy_install pyodbc`)
* Maybe [`wxPython`](http://stackoverflow.com/questions/9205317/how-do-i-install-wxpython-on-mac-os-x)

Launch PoziConnect using the `PoziConnect.sh` bash script.


## Modes of execution

PoziConnect can be executed in several modes:

* __Interactive mode__:
  is entered when PoziConnect is launched without command-line parameters.
  It is used for running tasks ad hoc.
    
* __Silent mode__:
  is entered when PoziConnect launched with the `--recipe` command-line
  paramater (see below). This is used to run multiple tasks unattended
  (i.e. nightly, scheduled processing).


### Layout

- `app`: source code of the PoziConnect application
- `vendor`: place external dependencies here for Windows (Python, GDAL)
- `tasks`: contains the task INI files
- `recipes`: contains recipes (text files listing successive tasks)
- `PoziConnect.ini`: sets some environment variables
- `PoziConnect.bat`: a wrapper to run from source on Windows
- `PoziConnect.sh`: a wrapper to run from source on Mac/UNIX


## Using recipes

Recipes are executed using the `--recipe` flag, for example:

    PoziConnect.bat --recipe=recipes/example_01.txt

Where `recipies/example_01.txt` is a text file with a list of tasks to run
(tasks are found in the `tasks` directory).


## TODO

* Finish renaming PlaceLab to PoziConnect in the entire codebase.


## Copyright

Groundtruth &copy; 2009-2013
