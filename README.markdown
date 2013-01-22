# PoziConnect

Overview
--------
PoziConnect provides you with a simple interface for accessing, processing, analysing and exporting your organisation's spatial and aspatial data.


Execution
---------
PoziConnect can be run in multiple modes:
* Interactive / silent
    * Interactive: just launching the executable (or the Python script)
    This is used for running tasks ad hoc.
    * Silent: with a batch wrapper using the --recipe flag (see below)
    This is used to run multiple tasks in an unsupervised manner (i.e. nightly, scheduled processing).
* Development / production
    * Development: Python script launched from a wrapper
    Does this require a version of Python on the development machine? TBC (what about the embedded, portable python?)
    * Production: Windows executable
    This executable, and the following file/directory structure, constitute a public release.


Files and directory structure
-----------------------------
- app: contains coding resources (developer-only area)
- app/include: contains the GDAL binaries (see below)
- recipes: contains the recipes (text files listing successive tasks)
- SQL: contains SQL query files referenced by tasks
- tasks: contains the tasks INI files
- PoziConnect.ini: sets some environment variables for the executable/Python script
- PoziConnect.bat (or PoziConnect.sh): batch wrapper
- PoziConnect.exe: Windows executable


GDAL binaries
-------------
Both development and production environments require downloading the GDAL binaries.
The version of the binaries (32 or 64 bits) has to match the operating system where PoziConnect will be executed.

The binaries are available from:
    http://www.gisinternals.com/sdk/

The binaries should be placed in app/include within a directory that reflects the binaries version, e.g:
    POZI_CONNECT_ROOT\app\include\release-1600-x64-gdal-1-9-mapserver-6-0

In PoziConnect.ini, the variable GDAL_BASE must point to the bin directory within, e.g.:
    GDAL_BASE: app/include/release-1600-x64-gdal-1-9-mapserver-6-0/bin


Recipes
-------
Recipes are invoked using the --recipe flag eg:

    app/PlaceLab.py --recipe=recipes/example_01.txt

Where, `recipies/example_01.txt` is just a text file with a list of tasks
to run (ie. tasks found in the tasks directory).


For developers
--------------
Producing a new version of the PoziConnect executable:

1.  code new features / fix bugs
2.  in a Windows environment, create the PoziConnect executable by running: app/create_exe2.bat
3.  the resulting PoziConnect.exe file is in: app/dist 
4.  copy it to the POZI_CONNECT_ROOT

Changing the logo:

1.  transform the logo image file into a base64 string
2.  put that string in: app/lib/gui/PlaceLabBanner.py, in the imageBase64 variable (within triple double quotes)
3.  produce a new version of PoziConnect

Other notes and thoughts:

+ Additional logging can be activated by setting the LOG level to DEBUG in logger.py script
+ Sometimes, changes to the source code (.py) are not reflected in the corresponding compiled code (.pyc). Delete the .pyc files to force the interpreter/compiler recreates them.
+ The work of renaming PlaceLab into PoziConnect in the entire codebase has not been undertaken (only visible bits have been renamed)

Groundtruth &copy; 2009-2013

