#!/usr/bin/env python

import sys

import iniparse
import logging
import logging.config
import optparse
import os
import string

# Get version from version file
from version import version

# Import our own logger
from lib.logger import *

# Import our own modules
from lib.configparser import *
from lib.gui.gui import * 


# Global Variables
# create logger
LOGGER = Logger('main', 'output/PlaceLab.log')
# create logger
#l = logging.getLogger("PlaceLab")
# Global Variables


###############################################
# Find all INI files in:
# - root dir
# - config dir
def findIniFiles(tasksDir):
    fileList = []
    rootdir = '.' 
    #configdir = rootDir + os.path.sep + 'config' 
    ext = '.ini'

    # Take top level INI files
    #for f in sorted(os.listdir(rootdir)):
        #if f.lower().endswith(ext):
            #fileList.append(os.path.join(rootdir,file))

    # Recurse through config directory to find INI files
    for root, subFolders, files in sorted(os.walk(tasksDir)):
        for f in files:
            if f.lower().endswith(ext):
                fileList.append(os.path.join(root,f))
    return fileList


def showHeader(text):
    string = "#" * 60 + "\n#" + ' ' + text + "\n" + "#" * 60 
    LOGGER.info(string)


def showGUI(taskList, options = {}):
    LOGGER.info("Showing GUI")# , options)
    options['taskList'] = taskList
    app = GUI(options)

    #app.tasks = taskList

    app.Show()


def showGUIOLD(taskList, options = {}):
    LOGGER.info("Showing GUI")# , options)
    app = mainGUI(0)

    # Store the file and profile list in the app
    #app.files = fileList
    app.tasks = taskList
    app.options = options 
    
    # Merge default options with ones provided in app INI file
    app.options.update(options)

    app.Show()
    #app.MainLoop()


def processTasks(taskList):
    for taskName, taskFile in taskList:
        options = {
            'taskName': taskName,
            'configFile': taskFile,
        }
        p = TaskManager(options)
        p.Execute()


###############################################
# Initialise
# - TODO - this function is too long - need to refactor it
def init():
    # Make app dir available to the sys path
    sys.path.extend(['app'])

    # Find out where our script lives and assume that the 
    # parent directory is the root of the application

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

    #version = appSettings.get('Version', 'dev')

    #if 'LogFile' in appSettings:
        #LOGGER.SetFile(appSettings.get('LogFile'))

    #LOGGER.info(os.environ)

    # Logging config file is the processed version of the appConfig
    # file. This allows us to dynamically configure the location
    # of the log file, etc.
    # We need StringIO for the LOGGER to read it.
    #loggingConfig = StringIO.StringIO(appConfig)
    #logging.config.fileConfig(loggingConfig)

    #sys.stdout = sys.stderr = LOGGER

    # "application" code

    # example with redirection of sys.stdout
    #LOGGER = Logger(logDir + os.path.sep + 'output.txt')
    #sys.stdout = sys.stderr = LOGGER
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
    print taskList
    if options.useGui:
        options = dict(appConfig.items('GUI')) if appConfig.has_section('GUI') else {}
        showGUI(taskList, options)
    else:
        processTasks(taskList)

