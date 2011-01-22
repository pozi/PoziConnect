#!/usr/bin/env python
"""
PlaceLab provides you with a simple interface for accessing, processing, analysing and exporting your organisation's spatial and aspatial data.
"""

import iniparse
import logging
import logging.config
import optparse
import os
import string
import sys

# Get version from version file
from version import version

# Import our own modules
from lib.configparser import *
from lib.gui.gui import * 
from lib.logger import *

# Create logger
LOGGER = Logger('main', 'output/PlaceLab.log')

###############################################
# Find all INI files in:
# - root dir
# - config dir
def findIniFiles(tasksDir):
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
    # Make app dir available to the sys path
    sys.path.extend(['app'])

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

    appConfigFile = rootDir + os.path.sep + scriptBaseName + '.ini'

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
    else:
        LOGGER.warn('Application config file could not be found! (%s)' % appConfigFile)

    appSettings = {}
    try:
        appSettings = dict(appConfig.items('Application Settings'))
    except Exception as e: 
        LOGGER.warn('Error:', e)

    # Log some information
    LOGGER.info("PlaceLab version:", version)
    LOGGER.info("isExe", isExe)
    LOGGER.info("scriptPath", scriptPath)
    LOGGER.info("scriptName", scriptName)
    LOGGER.info("scriptBaseName", scriptBaseName)
    LOGGER.info("scriptDir", scriptDir)
    LOGGER.info("rootDir", rootDir)
    LOGGER.info("logDir", logDir)
    LOGGER.info("confFile", appConfigFile)
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

    gdalAppDir = rootDir + '/app/include/release-1310-gdal-1-6-mapserver-5-6/bin/gdal/apps'

    #os.chdir(scriptHome)

    fileList = []
    if options.recipe_filename:
        print tasksDir
        # The recipe file will provide the list of ini files that will create tasks
        fileList = map(lambda x: os.path.join(tasksDir, string.strip(x)), open(options.recipe_filename).readlines())
    else:
        # Take file list from arguments if provided
        fileList = args if (len(args) > 0) else findIniFiles(tasksDir)

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

