#!/usr/bin/env python

import glob
import os
import shutil
import subprocess
import sys

from logger import *
from Crypt import *
from SQLite import *

"""
# Import our own modules
from lib.logger import *

scriptName = ''
try:
    scriptName = __file___
except Exception as e:
    scriptName = sys.argv[0]

appDirName = os.path.dirname(os.path.realpath(scriptName))
rootDirName = os.path.realpath(appDirName + os.path.sep + '..')

logger = Logger(rootDirName + '/output/output2.txt')
sys.stdout = logger
sys.stderr = logger

self.logger.info("OGR =============")
self.logger.info("scriptName", scriptName)
self.logger.info("appDirName", appDirName)
self.logger.info("rootDirName", rootDirName)


"""

class OGRBase():
    """
    @requires:
        os
        subprocess
        sys
    """
    def __init__(self, items = {}, options = {}):
        #self.logger.info("Init ogr2ogr:", items, options)
        self.items = items
        self.options = options

        self.fileFormats = ['CSV', 'GML', 'VRT', 'KML', 'GPX', 'SQLite', 'ESRI Shapefile', 'MapInfo File', 'DGN', 'DXF']
        self.dbFormats = ['SQLite', 'ODBC', 'PostgreSQL']

        scriptName = ''
        try:
            scriptName = __file___
        except Exception as e:
            scriptName = sys.argv[0]

        appDirName = os.path.dirname(os.path.normpath(scriptName))
        #rootDirName = os.path.normpath(appDirName + os.path.sep + '..')

        self.executables = {
            'ogr2ogr': 'ogr2ogr',
            'ogrinfo': 'ogrinfo' 
            }

        loggerName = 'OGR'
        if 'logger' in options:
            logger = options.get('logger')
            self.logger = logger.clone(loggerName) 
        else:
            self.logger = Logger(loggerName)

    def CreateCommand(self, items):
        self.logger.debug("CREATECOMMAND", items)

        ##################################################
        # Create list of arguments for ogr2ogr
        command = [self.executable]

        # Get the format option and loop through it
        format = items.get('format', 'CSV')
        command += ['-f', format]

        assigncoordsys = items.get('assigncoordsys', None)
        if assigncoordsys:
            command += ['-a_srs', assigncoordsys]

        overridecoordsys = items.get('overridecoordsys', None)
        if overridecoordsys:
            command += ['-s_srs', overridecoordsys]

        transformcoordsys = items.get('transformcoordsys', None)
        if transformcoordsys:
            command += ['-t_srs', transformcoordsys]

        destination = items.get('destination', "DESTINATION_MISSING")
        if destination:
            command += [destination]

        datasource = items.get('datasource', "SOURCE_MISSING")
        if datasource:
            command += [datasource]

        sourcetablename = items.get('sourcetablename')
        select = items.get('select')
        where = items.get('where')
        sql = items.get('sql')

        """
        sqlfile = items.get('sqlfile')
        if sqlfile:
            if not os.path.exists(sqlfile):
                exitCode = 1
                errorMessage = "SQLFile file could not be found" 
                raise IOError(exitCode, errorMessage, str(sqlfile))

            sql = " ".join(open(sqlfile, 'r').read().splitlines())
        """

        if sourcetablename and not sql:
            sql = "SELECT %s FROM %s" % (select or '*', sourcetablename) 
            if where:
                sql += " WHERE %s" % where

        if not sql:
            if select:
                command += ['-select', select]
            if where:
                command += ['-where', where]
        else:
            command += ['-sql', sql]

        name = items.get('name', None)
        if name:
            command += ["-nln", name ]

        update = items.get('update', True)
        if update:
            # Don't provide update option if SQLite file does not exist yet
            formats = ['SQLite']
            if format in formats and os.path.isfile(destination):
                command += ["-update"]
            else:
                pass

        append = items.get('append', False)
        if append:
            command += ["-append"]

        overwrite = items.get('overwrite', True)
        if overwrite:

            # OGR's SQLite driver does not support DROPping tables,
            # so we do it ourselves
            if os.path.isfile(destination) or format == "PostgreSQL":

                if format in ["SQLite", "PostgreSQL"]:
                    if name:
                        # Remove the table from the geometry_columns first
                        sql = "DELETE FROM geometry_columns WHERE f_table_name = '%s'" % (name)
                        tmpItems = {
                            'datasource': destination,
                            'sql': sql,
                            'summary': False,
                        }
                        ogrinfo = OGRInfo(tmpItems)
                        ogrinfo.Process()

                        # Finally DROP the table
                        sql = 'DROP TABLE IF EXISTS ' + name + ''
                        tmpItems['sql'] = sql
                        ogrinfo = OGRInfo(tmpItems)
                        ogrinfo.Process()
                else: 
                    command += ["-overwrite"]

            # If destination is a directory and we have an 'nln' (name)
            # then we check if a file that matches that name exists.
            # (based on the output format)
            # If so, we add the 'overwrite' option.
            # Example: dest = 'output', name = 'address', format = shp,then 
            # we test for output/address.<shp|db> 
            if os.path.isdir(destination) and name:
                formatExtensions = {
                    'ESRI Shapefile': ['shp', 'dbf'],
                    'MapInfo File': ['tab', 'mif'],
                }
                extensions = formatExtensions.get(format, [])
                overwrite = False
                for ext in extensions:
                    file = "%s/%s.%s" % (destination, name, ext)
                    if os.path.isfile(file):
                        overwrite = True
                        break;
                if overwrite: 
                    command += ["-overwrite"]


            # Don't add overwrite parameter with CSV since we take 
            # care of this manually
            #elif format != "CSV":
                #command += ["-overwrite"]

        if format == "SQLite":
            # Introduce spatialite support, but only when the file does not
            # exist yet (otherwise it's a useless optio)
            spatialite = items.get('spatialite', True)
            if spatialite:

                # Only add this option when the destination does not exist yet
                if not os.path.isfile(destination):
                    command += ["-dsco", 'SPATIALITE=YES']

                # Determine whether to create a layer with a spatial 
                # index. Defaults to yes in OGR with spatialite enabled, 
                # but this fails for non-spatial layers
                # Rule: spatialindex is True unless:
                # - Set to False in INI
                # - DataSource is ODBC or CSV
                dsIsODBC = datasource.lower().startswith('odbc:')
                dsIsCSV = datasource.lower().endswith('.csv')

                spatialindex = items.get('spatialindex', not (dsIsODBC or dsIsCSV))

                # It is a default for Spatialite, but let's make it explicit, even
                # when it's set to yes
                if spatialindex:
                    command += ["-lco", 'SPATIAL_INDEX=YES']
                else:
                    command += ["-lco", 'SPATIAL_INDEX=NO']

            # Keep existing casing for table and column names (don't make it lower)
            command += ["-lco", 'LAUNDER=NO']

        return command

    def CommandToString(self, command):
        commandString = subprocess.list2cmdline(command)

        # Replace any encrypted passwords with masked ones ("*****") 
        #crypt = Crypt()
        #hidePasswords = True
        #commandString = crypt.Decrypt(commandString, hidePasswords)

        return commandString
        

    ##############################################################
    # Do a system call
    def ExecuteCommand (self, command):

        self.logger.info("#" * 60 + "\n#", self.CommandToString(command) + '\n')

        try:
            import subprocess
            kwargs = {}

            env = os.environ.copy()

            if subprocess.mswindows:
                su = subprocess.STARTUPINFO()
                su.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                su.wShowWindow = subprocess.SW_HIDE
                kwargs['startupinfo'] = su

                #gdal_data = gdal_path + '/gdal-data'

                #env['GDAL_DATA'] = gdal_data
                #env['PATH'] = ';'.join([gdal_path, gdal_bin_path, os.environ["PATH"]])


                """
                self.logger.info("#" * 50)
                self.logger.info("NEW NEW NEW ENV!")
                self.logger.info("#" * 50)
                e = 'PATH'
                self.logger.info("%s: %s" % (e, env.get(e, '')))
                """

                #kwargs['shell'] = True

            ## stderr=subprocess.PIPE,
            ## stdin=subprocess.PIPE,
            ##proc.stderr.close()
            ##proc.stdin.close()

            kwargs['env'] = env 
            kwargs['stdout'] = subprocess.PIPE 
            kwargs['stderr'] = subprocess.PIPE
            kwargs['stdin'] = subprocess.PIPE

            #process = subprocess.Popen( (r'c:\python25\python.exe', r'd:\projekte\bar.py'), **kwargs )

            #subprocess.call(['echo', '%PATH%'], **kwargs)
            #subprocess.check_call(command, **kwargs)

            # Replace any encrypted passwords with the plain text ones
            crypt = Crypt()
            command = map(crypt.Decrypt, command)

            process = subprocess.Popen(command, **kwargs)

            stdout, stderr = process.communicate()
            self.logger.info(stdout)
            #self.logger.info(stderr)
            exitCode = process.wait()
            if exitCode != 0:
                self.logger.info("There were some errors", exitCode)
                errorMessage = stderr
                raise EnvironmentError(exitCode, errorMessage)

        except Exception as e:
            self.logger.info("That didn't work well:", e)
            self.logger.info("Exiting. Please fix the problem!\n")
            raise

    def Process(self, items = None):
        items = items or self.items
        self.logger.info("OGR2OGR processing", items)

        #### OVERRIDE OGR2OGR if both source and destination are the same SQLite file

        sourceformat = items.get('sourceformat')
        datasource = items.get('datasource')
        destination = items.get('destination')
        name = items.get('name')
        sql = items.get('sql')
        
        if datasource == destination and sourceformat == 'SQLite' and sql:
            message = "# Source and Destination are the same SQLite file:\n"
            message += "# will use internal SQLite module instead of OGR\n"
            message += "# SQLite file: %s\n" % datasource
            message += "# Output table: %s\n" % name
            message += "# SQL: \n%s" % sql
            
            self.logger.info("#" * 60 + "\n" + message)

            #sql = "%r" % sql

            sqlite = SQLite()
            conn = sqlite.connect(datasource)
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS "%s"' % name)
            cursor.execute('CREATE TABLE "%s" AS %s' % (name, sql))

            self.logger.info("Done.")

        # ogr2ogr creates a directory for CSV output
        # We don't like that. That's why we have ogr2ogr
        # create a temp dir, move all files out if it after
        # it is done and then remove the temp dir
        elif items.get('format') == 'CSV':

            # Change the destination dir to the tmpDestDir 
            # (which is a subdir of the destDir)
            destDir = os.path.dirname(items['destination'])
            tmpDestDir = destDir + "/tmp" + str(os.getpid())
            items['destination'] = tmpDestDir

            command = self.CreateCommand(items)
            self.ExecuteCommand(command)

            # Move all files from tmpDestDir to destDir
            # and remove the tmpDestDir afterwards
            for file in glob.glob(tmpDestDir + '/*'):

                # Get File name from path
                fileName = os.path.basename(file)

                # Remove any pre-existing files in the 
                # destDir first
                destFile = destDir + '/' + fileName
                if os.path.isfile(destFile):
                    os.remove(destFile)

                # Move file from tmpDir to destDir
                shutil.move(file, destDir)
                self.logger.info("\n# Moved '%s' to '%s'" % (file, destDir))


            # Remove tmpDestDir (should be empty now)
            os.rmdir(tmpDestDir)

        else:
            command = self.CreateCommand(items)
            self.ExecuteCommand(command)


class OGR2OGR(OGRBase):
    def __init__(self, items = {}, options = {}):
        OGRBase.__init__(self, items, options)
        self.executable = self.executables['ogr2ogr']

class OGRInfo(OGRBase):
    def __init__(self, items = {}, options = {}):
        OGRBase.__init__(self, items, options)
        self.executable = self.executables['ogrinfo']

    def CreateCommand(self, items):
        #self.logger.info("CREATECOMMAND", self.executable, items)

        ##################################################
        # Create list of arguments for ogr2ogr
        command = [self.executable]

        sourceformat  = items.get('sourceformat')
        datasource = items.get('datasource', "SOURCE_MISSING")

        if datasource:
            command += [datasource]

        for itemName in ['where', 'sql']:
            itemValue = items.get(itemName, None)
            if itemValue:
                command += ['-' + itemName, itemValue ]

        sqlfile = items.get('sqlfile', None)
        if sqlfile:
            queryString = " ".join(open(sqlfile, 'r').read().splitlines())
            command += ["-sql", queryString ]

        layers = items.get('sourcetablename', '')
        if layers:
            command += [layers.replace(',', ' ')]

        summary = items.get('summary', True)
        if summary:
            command += ["-summary"]

        return command

if __name__ == "__main__":
    o = OGR2OGR()
    o.logger.info(o)
    sys.exit()

