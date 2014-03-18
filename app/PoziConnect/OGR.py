#!/usr/bin/env python

import glob
import os
import shutil
import subprocess
import sys
import datetime

from logger import *
from Crypt import *
from SQLite import *

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

        self.fileFormats = ['CSV', 'GML', 'VRT', 'KML', 'GPX', 'SQLite', 'ESRI Shapefile', 'MapInfo File', 'DGN', 'DXF', 'GeoJSON','XLSX']
        self.dbFormats = ['SQLite', 'ODBC', 'PostgreSQL','OCI']

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

        sourceformat = items.get('sourceformat')
        sourcetablename = items.get('sourcetablename')
        select = items.get('select')
        where = items.get('where')
        sql = items.get('sql')

        # When SQLite is a source format, we need to add the name of the table to export
        if sourceformat == "SQLite":
            sourcetablename = items.get('sourcetablename', None)
            # In case there is no source table name (ex: use of a SQL query or file), we don't add the tablename to the command
            if sourcetablename:
                command += [sourcetablename]


        # Detecting if the source is spatial or not:
        dsIsODBC = datasource.lower().startswith('odbc:')
        dsIsCSV = datasource.lower().endswith('.csv')
        dsIsDBF = datasource.lower().endswith('.dbf')

        # GeometryType provided in configuration (always overrides automatic detection)
        geometrytype = items.get('geometrytype')

        # Automatic detection of data sources that are not spatial
        # This is limited - for instance, non-spatial MapInfo files not recognised as non-spatial
        if not geometrytype:
            if dsIsODBC or dsIsCSV or dsIsDBF:
                geometrytype = "NONE";

        if geometrytype:
            command += ['-nlt', geometrytype]

        # Logging if the destination directory does not exist
        destinationfilepath = items.get('destinationfilepath',None)
        destinationdrivename = items.get('destinationdrivename','')
        if destinationfilepath:
            # Catering for URI paths that do not contain a drive letter
            if destinationdrivename:
                destinationfullpath = destinationdrivename + destinationfilepath
            else:
                destinationfullpath = destinationfilepath
            if not(os.path.isdir(destinationfullpath)):
                errorMessage = "The directory '%s' does not exist - please create it before running the task again.\n" % (destinationfullpath)
                exitCode = 1
                self.logger.info("#" * 60 + "\n#", errorMessage ,"#" * 60 + "\n#")
                raise IOError(exitCode, errorMessage)

        if sourcetablename and not sql and sourceformat not in self.fileFormats and sourceformat not in ['ODBC']:
            if sourcetablename.replace(" ","")==sourcetablename:
                sql = "SELECT %s FROM %s" % (select or '*', sourcetablename)
                if where:
                    sql += " WHERE %s" % where
            else:
                self.logger.debug("Source table name:'%s' contains spaces." % (sourcetablename), items)

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

        # By default, overwriting the output file
        overwrite = items.get('overwrite', True)

        if overwrite:
            # OGR's SQLite driver does not support DROPping tables,
            # so we do it ourselves
            if os.path.isfile(destination):

                if format in ["SQLite"]:
                    if name:
                        # Remove the table from the geometry_columns first
                        sql = "DELETE FROM geometry_columns WHERE upper(f_table_name) = upper('%s')" % (name)
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
                    'MapInfo File': ['tab', 'mif']
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

        if format == "GeoJSON":
            # The hardcoded layer name for a GeoJSON file is "OGRGeoJSON"
            sourcetablename = "OGRGeoJSON"

        if format == "SQLite":
            # Introduce spatialite support, but only when the file does not
            # exist yet (otherwise it's a useless option)
            spatialite = items.get('spatialite', True)

            # Performance: increasing the commit batch size
            command += ['-gt', '65536']

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
                spatialindex = items.get('spatialindex', not (geometrytype=="NONE"))

                # It is a default for Spatialite, but let's make it explicit, even
                # when it's set to yes
                if spatialindex:
                    command += ["-lco", 'SPATIAL_INDEX=YES']
                else:
                    command += ["-lco", 'SPATIAL_INDEX=NO']

            # Keep existing casing for table and column names (don't make it lower)
            launder = items.get('launder', False)
            if launder:
                command += ["-lco", 'LAUNDER=YES']
            else:
                command += ["-lco", 'LAUNDER=NO']

        if format == "PostgreSQL":
            # Normalisation of object (table, columns...) names
            command += ["-lco", 'LAUNDER=YES']

            # Not creating spatial indexes if spatialindex set to false
            spatialindex = items.get('spatialindex', True)
            if not spatialindex:
                command += ["-lco", 'SPATIAL_INDEX=NO']

            # This maintains the name of the spatial column in non-spatial object to wkb_geometry
            if geometrytype != "NONE":
                command += ["-lco", 'GEOMETRY_NAME=the_geom']
            # Skipping unsuccessful OGR2OGR commands
            command += ["-skipfailures"]
            # Catering for the case where we really want to overwrite the object (changed structure) - by default, we update/append
            overwrite = items.get('overwrite', False)
            if overwrite:
                command += ["-overwrite"]
            else:
                command += ["-update"]
                command += ["-append"]

            # Removing the existing records - so that the append re-populates empty tables
            if name:
                # Truncate the table
                sql = "TRUNCATE TABLE %s" % (name)
                tmpItems = {
                    'datasource': destination,
                    'sql': sql,
                    'summary': False,
                }
                ogrinfo = OGRInfo(tmpItems)
                ogrinfo.Process()

        if format == "OCI":
            # Normalisation of object (table, columns...) names
            command += ["-lco", 'LAUNDER=YES']

            # Overwrite by default
            command += ["-overwrite"]

            # Managing the target SRID - extract the numeric part coordinate system (only if geometry type is not NONE)
            if geometrytype != "NONE":
                if not assigncoordsys:
                    self.logger.error("The coordinate system is required via a parameter 'AssignCoordSys'")
                else:
                    command += ["-lco", 'srid='+assigncoordsys.split(":")[1]]

            # Not creating spatial indexes if spatialindex set to false
            spatialindex = items.get('index', True)
            if not spatialindex:
                command += ["-lco", 'INDEX=NO']

            # This maintains the name of the spatial column in non-spatial object to wkb_geometry
            if geometrytype != "NONE":
                command += ["-lco", 'GEOMETRY_NAME=the_geom']

        return command

    def PostProcess(self, items):
        try:
            format = items.get('format', 'CSV')
            if format == "PostgreSQL":
                self.logger.debug("POSTPROCESS", items)

                ##################################################
                name = items.get('name', None)
                destination = items.get('destination', "DESTINATION_MISSING")
                datasource = items.get('datasource', "SOURCE_MISSING")
                geometrytype = items.get('geometrytype')
                viewsupportingspatiallayer = items.get('viewsupportingspatiallayer')
                viewname = items.get('destinationtablename')

                if name:
                    # Add a comment to date / time the update of the table
                    d_str=datetime.datetime.now().strftime("%d/%m/%y at %H:%M:%S")

                    # Object type - defaults to TABLE
                    obj_type = "TABLE"
                    if viewsupportingspatiallayer:
                        obj_type = "VIEW"
                    if items.get('ogrinfoonly'):
                        datasource = "PoziConnect"

                    sql = "COMMENT ON %s %s IS 'Updated on %s (source: PoziConnect)'" % (obj_type,name,d_str)
                    tmpItems = {
                        'datasource': destination,
                        'sql': sql,
                        'summary': False
                    }
                    ogrinfo = OGRInfo(tmpItems)
                    ogrinfo.Process()

                    if geometrytype =="NONE":
                        # Remove the dummy geometry column in the table
                        # DROP COLUMN IF EXISTS not available in 8.4
                        sql = "ALTER TABLE %s DROP COLUMN %s" % (name,"wkb_geometry")
                        tmpItems = {
                            'datasource': destination,
                            'sql': sql,
                            'summary': False
                        }
                        ogrinfo = OGRInfo(tmpItems)
                        ogrinfo.Process()

                # For views: special processing of the geometry_column records
                if viewsupportingspatiallayer and viewname:

                    # Delete the geometry_columns record for this view
                    sql = "DELETE FROM geometry_columns WHERE f_table_name='%s'" % (viewname)
                    tmpItems = {
                        'datasource': destination,
                        'sql': sql,
                        'summary': False
                    }
                    ogrinfo = OGRInfo(tmpItems)
                    ogrinfo.Process()

                    # Insert the geometry_columns record based on the supporting spatial layer
                    sql = "INSERT INTO geometry_columns SELECT f_table_catalog,f_table_schema,'%s',f_geometry_column,coord_dimension,srid,type FROM geometry_columns WHERE f_table_name='%s'" % (viewname,viewsupportingspatiallayer)
                    tmpItems = {
                        'datasource': destination,
                        'sql': sql,
                        'summary': False
                    }
                    ogrinfo = OGRInfo(tmpItems)
                    ogrinfo.Process()

                    # We don't remove the record in the geometry_columns table to allow for update/append
                    # If we delete this record, the update/append raises an error

        except Exception as e:
            self.logger.info("That didn't work well:", e)
            self.logger.info("Exiting. Please fix the problem!\n")
            raise

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
                import _subprocess
                su = subprocess.STARTUPINFO()
                su.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
                su.wShowWindow = _subprocess.SW_HIDE
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

            self.logger.info("#" * 60 + "\n#"+ "LOGGING ERRORS FROM EXECUTABLE CALL - START" + '\n')
            self.logger.info(stderr)
            self.logger.info("#"+ "LOGGING ERRORS FROM EXECUTABLE CALL - END\n" + "#" * 60 + '\n')

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
        sqlprocessing = (items.get('sqlprocessing', 'OGR')).upper()

        if datasource == destination and sourceformat == 'SQLite' and sql and (sqlprocessing=="SQLITE"):
            message = "# Source and Destination are the same SQLite file:\n"
            message += "# will use internal SQLite module instead of OGR\n"
            message += "# SQLite file: %s\n" % datasource
            message += "# Output table: %s\n" % name
            message += "# SQL: \n%s" % sql

            self.logger.info("#" * 60 + "\n" + message)

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
            # When outputting to tab files, files can not be overwritten easily
            # We delete them manually if the overwrite option has been specified
            if items.get('format') == 'MapInfo File' and items.get('overwrite'):
                self.logger.info("\n# Overwrite option is on: will delete existing files with same name (if they exist)\n")
                (filepath, filename) = os.path.split(items['destinationstore'])
                (shortname, extension) = os.path.splitext(filename)

                #We go throught the possible extensions for MapInfo files that compose a layer and delete the corresponding files if they exists
                for file in (glob.glob(os.path.join(filepath,shortname)+ext) for ext in ('.tab','.id','.map','.dat','.ind')):
                    #shutil.move(file, file+'.bak')
                    if file and os.path.isfile(file[0]):
                        self.logger.info("# Deleting file: '%s' " % (file[0]))
                        os.remove(file[0])

            # Basic processing
            command = self.CreateCommand(items)
            self.ExecuteCommand(command)
            self.PostProcess(items)


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
        datasource = items.get('datasource', items.get('destinationstore',"SOURCE AND DESTINATION MISSING"))


	# Adding support for definitions of views using OGRINFO
	viewsupportingspatiallayer = items.get('viewsupportingspatiallayer')
	viewdefinition = items.get('viewdefinition')

	if viewsupportingspatiallayer and viewdefinition:
		viewname = items.get('destinationtablename')

		datasource = items.get('destinationstore')
		command += [datasource]

		queryString = "CREATE OR REPLACE VIEW %s AS %s" % (viewname,viewdefinition)
		command += ["-sql", queryString ]
	else:
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

