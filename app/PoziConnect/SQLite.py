import sqlite3
import re

# PlaceLab's modules
from logger import *

class SQLite():
    """ SQLite extends sqlite3 with regular expression functionality """

    def __init__(self, options = {}):
        loggerName = 'SQLite'
        if 'logger' in options:
            logger = options.get('logger')
            self.logger = logger.clone(loggerName) 
        else:
            self.logger = Logger(loggerName)

        # Copy all available methods in module
        # to this class
        for i in dir(sqlite3):

            # Except for methods that we override
            if not i in dir(self):
                exec ("self.%s = sqlite3.%s" % (i, i))
            else:
                #print "Skipping: " , i
                pass

    def connect(self, string):

        # Use the standard SQLite3 connection
        conn = sqlite3.connect(string)

        ###############################################
        # Add some useful functions to our SQL
        ###############################################
        
        def regexp(expr, item):
          return re.search(expr, item or '') is not None  

        def regexp_replace(text, pattern, replacement):

            if text is None:
            	text = ''
            	
            """
            print "-" * 60
            print "pattern", pattern
            print "replacement", replacement
            print "TEXT IN :", text
            print "TYPE OF TEXT :", type(text)
            print "MATCH  ", re.search(pattern, text)
            print "FINDALL  ", re.findall(pattern, text)
            """

            	
            output = None


            # Compile a regular expression speeds up the process
            # Also make search/replace case insensitive
            pattern = re.compile(pattern, re.I)

            # Only replace when there is a match, otherwise return None
            match = re.search(pattern, text)
            if match:
                try:
                    output = re.sub(pattern, replacement, text)
                except Exception as e:
                    error = [] 
                    error.append("regexp_replace failed:")
                    error.append("  errror:      %s" % str(e))
                    error.append("  text:        %s" % text)
                    error.append("  pattern:     %s" % pattern)
                    error.append("  replacement: %s" % replacement)
                    self.logger.debug("\n".join(error))
            return output

        conn.create_function("regexp", 2, regexp)
        conn.create_function("regexp_replace", 3, regexp_replace)

        return conn

if __name__ == "__main__":
    s = SQLite()

    conn= s.connect('../../sample/VicData.sqlite')

    cursor = conn.cursor()
    # 'FEATURE_TYPE_CODE=island < br > SCALE_USE_CODE=4'
    reg = r'.*(FEATURE)_(TYPE_CODE)=(.+) <.*'
    sql = r"""

    DROP TABLE IF EXISTS tblcopy; CREATE TABLE tblcopy AS

        SELECT name n1, 
          regexp_replace(Description, '%s', '\1') as Desc1,
          regexp_replace(Description, '%s', '\2') as Desc2,
          regexp_replace(Description, '%s', '\3') as Desc3

          from vmlite_state_bdy
      ;;;
      """ % (reg, reg, reg)

    #cursor.execute("DROP TABLE IF EXISTS tblcopy")
    cursor.executescript(sql)

    cursor.execute("select * from tblcopy")
    print "OUTPUT", cursor.fetchall()

    script = """
      DROP TABLE IF EXISTS ?; CREATE TABLE ? AS
      ?
      ;
    """ 
    cursor.executescript(table, table, sql)

