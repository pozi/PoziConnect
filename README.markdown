# PoziConnect

Overview
--------
PoziConnect provides you with a simple interface for accessing, processing,
analysing and exporting your organisation's spatial and aspatial data.

Execution
---------
PoziConnect can be run in multiple modes:
* Interactive / silent
- Interactive: just launching the executable (or the Python script)
- Silent: with a batch wrapper using the --recipe flag (see below)
* Development / production
- Development: Python script launched from a wrapper
- Production: Windows executable

Directory structure
-------------------
PoziConnect.ini: sets some environment variables for the executable/Python script
PoziConnect.bat (or PoziConnect.sh): batch wrapper
PoziConnect.exe: Windows executable
app: coding resources (developer only area)
app/include: contains the GDAL binaries (see below)
recipes: contains the recipes (text files listing successive tasks)
SQL: contains SQL query files referenced by tasks
tasks: contains the tasks INI files

GDAL binaries
-------------
Both development and production environments require downloading the GDAL binaries.
The version of the binaries has to match the operating system where PoziConnect will be executed.
The binaries are available from:
http://www.gisinternals.com/sdk/

Recipes
-------
Recipes are invoked using the --recipe flag eg:

    app/PlaceLab.py --recipe=recipes/example_01.txt

Where, `recipies/example_01.txt` is just a text file with a list of tasks
to run (ie. tasks found in the tasks directory).

For developers
--------------
Additional logging can be activated by setting the LOG level to DEBUG in logger.py script


Groundtruth 2009-2013

