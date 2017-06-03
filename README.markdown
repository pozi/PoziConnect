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

Make sure that `PYTHON_DIR` in `setenv_python.bat` correctly points to the
Python `App` directory. For example:

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

#### Customising Logo:

Logos are compiled when the application is built using build.bat. To update
a logo, simply edit/replace the file at app\PoziConnect\gui\gui_logo.png

#### Program Icon

To create an icon file, upload a 48x48 png to http://convertico.com/ and download the ico file it generates to `app\PoziConnect\gui`.

After the build process, the `PoziConnect.exe` will not display the program icon on all systems. Follow instructions at https://command-tab.com/2008/07/21/how-to-combine-ico-files-into-a-windows-exe/ to manually add the icon to the exe.

#### Other notes:

* Additional logging can be activated by setting the log level in `logger.py`
* Sometimes, changes to the source code (`*.py`) are not correctly reflected in
  the corresponding compiled code (`*.pyc`). Delete the `*.pyc` files to force their
  regeneration.


## Running on Mac/UNIX

It is good practice to use `virtualenv` to isolate Python dependencies
(as described [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/)),
and `pip` to install those dependencies. However, in the case of PoziConnect
this is complicated by two issues.

### Special dependencies

**Firstly**, PoziConnect depends on two things that are better installed as
operating system packages: `GDAL` and `wxPython`.

When `GDAL` is installed with its Python components, it provides Python
langugage bindings, but also many extra command line tools. PoziConnect
uses GDAL via the command line (not via Python bindings). Install it
on Mac using [homebrew](https://github.com/mxcl/homebrew):

    brew update && brew install gdal --with-postgres --with-postgresql

After this, the output of `ogrinfo --formats` should include
`-> "PostgreSQL" (read/write)`.

The `wxPython` module integrates with operating system GUI components
and is generally not installed via `pip`. Install it on Mac as described
[here](http://stackoverflow.com/questions/9205317/how-do-i-install-wxpython-on-mac-os-x),
with:

    brew update && brew install wxmac

The `requirements.txt` file records module versions known to work together.

The remaining, normal python module dependency is `pyodbc`. At this point you
can [create a virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/),
then install the recommended `pyodbc` into it:

    pip install `grep pyodbc requirements.txt`

The output of `pip freeze` should now be very similar to `requirements.txt`.

### Virtualenv ain't framework

**Secondly**, as you will see if you attempt to run PoziConnect from within the
virtualenv, `wxPython` needs to be run from a framework build of Python in
order to access the screen. The Python in the virtualenv is not a proper
framework Python (even when created from your system's famework Python).
This issue is discussed [in the `wxPython` documentation](http://wiki.wxpython.org/wxPythonVirtualenvOnMac).

The solution is to run PoziConnect from your system Python, but give it access
to the modules in the virtualenv. This access can be set up after Python is
started, as described [in the virtualenv documentation](http://www.virtualenv.org/en/latest/#using-virtualenv-without-bin-python).

If the environment variable `POZICONNECT_ACTIVATE_THIS` is set to the full
path of a `bin/activate_this.py` file in a virtualenv, PoziConnect will perform
`execfile` on it to gain access to that virtualenv's modules.

You can set the `POZICONNECT_ACTIVATE_THIS` variable using a tool like
[autoenv](https://github.com/kennethreitz/autoenv).

### Run it

With this done, run `deactivate` to leave your virtualenv and return to
your system's Python, then launch PoziConnect using the `PoziConnect.sh` bash
script.

### Working with PoziConnectConfig

The Pozi Connect tasks that Groundtruth maintains for its clients are kept in a separate repository. To test Pozi Connect with the available tasks, set up a symlink so that Pozi Connect can read the tasks from the PoziConnectConfig repository.

```
mklink /D C:\Users\Simon\GitHub\PoziConnect\tasks C:\Users\Simon\GitHub\PoziConnectConfig
```

Any data files that Pozi Connect expects to find in the output folder can also be linked.

```
mklink /D C:\Users\Simon\GitHub\PoziConnect\output C:\Data\_PoziConnect
```

### Other notes

* Running with setuptools 0.7.5 installed triggered the error
  `AttributeError: ResourceManager instance has no attribute '_warn_unsafe_extraction'`.
  Upgrading to setuptools 1.1 fixed the problem. Check your version of setuptools
  with `which easy_install | xargs cat`.


## Modes of execution

PoziConnect can be executed in several modes:

* __Interactive mode__:
  is entered when PoziConnect is launched without command-line parameters.
  It is used for running tasks ad hoc.

* __Silent mode__:
  is entered when PoziConnect launched with the `--recipe` command-line
  paramater (see below). This is used to run multiple tasks unattended
  (i.e. nightly, scheduled processing).


## Layout

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

Groundtruth &copy; 2009-2017
