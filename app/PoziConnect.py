#!/usr/bin/env python
"""
PoziConnect provides you with a simple interface for accessing, processing, analysing and exporting your organisation's spatial and aspatial data.
"""

import logging
import logging.config
import optparse
import os
import string
import sys
import wx
import zipfile
import datetime

# Make modules from a virtualenv accessible if requested
if os.environ.get('POZICONNECT_ACTIVATE_THIS', False):
    execfile(os.environ['POZICONNECT_ACTIVATE_THIS'], dict(__file__=os.environ['POZICONNECT_ACTIVATE_THIS']))

# Make dirs available to the sys path
sys.path.extend(['app'])
sys.path.extend(['app/external'])

import iniparse

# Get version from version file
from PoziConnect.version import version

# Import our own modules
from PoziConnect.configparser import *
from PoziConnect.gui.gui import *
from PoziConnect.logger import *

# Create logger
LOGGER = Logger('main', 'output/PoziConnect.log')

def checkZipFile(folder):
    zipFileList = []
    # Scan the folder for a ZIP file
    for f in os.listdir(folder):
        if f.lower().endswith("zip"):
            zipFileList.append(os.path.join(folder,f))

    LOGGER.info("zipFileList", zipFileList)
    return zipFileList

# Helper function to zip an entire folder
# http://coreygoldberg.blogspot.com.au/2009/07/python-zip-directories-recursively.html
def zipper(dir, zip_file):
    zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(dir))
    for root, dirs, files in os.walk(dir):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            fullpath = os.path.join(root, f)
            archive_name = os.path.join(archive_root, f)
            print f
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

def cleanAndRemoveDir(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(folder)

###############################################
# Find all INI files in:
# - root dir
# - config dir
def findIniFiles(tasksDir,filterInclude,filterExclude):
    """
    Will find all .INI files in a provided directory and will return them as
    a list
    """
    fileList = []
    rootdir = '.'
    ext = '.ini'

    # Recurse through config directory to find INI files
    for root, subFolders, files in sorted(os.walk(tasksDir)):
        for f in files:
            for subst in filterInclude.split(","):
                # Filtering tasks (including only those that contain a site-specific name)
                if subst.lower().strip() in f.lower():
                    fileToExclude = False
                    for subst2 in filterExclude.split(","):
                        if subst2.lower().strip() in f.lower():
                            fileToExclude = True
                            break

                    # Filtering on file extension (including only .ini files)
                    if not fileToExclude:
                        if f.lower().endswith(ext):
                            fileList.append(os.path.join(root,f))

    return fileList


def showHeader(text):
    """
    Will provide a clearly distinguishable header as logging output
    """
    string = "#" * 60 + "\n#" + ' ' + text + "\n" + "#" * 60
    LOGGER.info(string)


def showGUI(taskList, options = {}):
    """
    Starts the application in GUI mode
    """
    LOGGER.info("Showing GUI")# , options)
    options['taskList'] = taskList
    app = GUI(options)
    app.Show()

def processTasks(taskList):
    """
    Loops through a list of tasks and executes them.
    This function will be called when the application
    runs in batch mode (no GUI).
    """
    for taskName, taskFile in taskList:
        options = {
            'taskName': taskName,
            'configFile': taskFile,
        }
        p = TaskManager(options)
        p.Execute()


def init():
    """
    Initialises the application. It does all sorts of magic to
    figure out where in the file system it resides and whether or
    it is run as a Windows executable or not.
    """

    # Test whether we are an executable (py2exe)
    isExe = hasattr(sys, "frozen")

    # Now determine the name of 'ourselves'. Based on that
    # we determine the root path of the application
    scriptPath = ''
    if isExe:
        scriptPath = sys.argv[0]
    else:
        try:
            scriptPath = __file__
        except Exception as e:
            scriptPath = '.'

    scriptPath = os.path.realpath(scriptPath)
    scriptDir = os.path.dirname(scriptPath)
    scriptName = os.path.basename(scriptPath)
    scriptBaseName = scriptName.rstrip('.py').rstrip('.exe')
    rootDir = appDir = ''

    # We assume that the EXE is always in the root of
    # the project. The python script is always in the 'app'
    # dir. Based on whether it is an exe or not we set
    # the appDir and rootDir variables
    if isExe:
        appDir = scriptDir + os.path.sep + 'app'
        rootDir = scriptDir
    else:
        appDir = scriptDir
        rootDir = os.path.realpath(scriptDir + os.path.sep + '..')

    tasksDir = rootDir + os.path.sep + 'tasks'
    logDir = rootDir + os.path.sep + 'output'
    backupDir = rootDir + os.path.sep + 'backup'

    appConfigFile = rootDir + os.path.sep + scriptBaseName + '.ini'
    siteConfigFile = rootDir + os.path.sep + scriptBaseName + '.site.ini'

    appConfigOptions = {
        'logger': LOGGER,
        'globalSections': ['Settings', 'Application Settings']
    }
    appConfig = ConfigParser(appConfigOptions)
    #LOGGER.info("CONFIG FILE", appConfigFile)
    if os.path.isfile(appConfigFile):
        appConfig.read(appConfigFile)
        #appConfig.SubstituteVariablesFromSection('Settings')
        for section in appConfig.sections():
            LOGGER.debug("SECTION:", section)
            items = appConfig.items(section)
            LOGGER.debug(items)

        if appConfig.has_section('ENV'):
            env = os.environ
            envItems = appConfig.items('ENV')
            for key, value in envItems:
                value = str(value) # force value to be a string
                if key.lower() == 'path':
                   envpath = env.get('PATH', '')
                   env[key] = os.pathsep.join(value.split(';') + envpath.split(os.pathsep))
                   LOGGER.debug("prepending to %s: %s" % (key, value))
                else:
                   env[key] = value
                   LOGGER.debug("setting: %s to %s" % (key, value))

        if appConfig.has_section('POSIX') and os.name == 'posix':
            for key, value in appConfig.items('POSIX'):
               if key.lower() == 'unsetgdal_data' and value == True: # 'YES' becomes True
                  del os.environ['GDAL_DATA']
                  LOGGER.info("Unset environment variable GDAL_DATA")

    else:
        LOGGER.warn('Application config file could not be found! (%s)' % appConfigFile)

    siteConfigOptions = {
        'logger': LOGGER,
        'globalSections': ['Settings']
    }
    siteConfig = ConfigParser(siteConfigOptions)
    if os.path.isfile(siteConfigFile):
        siteConfig.read(siteConfigFile)
        #appConfig.SubstituteVariablesFromSection('Settings')
        for section in siteConfig.sections():
            LOGGER.debug("SECTION:", section)
            items = siteConfig.items(section)
            LOGGER.debug(items)
    else:
        LOGGER.warn('Site specific config file could not be found! (%s)' % siteConfigFile)

    appSettings = {}
    try:
        appSettings = dict(appConfig.items('Application Settings'))
        appSettings.update(dict(siteConfig.items('Settings')))
    except Exception as e:
        LOGGER.warn('Error:', e)

    # Log some information
    LOGGER.info("PoziConnect version:", version)
    LOGGER.info("isExe", isExe)
    LOGGER.info("scriptPath", scriptPath)
    LOGGER.info("scriptName", scriptName)
    LOGGER.info("scriptBaseName", scriptBaseName)
    LOGGER.info("scriptDir", scriptDir)
    LOGGER.info("rootDir", rootDir)
    LOGGER.info("backupDir", backupDir)
    LOGGER.info("logDir", logDir)
    LOGGER.info("confFile", appConfigFile)

    taskIncludeFilter = ''
    taskExcludeFilter = 'Hopefully this string is not contained in any filename!'
    if os.path.isfile(siteConfigFile):
        LOGGER.info("siteConfFile", siteConfigFile)
        LOGGER.info("siteConfig", siteConfig)
        for a,b in siteConfig.items('Settings'):
            if a.lower()=="include" and len(b.strip()):
                taskIncludeFilter = b
                LOGGER.info("Including tasks containing (any of): ",taskIncludeFilter)
            if a.lower()=="exclude" and len(b.strip()):
                taskExcludeFilter = b
                LOGGER.info("Excluding tasks containing (any of): ",taskExcludeFilter)

    LOGGER.info("CWD", os.getcwd())
    """
    LOGGER.info("sys.path", sys.path)
    extra = os.environ.get('USERNAME')
    if extra:
        sys.path.extend(extra.split(os.pathsep))
    LOGGER.info("sys.path", sys.path)

    LOGGER.info("-------------------")
    LOGGER.info("frozen", repr(getattr(sys, "frozen", None)))
    LOGGER.info("sys.executable", sys.executable)
    LOGGER.info("sys.prefix", sys.prefix)
    LOGGER.info("sys.argv", sys.argv)
    LOGGER.info("-------------------")

    env = os.environ.copy()
    LOGGER.info("PATH", env.get('PATH'), '\n')
    """

    #LOGGER.info("ENVIRONMENT:")
    #for e in env:
        #LOGGER.info("%s: %s" % (e, env[e]))


    # Name of the Settings section in the ini file
    settingsSectionName = 'Settings'

    ###############################################################
    # Process command line options and arguments
    usage = "usage: %prog [options] path/to/ini-file"
    parser = optparse.OptionParser(usage)
    #parser.add_option("-a", "--auto", action="store_true", default=False,
    #                  help="run only ini files that are marked with 'auto'", metavar="auto")
    parser.add_option("-r", "--recipe", dest="recipe_filename", default=False,
                      help="run the tasks in the RECIPE_FILE", metavar="RECIPE_FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    # Don't use GUI if 'recipe' is set
    options.useGui = not options.recipe_filename

    #if len(args) < 1:
        #parser.error("please provide an ini file as argument")
        #useGui = True

    #iniFile = args[0]

    LOGGER.info("ARGS", options.useGui, args)

    # USED HARDCODED IN OGR.py
    # TODO: don't hardcode

    #gdalAppDir = rootDir + '/app/include/release-1310-gdal-1-6-mapserver-5-6/bin/gdal/apps'

    #os.chdir(scriptHome)

    # If exists a zip file in the directory, we prompt the user for upgrade

    # Check for a ZIP file
    zipFileList = []
    zipFileList = checkZipFile(rootDir)
    if zipFileList:
        # Creates a mini-app, with a 0-sized frame, just to support a basic dialog
        app = wx.App(False)
        frame = wx.Frame(None, wx.ID_ANY, "", size=(0,0))

        dlg = wx.MessageDialog(frame,
            "There is a ZIP file in PoziConnect folder: "+str(zipFileList)+". Are you sure you want to update your tasks?",
            "Update confirmation", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()

        # Destroying both the modal and its supporting frame
        dlg.Destroy()
        frame.Destroy()

        # Processing the OK button, continuing unabatted otherwise
        if result == wx.ID_OK:
            LOGGER.info('Starting task upgrade ...')
            # Perform backup of tasks
            if not os.path.isdir(backupDir):
                # Create the directory then!
                os.makedirs(backupDir)

            # Build a new ZIP file of all the tasks from the task dir
            try:
                zipped_tasks = zipper(tasksDir,backupDir+os.path.sep+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-tasks.zip')
            except:
                LOGGER.info('Not able to zip the tasks folder ...')

            # Deleting the content of the tasks folder
            try:
                cleanAndRemoveDir(tasksDir)
            except:
                LOGGER.info('Not able to delete the tasks file ...')

            # Expanding the ZIP file into the tasks directory
            try:
                # There should only ever be one (and only one) ZIP file
                for zf in zipFileList:
                    with zipfile.ZipFile(zf, "r") as z:
                        # Extract all files at the rootDir
                        z.extractall(rootDir)

                        # Getting the repository mapping
                        if appConfig.has_section('UPDATES'):
                            for key,value in appConfig.items('UPDATES'):
                                if key.lower() == 'repository':
                                    # Assumption1: ZIP at the root of the app
                                    # Assumption2: master branch has been downloaded, and suffixes the repository name
                                    zippedDirName = rootDir+os.path.sep+value+'-master'
                                    LOGGER.info('Renaming from: '+zippedDirName)
                                    LOGGER.info('Renaming to  : '+tasksDir)
                                    # Rename the extracted folder to tasks
                                    os.rename(zippedDirName,tasksDir)

            except:
                LOGGER.info('Not able to unzip the zip file into a tasks folder ...')

            # Removing the ZIP file
            try:
                for zf in zipFileList:
                    os.remove(zf)
            except:
                LOGGER.info('Not able to delete the zip file ...')

    # Now that the tasks have potentially be updated, we continue with loading the (new) filenames
    fileList = []
    if options.recipe_filename:
        print tasksDir
        # The recipe file will provide the list of ini files that will create tasks
        fileList = map(lambda x: os.path.join(tasksDir, string.strip(x)), open(options.recipe_filename).readlines())
    else:
        # Take file list from arguments if provided
        fileList = args if (len(args) > 0) else findIniFiles(tasksDir,taskIncludeFilter,taskExcludeFilter)

    ###############################################
    # Now create a list of tasks based on the ini
    # files found. Then sort it alphabetically
    taskList = []
    for f in fileList:
        taskName = os.path.splitext(os.path.basename(f))[0]
        taskList.append((taskName, f))
    taskList.sort()

    return options, appConfig, taskList

if __name__ == "__main__":
    options, appConfig, taskList = init()
    if options.useGui:
        options = dict(appConfig.items('GUI')) if appConfig.has_section('GUI') else {}
        showGUI(taskList, options)
    else:
        processTasks(taskList)

