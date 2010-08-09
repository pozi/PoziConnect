from logger import *
from OGR import *

import RealPyOdbc

#####################################################
# Helper functions
#####################################################

# Helper function for executing system calls
def system(command):
    OGRBase().ExecuteCommand(command.split(' '))

# DSNList shows a list of DSNs (only on Windows machines)
def DSNList():
    logger = OGRBase().logger

    odbc = RealPyOdbc.odbc()
    dsnlist = odbc.EnumerateDSN()
    output = "#" * 60 + "\n#" + " DSN List \n" + "#" * 60 + "\n"

    # Calculate max width of DSN names
    maxwidth = max([len(k) for k,v in dsnlist])
    spacing = maxwidth + 2
    for dsn, driver in dsnlist:
        # format output to have a nice looking 2 column layout
        output += ("%-" + str(spacing) + "s (%s)\n") % (dsn, driver)
    logger.info(output)

# DSNTables shows a list of tables for a given DSN (only on Windows machines)
# The 'user' parameter is optional
def DSNTables(dsn, user = ""):
    logger = OGRBase().logger

    odbc = RealPyOdbc.odbc()
    odbc.ConnectOdbc(dsn, user)
    dsntables = odbc.GeTables()
    output = "#" * 60 + "\n#" + " DSN Tables for DSN: \"%s\" \n" % (dsn) + "#" * 60 + "\n"

    for table in sorted(dsntables):
        output += " - %s\n" % (table[0])
    logger.info(output)


