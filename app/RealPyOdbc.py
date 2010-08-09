# Welcome to RealPyODBC
# Version 0.1 beta
# This class help you to connect your python script with ODBC engine.
# I need at least ctypes 0.9.2 for work.
#
# This class is not db-api 2.0 compatible. If you want to help me to do it
# please modify it and send me an e-mail with your work!
# All the comunity will thanks you.
#
# Please send bugs and reports to michele.petrazzo@unipex.it
#
# TO-DO
# Make compatibility with db-api 2.0, so add:
# apilevel, theadsafety, paramstyle, cursor, exceptions, ....
#
# From: http://unipex.it/vario/RealPyOdbc.py
#
# This software if released with MIT Licence

'''
A little example

dsn_test = 'mysql'
user = 'someuser'

od = odbc()
#Dsn list
DSN_list = od.EnumerateDSN()
od.ConnectOdbc(dsn_test, user)
#Get tables list
tables = od.GeTables()
#Get fields on the table
cols = od.ColDescr(tables[0])
#Make a query
od.Query('SELECT * FROM %s' % tables[0])
#Get results
print od.fetchmany(2)
print od.fetchall()
#Close before exit
od.close()'''

import sys, os
import ctypes

library = "/usr/lib/libodbc.so"
VERBOSE = 0    

#Costants
SQL_FETCH_NEXT = 0x01
SQL_FETCH_FIRST = 0x02
SQL_FETCH_LAST = 0x04

SQL_INVALID_HANDLE = -2
SQL_SUCCESS = 0
SQL_SUCCESS_WITH_INFO = 1
SQL_NO_DATA_FOUND = 100

SQL_NULL_HANDLE = 0
SQL_HANDLE_ENV = 1
SQL_HANDLE_DBC = 2
SQL_HANDLE_DESCR = 4
SQL_HANDLE_STMT = 3

SQL_ATTR_ODBC_VERSION = 200
SQL_OV_ODBC2 = 2

SQL_TABLE_NAMES = 3
SQL_C_CHAR = 1

#Types
SqlTypes = {0:'TYPE_NULL',1:'CHAR',2:'NUMERIC',3:'DECIMAL',4:'INTEGER', \
    5:'SMALLINT',6:'FLOAT',7:'REAL',8:'DOUBLE',9:'DATE',10:'TIME',\
    11:'TIMESTAMP',12:'VARCHAR'}

#Custom exceptions
class OdbcNoLibrary(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class OdbcLibraryError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class OdbcInvalidHandle(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class OdbcGenericError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class odbc:
    """This class implement a odbc connection. It use ctypes for work.
    """
    def __init__(self):
        """Init variables and connect to the engine"""
        self.connect = 0
        if sys.platform == 'win32':
            self.odbc = ctypes.windll.odbc32
        else:
            if not os.path.exists(library):
                raise OdbcNoLibrary, 'Library %s not found' % library
            try:
                self.odbc = ctypes.cdll.LoadLibrary(library)
            except:
                raise OdbcLibraryError, 'Error while loading %s' % library
        
        self.env_h = ctypes.c_int()
        self.dbc_h = ctypes.c_int()
        self.stmt_h = ctypes.c_int()

        self.odbc.SQLAllocHandle.restype = ctypes.c_short
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, ctypes.byref(self.env_h))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_ENV, self.env_h, ret)

        self.odbc.SQLSetEnvAttr.restype = ctypes.c_short
        ret = self.odbc.SQLSetEnvAttr(self.env_h, SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC2, 0)
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_ENV, self.env_h, ret)

        self.odbc.SQLAllocHandle.restype = ctypes.c_short
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_DBC, self.env_h, ctypes.byref(self.dbc_h))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)

    def ConnectOdbc(self, dsn, user, passwd = ''):
        """Connect to odbc, we need dsn, user and optionally password"""
        self.dsn = dsn
        self.user = user
        self.passwd = passwd

        sn = ctypes.create_string_buffer(dsn)
        un = ctypes.create_string_buffer(user)        
        pw = ctypes.create_string_buffer(passwd)
        self.odbc.SQLConnect.restype = ctypes.c_short
        ret = self.odbc.SQLConnect(self.dbc_h, sn, len(sn), un, len(un), pw, len(pw))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
        self.__set_stmt_h()
        self.connect = 1

    def GeTables(self):
        """Return a list with all tables"""
        self.__set_stmt_h()
        self.odbc.SQLTables.restype = ctypes.c_short
        #We want only tables
        t_type = ctypes.create_string_buffer('TABLE')
        ret = self.odbc.SQLTables(self.stmt_h, None, 0, None, 0, None, 0, \
            ctypes.byref(t_type), len(t_type))
        if not ret == SQL_SUCCESS:
            self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
        data = ctypes.create_string_buffer(1024)
        buff = ctypes.c_int()
        self.__bind(SQL_TABLE_NAMES, data, buff)
        return self.__fetch([data])

    def Query(self, q):
        """Make a query"""
        self.__set_stmt_h()
        self.odbc.SQLExecDirect.restype = ctypes.c_short
        ret = self.odbc.SQLExecDirect(self.stmt_h, q, len(q))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)

    def FetchOne(self):
        return self._fetch(1)
        
    def FetchMany(self, rows):
        return self._fetch(rows)

    def FetchAll(self):
        return self._fetch()

    def NumOfCols(self):
        """Get the number of cols"""
        NOC = ctypes.c_int()
        self.odbc.SQLNumResultCols.restype = ctypes.c_short
        ret = self.odbc.SQLNumResultCols(self.stmt_h, ctypes.byref(NOC))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
        return NOC.value

    def NumOfRow(self):
        """Get the number of rows"""
        NOR = ctypes.c_int()
        self.odbc.SQLRowCount.restype = ctypes.c_short
        ret = self.odbc.SQLRowCount(self.stmt_h, ctypes.byref(NOR))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
        return NOR.value        

    def ColDescr(self, table):
        """We return a list with a tuple for every col:
        field, type, number of digits, allow null"""
        self.Query("SELECT * FROM " + table)
        NOC = self.NumOfCols()
        self.odbc.SQLDescribeCol.restype = ctypes.c_short
        CName = ctypes.create_string_buffer(1024)
        Cname_ptr = ctypes.c_int()
        Ctype = ctypes.c_int()
        Csize = ctypes.c_int()
        NOdigits = ctypes.c_int()
        Allow_nuls = ctypes.c_int()
        ColDescr = []
        for row in range(1, NOC+1):
            ret = self.odbc.SQLDescribeCol(self.stmt_h, row, ctypes.byref(CName), len(CName), ctypes.byref(Cname_ptr),\
                ctypes.byref(Ctype),ctypes.byref(Csize),ctypes.byref(NOdigits), ctypes.byref(Allow_nuls))
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
            if SqlTypes.has_key(Ctype.value):
                ColDescr.append((CName.value, SqlTypes[Ctype.value],NOdigits.value,Allow_nuls.value))
            else:
                ColDescr.append((CName.value, SqlTypes[0],NOdigits.value,Allow_nuls.value))
        return ColDescr

    def EnumerateDSN(self):
        """Return a list with [name, descrition]"""
        dsn = ctypes.create_string_buffer(1024)
        desc = ctypes.create_string_buffer(1024)
        dsn_len = ctypes.c_int()
        desc_len = ctypes.c_int()
        dsn_list = []
        self.odbc.SQLDataSources.restype = ctypes.c_short
        while 1:
            ret = self.odbc.SQLDataSources(self.env_h, SQL_FETCH_NEXT, \
                dsn, len(dsn), ctypes.byref(dsn_len), desc, len(desc), ctypes.byref(desc_len))
            if ret == SQL_NO_DATA_FOUND:
                break
            elif not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                self.ctrl_err(SQL_HANDLE_STMT, stmt_h, ret)
            else:
                dsn_list.append((dsn.value, desc.value))
        return dsn_list

    def ctrl_err(self, ht, h, val_ret):
        """Method for make a control of the errors
        We get type of handle, handle, return value
        Return a raise with a list"""
        state = ctypes.create_string_buffer(5)
        NativeError = ctypes.c_int()
        Message = ctypes.create_string_buffer(1024*10)
        Buffer_len = ctypes.c_int()
        err_list = []
        number_errors = 1
        self.odbc.SQLGetDiagRec.restype = ctypes.c_short
        while 1:
            ret = self.odbc.SQLGetDiagRec(ht, h, number_errors, state, \
                NativeError, Message, len(Message), ctypes.byref(Buffer_len))
            if ret == SQL_NO_DATA_FOUND:
                #No more data, I can raise
                raise OdbcGenericError, err_list
                break
            elif ret == SQL_INVALID_HANDLE:
                #The handle passed is an invalid handle
                raise OdbcInvalidHandle, 'SQL_INVALID_HANDLE'
            elif ret == SQL_SUCCESS:
                err_list.append((state.value, Message.value, NativeError.value))
                number_errors += 1

    def close(self):
        """Call me before exit, please"""
        self.__CloseCursor()
        self.__CloseHandle()

    def __set_stmt_h(self):
        self.__CloseHandle(SQL_HANDLE_STMT, self.stmt_h)
        self.odbc.SQLAllocHandle.restype = ctypes.c_short
        ret = self.odbc.SQLAllocHandle(SQL_HANDLE_STMT, self.dbc_h, ctypes.byref(self.stmt_h))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)

    def __fetch(self, cols, NOR = 0):
        if not NOR: NOR = self.NumOfRow()
        rows = []
        self.odbc.SQLFetch.restype = ctypes.c_short
        while NOR:
            row = []
            ret = self.odbc.SQLFetch(self.stmt_h)
            if ret == SQL_NO_DATA_FOUND:
                break
            elif not ret == SQL_SUCCESS:
                self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
            for col in cols:
                row.append(col.value)
            rows.append(row)
            NOR -= 1
        return rows

    def __bind(self, col, data, buff_indicator):
        self.odbc.SQLBindCol.restype = ctypes.c_short
        ret = self.odbc.SQLBindCol(self.stmt_h, col, SQL_C_CHAR, ctypes.byref(data), \
          len(data), ctypes.byref(buff_indicator))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)

    def _fetch(self, NOR = 0):
        col_vars = []
        buff = ctypes.c_int()
        for col in range(1, self.NumOfCols()+1):
            col_vars.append(ctypes.create_string_buffer(1024))
            self.__bind(col, col_vars[col -1], buff)
        return self.__fetch(col_vars, NOR)

    def __CloseCursor(self):
        self.odbc.SQLCloseCursor.restype = ctypes.c_short
        ret = self.odbc.SQLCloseCursor(self.stmt_h)
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            self.ctrl_err(SQL_HANDLE_ENV, self.stmt_h, ret)
        return

    def __CloseHandle(self, ht='', h=0):
        self.odbc.SQLFreeHandle.restype = ctypes.c_short
        if ht:
            if not h.value: return
            ret = self.odbc.SQLFreeHandle(ht, h)
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                self.ctrl_err(SQL_HANDLE_ENV, self.stmt_h, ret)
            return
        if self.stmt_h.value:
            if VERBOSE: print 's'
            ret = self.odbc.SQLFreeHandle(SQL_HANDLE_STMT, self.stmt_h)
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                self.ctrl_err(SQL_HANDLE_ENV, self.stmt_h, ret)
        if self.dbc_h.value:
            if self.connect:
                if VERBOSE: print 'disc'
                self.odbc.SQLDisconnect.restype = ctypes.c_short
                ret = self.odbc.SQLDisconnect(self.dbc_h)
                if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                    self.ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
            if VERBOSE: print 'dbc'
            ret = self.odbc.SQLFreeHandle(SQL_HANDLE_DBC, self.dbc_h)
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                self.ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
        if self.env_h.value:
            if VERBOSE: print 'env'
            ret = self.odbc.SQLFreeHandle(SQL_HANDLE_ENV, self.env_h)
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                self.ctrl_err(SQL_HANDLE_ENV, self.env_h, ret)

