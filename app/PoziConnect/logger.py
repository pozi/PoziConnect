from copy import copy, deepcopy
import logging
import os
import sys


LOG_DIR = 'output'  # get from ini file?
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
  

fileName = os.path.join(LOG_DIR, 'PoziConnect.log')

formatters = {}
formatters['console'] = '%(name)-15s: %(levelname)-8s %(message)s'
formatters['file'] = '%(asctime)s - %(name)-15s - %(levelname)s - %(message)s'

isExe = hasattr(sys, "frozen")

logLevel = logging.INFO
#logLevel = logging.DEBUG
if isExe:
    logLevel = logging.INFO


# set up logging to file - see previous section for more details
logging.basicConfig(level=logLevel,
                    format=formatters.get('file'),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=fileName,
                    filemode='w'
                    )

if not isExe:
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    # tell the handler to use this format
    console.setFormatter(logging.Formatter(formatters.get('console')))

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

# a simple class with a write method
class Logger:
    def __init__(self, name = 'root', fileName = ''):
       
        # set a format which is simpler for console use
        self.fileName = fileName

        self.logger = logging.getLogger(name)

    def clone(self, name = '' ):
        clone = Logger(name, self.fileName) 
        #if self.fileName:
            #clone.SetFile(self.fileName)
        return clone

    def SetFile(self, fileName):
        if hasattr(self, 'fileName') or not fileName:
            return

        self.fileName = fileName

        #fh = logging.FileHandler(fileName)
        #fh.setLevel(logging.DEBUG)
        #fh.setFormatter(logging.Formatter(self.formatters.get('file')))
        #self.logger.addHandler(fh)

    def ArgsToString(self, args):
        strArgs = map(str, args)
        string = " ".join(strArgs)
        if '\n' in string:
            string = '\n\n' + string
        return string

    def write(self, *args):
        string = self.ArgsToString(args)
        self.logger.info(string)

    def debug(self, *args):
        string = self.ArgsToString(args)
        self.logger.debug(string)
 
    def info(self, *args):
        string = self.ArgsToString(args)
        self.logger.info(string)
 
    def warn(self, *args):
        string = self.ArgsToString(args)
        self.logger.warn(string)
 
    def error(self, *args):
        string = self.ArgsToString(args)
        self.logger.error(string)
 
    def critical(self, *args):
        string = self.ArgsToString(args)
        self.logger.critical(string)
 
# example with redirection of sys.stdout
if __name__ == "__main__":
    logger = Logger('log.txt')                  # a writable object
    sys.stdout = logger                         # redirection
    print "TESTING"


