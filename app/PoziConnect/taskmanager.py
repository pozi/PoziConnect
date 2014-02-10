#!/usr/bin/env python

# Make app dir available to the sys path
import sys
sys.path.extend(['.', '..', 'lib'])

import os
import datetime
from datetime import datetime
import sqlite3
import StringIO

# Modules to allow tasks to be threaded
# (needed for GUI)
import threading
from threading import Thread

# Modules for creating ZIP files
import zipfile
from zipfile import *
import zlib

# PlaceLab's modules
from configparser import *
from logger import *
from OGR import *
from ExcelReader import *

# Helper functions
from utilities import *
try:
    from os import startfile
except:
    pass

# Get version information
from PoziConnect.version import version

# For copying files
import shutil
from shutil import *

taskDebug = True

#####################################################
# Task Manager Class
#####################################################

class TaskManager(Thread):
    def __init__(self, options = {}):
        Thread.__init__(self)
        #self.logger.debug("Init:", fileName)

        loggerName = 'TaskManager'
        if 'logger' in options:
            logger = options.get('logger')
            self.logger = logger.clone(loggerName)
        else:
            self.logger = Logger(loggerName)

        # For management of ending the thread
        self._stop = threading.Event()

        # Store default options first
        self.options = {
            'lowerKeys': False,
            'itemsAsDict': False,
            'configFile': None,
            'globalSections': ['User Settings', 'General Settings']
        }

        # Then merge provided options with the default ones
        self.options.update(options)

        self.InitConfig()


    ###############################################################
    # Process INI file
    ###############################################################
    def InitConfig(self):
        self.config = ConfigParser(self.options)

        self.configFile = self.options.get('configFile')
        if self.configFile:
            self.config.read(self.configFile)

    def stop (self):
        self._stop.set()

    def stopped (self):
        return self._stop.isSet()

    def GetSectionItems(self, section):
        items = {}
        if self.config.has_section(section):
            items = self.config.items(section)
            if self.options.get('lowerKeys'):
                items = items.LowerKeys()
            if self.options.get('itemsAsDict'):
                items = dict(items)
        else:
            self.logger.warn("Section %s does not exist!" % (section))
        return items

    def GetTaskSections(self):
        """
        Returns all sections in config that are not global sections
        """

        globalSections = self.config.GetGlobalSections()
        sections = self.config.sections()
        taskSections = []

        tmpSections = sections[:]
        for section in tmpSections:
            if section not in globalSections:
                taskSections.append(section)

        self.logger.debug("sections", globalSections, sections, taskSections)
        return taskSections

    def run(self):
        self.logger.debug("Task run")
        try:
            self.Execute()
        except Exception as e:
            if self.errorCallback:
                self.errorCallback(e)
            else:
                sys.exit(1)

    def logHeader(self, text):
        string = "#" * 60 + "\n#" + ' ' + text + "\n" + "#" * 60
        self.logger.info(string)

    def Execute(self):
        taskName = self.options.get('taskName', 'unknown')
        text = "Processing Task: '%s' ('%s')" % (taskName, self.configFile)
        self.logHeader(text)

        # Assign callback functions for reporting progress and notifaction
        # of completion of app
        readyCallback = self.readyCallback if hasattr(self, 'readyCallback') else None
        progressCallback = self.progressCallback if hasattr(self, 'progressCallback') else None
        errorCallback = self.errorCallback if hasattr(self, 'errorCallback') else None

        ###############################################################
        # Loop through sections and process them


        taskSettings = dict(self.GetSectionItems('General Settings'))
        #self.logger.debug("task settings", taskSettings)

        taskDebug = taskSettings.get('Debug', True)

        sections = self.GetTaskSections()

        counter = 1

        for section in sections:

            # Stop if directed
            if self.stopped():
                break

            # Execute progress Callback if supplied
            if progressCallback:
                # We start of with counter = 1 and end with the number
                # of sections +1. This makes our gauge show up something
                # immediately from the start, which is more intuitive.
                percentage = (100 * counter) / (len(sections) + 1)
                #self.logger.debug("Calling progress callback", percentage)

                status = "Processing %s..." % section
                progressCallback(percentage, status)

            # For keeping track of progress
            counter += 1

            # Items are returned in dict form and have their keys
            # in lower case (True)

            items = self.GetSectionItems(section)

            self.logger.info("#" * 60 + "\n#" + ' Section: ' + section + "\n" + "#" * 60 )

            # Run task
            task = Task(section, dict(items))
            task.run()

        # Execute Ready Callback if supplied
        if readyCallback:
            #self.logger.debug("Calling ready callback", readyCallback)
            status = "Cancelled." if self.stopped() else "Completed at "+str(datetime.datetime.now().strftime("%H:%M:%S"))+"."
            self.logger.info("#" * 60 + "\n#" + 'Task ' + status + "\n" + "#" * 60 )
            readyCallback(status)


#####################################################
# Task Class
#####################################################

class Task():
    def __init__(self, section = '', items = {}, options = {}):

        self.section = section
        self.items = items

        loggerName = 'Task'
        if 'logger' in options:
            logger = options.get('logger')
            self.logger = logger.clone(loggerName)
        else:
            self.logger = Logger(loggerName)

        self.logger.debug("Init Task", section, items)

        # Apply magic to the Source data store string and extract
        # extra information from it
        Source = self.items.get('Source')
        srcItems = self.ParseDataStore(Source) or {}

        # Prepend the word 'Source' to every item
        srcItems = dict(('Source' + x, y) for x,y in srcItems.items())

        # Apply magic to the Destination data store string and extract
        # extra information from it
        Destination = self.items.get('Destination')
        dstItems = self.ParseDataStore(Destination) or {}

        # Prepend the word 'Destination' to every item
        dstItems = dict(('Destination' + x, y) for x,y in dstItems.items())

        self.logger.debug('SourceDataStore',  srcItems)
        self.logger.debug('DestDataStore',  dstItems)

        # Merge the extracted information with the existing items
        self.items.update(srcItems)
        self.items.update(dstItems)

        self.logger.debug('ALL', self.items)

        # A reference list of file and database formats
        self.fileFormats = ['CSV', 'GML', 'VRT', 'KML', 'GPX', 'SQLite', 'ESRI Shapefile', 'MapInfo File', 'DGN', 'DXF','XLS']
        self.dbFormats = ['SQLite', 'ODBC', 'PostgreSQL','OCI']

    def ParseDataStore(self, store, forcedFormat = None):
        if not store:
            return {}

        self.logger.debug("  Store: ", store)

        globalRegs = {
            'dirSep': r'[\/\\]', # either / or \ are accepted
            'driveName': r'[a-z]:\\', # C:\
            'fileName': r'[ a-z0-9_-]+', # water_use-2
            'fileExtension': r'\.[a-z0-9_-]+', # .csv
            'schemaName': r'[a-z0-9]+',
            'tableName': r'[a-z0-9_\- .:]+',
            'fileFormat': r'(({driveName})?(.+?){dirSep}?(({fileName})({fileExtension})))',
        }
        #regexp = r'(%s)?(.*?)%s?((%s)(%s))' % (driveName, dirSep, validFileName, fileExt)

        ff = globalRegs['fileFormat']
        self.logger.debug("FF:", ff.format(**globalRegs))

        formatRegs = {
            'SQLite': {
                '1-File Path SQLite with Table Name specified': {
                    'regExp': globalRegs.get('fileFormat') + ',(.+)',
                    'formatRegs': {
                        'fileExtension' : r'\.sqlite',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', None, 'FileExtension', 'TableName'],
                },
                '2-File Path SQLite without Table Name': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.sqlite',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', None, 'FileExtension'],
                },
                '3-File Path db with Table Name specified': {
                    'regExp': globalRegs.get('fileFormat') + ',(.+)',
                    'formatRegs': {
                        'fileExtension' : r'\.db',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', None, 'FileExtension', 'TableName'],
                },
                '4-File Path db without Table Name': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.db',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', None, 'FileExtension'],
                },
            },
            'CSV': {
                '1-File Path': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.csv',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'XLS': {
                '1-File Path': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.xls',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'KML': {
                '1-File Path': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.kml',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'TableName', None, 'FileExtension'],
                },
            },
            'ESRI Shapefile': {
                '1-File Path': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.shp',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
                '2-DBF only': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.dbf',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'MapInfo File': {
                '1-File Path TAB': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.tab',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
                '2-File Path MIF': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.mif',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'DGN': {
                '1-File Path': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.dgn',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'DXF': {
                '1-File Path': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.dxf',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'GML': {
                '1-File Path': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.gml',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'GeoRSS': {
                '1-File Path': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.xml^',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'VRT': {
                '1-File Path with Table Name specified': {
                    'regExp': globalRegs.get('fileFormat') + ',(.+)',
                    'formatRegs': {
                        'fileExtension' : r'\.vrt',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', None, 'FileExtension', 'TableName'],
                },
                '2-File Path without Table Name specified': {
                    'regExp': globalRegs.get('fileFormat'),
                    'formatRegs': {
                        'fileExtension' : r'\.vrt',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', 'TableName', 'FileExtension'],
                },
            },
            'ODBC': {
                #'1-Schema+Table': {
                    #'regExp': r'(ODBC:[^,]+),?({schemaName})\.({tableName})',
                    #'outputVars': ['Store', 'SchemaName', 'TableName'],
                #},
                '2-Table Only': {
                    'regExp': r'((ODBC:[^,]+),?({tableName}))',
                    'outputVars': ['Store', 'StoreBase', 'TableName'],
                },
            },
            'PostgreSQL': {
                #'1-Schema+Table': {
                    #'regExp': r'(PG:[^,]+),?({schemaName})\.({tableName})',
                    #'outputVars': ['Store', 'SchemaName', 'TableName'],
                #},
                '2-Table Only': {
                    'regExp': r'(PG:[^,]+),?({tableName})',
                    'outputVars': ['Store', 'TableName'],
                },
            },
            'OCI': {
                #'1-Schema+Table': {
                    #'regExp': r'(PG:[^,]+),?({schemaName})\.({tableName})',
                    #'outputVars': ['Store', 'SchemaName', 'TableName'],
                #},
                '2-Table Only': {
                    'regExp': r'(OCI:[^,]+),?({tableName})',
                    'outputVars': ['Store', 'TableName'],
                },
            },
            'WFS': {
                'WFS URL endpoint with table name': {
                    'regExp': r'(WFS:[^,]+),?({tableName})',
                    'outputVars': ['Store', 'TableName'],
                },
                'WFS XML definition file with table name': {
                    'regExp': globalRegs.get('fileFormat') + ',({tableName})',
                    'formatRegs': {
                        'fileExtension' : r'\.xml',
                    },
                    'outputVars': ['Store', 'DriveName', 'FilePath', 'FileName', None, 'FileExtension', 'TableName'],
                },
	     },
        }

        def match(format, items, formatIsForced = False):
            for item in sorted(items.items()):
                self.logger.debug("  Format:", format)
                self.logger.debug("  Items:", item)
                #self.logger.debug("options:", options)

                flavour, options = item
                regExp = options.get('regExp')
                formatRegs = options.get('formatRegs', {})
                outputVars = options.get('outputVars', [])
                self.logger.debug("    Flavour:", flavour)
                self.logger.debug("      formatRegs:", formatRegs )
                self.logger.debug("      outputVars:", outputVars )
                regOptions = globalRegs.copy()
                regOptions.update(formatRegs)

                # When the format is forced, accept any file extension instead
                # of the default for this (file) format
                if formatIsForced:
                    regOptions['fileExtension'] = globalRegs['fileExtension']

                self.logger.debug("      Regexp before:", regExp )
                # Do variable substitution using regOptions
                regExp = regExp.format(**regOptions)
                self.logger.debug("      Regexp after: ", regExp )

                p = re.compile(regExp, re.IGNORECASE)
                for i in re.finditer(p, store):
                    self.logger.debug('      ** Match: ', i.groups())
                    formatObject = {}
                    formatObject['Format'] = format
                    for index, varValue in enumerate(i.groups()):
                        varName = outputVars[index]
                        if varName:
                            self.logger.debug("        Set: %s = %s" % (varName, varValue))
                            formatObject[varName] = varValue
                    return formatObject
            return {}

        # What formats to loop through to find a match?
        # If we force a format, it will only that one.
        # Otherwise we use heuristics by looping through
        # all of them until we find a match. First match wins.

        formats = formatRegs.keys()

        if forcedFormat:
            self.logger.debug("  Forced Format: ", forcedFormat)
            if forcedFormat in formatRegs:
                formats = [forcedFormat]
            else:
                self.logger.debug("  Forced format '%s' is unknown. Known formats are: %s" % (forcedFormat, str(formatRegs.keys())))
                self.logger.debug("  Exiting...")
                return {}
        else:
            self.logger.debug("  Using heuristics to find matching format...")

        for format in formats:
            self.logger.debug("  Testing format: %s" % (format))
            items = formatRegs.get(format)
            o = match(format, items, forcedFormat)
            if o:
                return o

        # We only get here if a format could not be matched
        self.logger.critical('A format could not be found for: %s' % store)

    def doInfo(self, items):
        self.logger.debug('ITEMS', items)

        # Execute an ogrinfo on the datasource. Whether or not
        # to this defaults to application settting for 'debug'
        # in INI file
        debug = items.get('debug', taskDebug)

        if items.get('sourceformat')=="XLS":
        	debug = False

        if debug:
            ogrInfoItems = {
                'sourceformat': items.get('sourceformat'),
                'datasource': items.get('datasource'),
                'sourcetablename': items.get('sourcetablename'),
            }
            ogrinfo = OGRInfo()
            ogrinfo.Process(ogrInfoItems)

    def doIndex(self, items):
        #items = self.items.copy()
        format = items.get('format')
        indexString = items.get('index')
        name = items.get('name')

        self.logger.info('DoIndex', items)

        if indexString and format in self.dbFormats:
            self.logger.debug("\n#" + ' Creating index on %s:' % indexString)
            indices = indexString.split(',')
            for index in indices:
                idx = "_".join(['idx', name, index])
                sql = 'CREATE INDEX ' + idx + ' ON "' + name + '"(' + index + ');'

                ogrInfoItems = {
                    'datasource': items.get('destination'),
                    'sql': sql,
                    'summary': False,
                }
                ogrinfo = OGRInfo()
                ogrinfo.Process(ogrInfoItems)

    def run(self):
        self.logger.debug('Task running')

        # Some preprocessing: read SQLFile into SQL parameter
        sqlFile = self.items.get('SQLFile')
        if sqlFile:
            if not os.path.exists(sqlFile):
                exitCode = 1
                errorMessage = "SQLFile file could not be found"
                raise IOError(exitCode, errorMessage, str(sqlFile))

            sqlFileHandle = open(sqlFile, 'r')
            sqlString = sqlFileHandle.read()
            sqlFileHandle.close()

            sql = " ".join(sqlString.splitlines())

            # Trick to do variable substitution on the sql
            sql = Item(('sql', sql)).SubstituteVars(self.items)[1]

            # Store the SQL in the items so it can be used
            self.items['SQL'] = sql

        # Convert items into how OGR understands them (lower case
        # and some different names):
        translate = {
            'sourcestore': 'datasource',
            'destinationstore': 'destination',
            'destinationformat': 'format',
            'destinationtablename': 'name',
        }

        ogrItems = {}
        for key, value in self.items.items():
            ogrItems[key.lower()] = value

        for key, translated in translate.items():
            if key in ogrItems:
               ogrItems[translated] = ogrItems[key]

        self.logger.info('Task items', self.items)
        self.logger.info('OGR items', ogrItems)

        # Execute Pre Command (if provided)
        preCommand = self.items.get('PreCommand')
        if preCommand:
            self.ExecuteCommand(preCommand, 'PreCommand')

        # Execute Command (if provided)
        Command = self.items.get('Command')
        if Command:
            self.ExecuteCommand(Command, 'Command')

        # Get sourece and destination stores
        sourceStore = self.items.get('SourceStore')
        sourceFormat = self.items.get('SourceFormat')
        destinationStore = self.items.get('DestinationStore')
        destinationFormat = self.items.get('DestinationFormat')

        # Do OGRinfo
        if sourceStore:
            if sourceFormat in self.fileFormats and not os.path.exists(sourceStore):
                exitCode = 1
                errorMessage = "Section '%s'\nSource file could not be found" % (self.section)
                raise IOError(exitCode, errorMessage, str(sourceStore))

            # Perform an ogrinfo
            self.doInfo(ogrItems)

	    if sourceFormat == 'XLS':
	    	# We need to process the Excel file into a CSV file - CSV files can then be processed natively by OGR2OGR
	    	# with the help of:
	    	# - the CSVT file for the types
	    	# - the VRT file for layer naming / conversion of XY into a geometry
	    	# Then, we need to provide the correct items values for the source to OGR2OGR
	    	# so that the source is now the resulting CSV (not the Excel file anymore)

	    	# Excel to CSV
	    	itemsForScript = ogrItems
	    	try:
		    	XLSread(itemsForScript,self)
                except Exception as e:
                	self.logger.critical("Excel to CSV Failed:", e)
                	raise

        # Perform ogr2ogr, but only if both a source and destination are configured
        if sourceStore and destinationStore:

            # If no destination table name is provided
            # then we assume the new table name will be the
            # same as the source table name
            if not ogrItems.get('name'):
                ogrItems['name'] = ogrItems.get('sourcetablename')

            # If destination format is any of the following, then manually
            # remove the destination files (work around buggy behaviour
            # in OGR).
            # Some formats then need to have their destination being the
            # destination directory instead of the full path
            # (ie: 'output' instead of 'output/file.shp')
            #if destinationFormat in ['GML','KML','DGN','ESRI Shapefile','MapInfo File']:
            if destinationFormat in ['GML','KML','DGN']:
                destination = ogrItems['destination']
                if os.path.isfile(destination):
                    self.logger.info("Removing existing destination: %s" % destination)
                    os.remove(destination)

            if destinationFormat in ['ESRI Shapefile', 'MapInfo File']:
                destDriveName = ogrItems.get('destinationdrivename') or ''
                destFilePath = ogrItems.get('destinationfilepath') or ''
                ogrItems['destination'] = destDriveName + destFilePath

            # Now we call ogr2ogr for this task (does the majority of the work)
            # Since it can raise exceptions, be put it in a try clause
            ogr2ogr = OGR2OGR()
            try:
                ogr2ogr.Process(ogrItems)
            except Exception as e:
                self.logger.critical("OGR Failed:", e)
                raise

        # Create indices if provided
        if destinationStore:
            # Create indices
            if ogrItems.get('index'):
                self.doIndex(ogrItems)

	    if ogrItems.get('ogrinfoonly'):
		ogrinfo = OGRInfo()
		try:
			ogrinfo.Process(ogrItems)
		except Exception as e:
			self.logger.critical("OGRINFO Failed:", e)
                	raise

        # Execute Post Command (if provided)
        postCommand = self.items.get('PostCommand')
        if postCommand:
            self.ExecuteCommand(postCommand, 'PostCommand')

    def ExecuteCommand(self, command, commandName = 'Command'):
        if command:

            self.logger.info("#" * 60 + "\n# Executing %s: \n# %s" % (commandName, command))

            try:
                sys.stdout = self.logger
                sys.stderr = self.logger

                # Decrypt any possible encrypted passwords in the command
                command = Crypt().Decrypt(command)

                exec(command)
            except Exception as e:
                self.logger.error("Command failed:\n", e)
            finally:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
        else:
            self.logger.warn("Execute %s: no command given. What am I supposed to do with that? ;-)" % commandName)


    def test(self):

        teststrings = {
            #'csv1': r'C:\Progra~1\output\blah.CsV',
            #'vrt': r'C:\Program Files\output\blah.vrt',
            #'kml1': r'C:\Program Files\output\blah.kml',
            #'sqlite1': '/OutputFolder/PlaceLab.sqlite,LYNX_vwPropertyClassification',
            #'sqlite2': '/OutputFolder/PlaceLab.sqlite',
            #'csv2': 'output',
            #'csv3': '/output/blah.csv',
            #'csv4': 'output/blah-2.csv',
            'shp1': 'output/blah.shp',
            #'odbc1': 'ODBC:DSN=Proclaim DSN;Trusted_Connection=Yes,dbo.tablename',
            #'odbc2': 'ODBC:DSN=Proclaim DSN;Trusted_Connection=Yes,tablename',
        }
        #dataSource = self.formats.get(self.inputFormat) % (self.inputStore, self.inputTable)
        #self.logger.debug("dataSource:", dataSource)

        for key in teststrings.keys():
            value = teststrings.get(key)
            self.logger.debug("Testing: %s -> %s" % (key, value) )
            forcedFormat = 'CCSV'
            o = self.ParseDataStore(value)
            #o = self.ParseDataStore(value, forcedFormat)
            print "OOO:", o
            self.logger.debug("OOO:", o)

if __name__ == "__main__":

    #DSNList()

    f = '../../config/button.ini'
    f = '../../PlaceLab.ini'
    f = '../../config/Test Export - Sample CSV.INI'
    f = '../../config/VICDATA.ini'
    options = {
        'lowerKeys': False,
        'itemsAsDict': True,
        'configFile': f,
        'globalSections': ['User Settings', 'Connection Settings', 'General Settings']
        }

    tm = TaskManager(options)
    #tm.Execute()
    section = 'ODBC 2 CSV'
    section = 'PIQA Parcel Extract'
    section = 'CSV Dir'
    #items = tm.GetSectionItems(section)
    task1 = Task()
    task1.test()


