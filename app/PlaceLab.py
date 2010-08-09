#!/usr/bin/env python


# Make app dir available to the sys path
import sys
sys.path.extend(['app'])

import iniparse
import logging
import logging.config
import optparse
import os

# Get version from version file
from version import version

# Import our own logger
from lib.logger import *

# create logger
logger = Logger('main', 'output/PlaceLab.log')

# Import our own modules
from lib.configparser import *
from lib.gui.gui import * 

# create logger
#l = logging.getLogger("PlaceLab")

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
    'logger': logger,
    'globalSections': ['Settings', 'Application Settings']
}
appConfig = ConfigParser(appConfigOptions) 
#logger.info("CONFIG FILE", appConfigFile)
if os.path.isfile(appConfigFile):
    appConfig.read(appConfigFile)
    #appConfig.SubstituteVariablesFromSection('Settings')
    for section in appConfig.sections():
        logger.debug("SECTION:", section)
        items = appConfig.items(section)
        logger.debug(items)

    if appConfig.has_section('ENV'):
        env = os.environ
        envItems = appConfig.items('ENV')
        for key, value in envItems:
            value = str(value) # force value to be a string
            if key.lower() == 'path':
               envpath = env.get('PATH', '')
               env[key] = os.pathsep.join(value.split(';') + envpath.split(os.pathsep))
               logger.debug("prepending to %s: %s" % (key, value))
            else:
               env[key] = value
               logger.debug("setting: %s to %s" % (key, value))
else:
    logger.warn('Application config file could not be found! (%s)' % appConfigFile)

appSettings = {}
try:
    appSettings = dict(appConfig.items('Application Settings'))
except Exception as e: 
    logger.warn('Error:', e)

#version = appSettings.get('Version', 'dev')

#if 'LogFile' in appSettings:
    #logger.SetFile(appSettings.get('LogFile'))

#logger.info(os.environ)

# Logging config file is the processed version of the appConfig
# file. This allows us to dynamically configure the location
# of the log file, etc.
# We need StringIO for the logger to read it.
#loggingConfig = StringIO.StringIO(appConfig)
#logging.config.fileConfig(loggingConfig)

#sys.stdout = sys.stderr = logger

# "application" code

# example with redirection of sys.stdout
#logger = Logger(logDir + os.path.sep + 'output.txt')
#sys.stdout = sys.stderr = logger
logger.info("PlaceLab version:", version)
logger.info("isExe", isExe)
logger.info("scriptPath", scriptPath)
logger.info("scriptName", scriptName)
logger.info("scriptBaseName", scriptBaseName)
logger.info("scriptDir", scriptDir)
logger.info("rootDir", rootDir)
logger.info("logDir", logDir)
logger.info("confFile", appConfigFile)
logger.info("CWD", os.getcwd())
"""
logger.info("sys.path", sys.path)
extra = os.environ.get('USERNAME')
if extra:
    sys.path.extend(extra.split(os.pathsep))
logger.info("sys.path", sys.path)

logger.info("-------------------")
logger.info("frozen", repr(getattr(sys, "frozen", None)))
logger.info("sys.executable", sys.executable)
logger.info("sys.prefix", sys.prefix)
logger.info("sys.argv", sys.argv)
logger.info("-------------------")

env = os.environ.copy()
logger.info("PATH", env.get('PATH'), '\n')
"""

#logger.info("ENVIRONMENT:")
#for e in env:
    #logger.info("%s: %s" % (e, env[e]))


# Name of the Settings section in the ini file
settingsSectionName = 'Settings'

###############################################################
# Process command line options and arguments
usage = "usage: %prog [options] path/to/ini-file"
parser = optparse.OptionParser(usage)
parser.add_option("-a", "--auto", action="store_true", default=False,
                  help="run only ini files that are marked with 'auto'", metavar="auto")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

# Don't use GUI if 'auto' is set
useGui = not options.auto 

#if len(args) < 1:
    #parser.error("please provide an ini file as argument")
    #useGui = True 

#iniFile = args[0]

logger.info("ARGS", useGui, args)

# USED HARDCODED IN OGR.py
# TODO: don't hardcode

gdalAppDir = rootDir + '/app/include/release-1310-gdal-1-6-mapserver-5-6/bin/gdal/apps'

#os.chdir(scriptHome)

###############################################
# Find all INI files in:
# - root dir
# - config dir
def findIniFiles():
    fileList = []
    rootdir = '.' 
    #configdir = rootDir + os.path.sep + 'config' 
    ext = '.ini'

    # Take top level INI files
    #for file in sorted(os.listdir(rootdir)):
        #if file.lower().endswith(ext):
            #fileList.append(os.path.join(rootdir,file))

    # Recurse through config directory to find INI files
    for root, subFolders, files in sorted(os.walk(tasksDir)):
        for file in files:
            if file.lower().endswith(ext):
                fileList.append(os.path.join(root,file))
    return fileList

# Take file list from arguments if provided
fileList = args if (len(args) > 0) else findIniFiles()

###############################################
# Now create a list of tasks based on the ini
# files found. Then sort it alphabetically
taskList = []
for file in fileList:
    taskName = os.path.splitext(os.path.basename(file))[0]
    taskList.append((taskName, file))
taskList.sort()

def showHeader(text):
    string = "#" * 60 + "\n#" + ' ' + text + "\n" + "#" * 60 
    logger.info(string)

def showGUI(taskList, options = {}):
    logger.info("Showing GUI")# , options)
    options['taskList'] = taskList
    app = GUI(options)

    #app.tasks = taskList

    app.Show()

def showGUIOLD(taskList, options = {}):
    logger.info("Showing GUI")# , options)
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

if __name__ == "__main__":
    if useGui:
        options = dict(appConfig.items('GUI')) if appConfig.has_section('GUI') else {}
        showGUI(taskList, options)
        pass
    else:
        processTasks(taskList)
        pass

