from distutils.core import setup
from PoziConnect.version import version
import os
import sys

sys.path.extend(['app'])
sys.path.extend(['app/external'])

VERSION = version
APP_DIR = os.path.dirname(__file__)

# Increase version minor number automatically
if VERSION:
    vList = version.split('.')
    minor = vList[-1]
    newMinor = int(minor) + 1
    vList[-1] = str(newMinor)
    VERSION = '.'.join(vList)

print "\nPrevious version number is: %s" % version
VERSION = raw_input('\nGive new version number (default: %s): ' % VERSION) or VERSION

if VERSION is not version:
    print "NEW VERSION! Writing to version.py"
    versionModule = "version = '%s'\n" % VERSION
    versionFile = open(os.path.join(APP_DIR, 'PoziConnect\\version.py'), 'w')

    versionFile.write(versionModule)
    versionFile.close()

import py2exe

COMPANY_NAME = 'Groundtruth Mapping Systems'
COPYRIGHT = '(c) 2010 ' + COMPANY_NAME
AUTHOR_NAME = 'Groundtruth Mapping Systems & Something Spatial'
AUTHOR_EMAIL = 'info@groundtruth.com.au'
AUTHOR_URL = "http://groundtruth.com.au/placelab"
PRODUCT_NAME = "Pozi Connect"
SCRIPT_MAIN = os.path.join(APP_DIR, 'PoziConnect.py')
VERSIONSTRING = PRODUCT_NAME + " BETA " + VERSION
ICON_FILE = os.path.join(APP_DIR, 'PoziConnect\gui\PlaceLabIcon.ico')

MODULE_INCLUDES =[
    #'base64',
    'wx',
    'iniparse',
    'agw',
    'RealPyOdbc'
]

MODULE_EXCLUDES =[
    #'email',
    'AppKit',
    'Foundation',
    'bdb',
    'difflib',
    'tcl',
    'Tkinter',
    'Tkconstants',
    'curses',
    'distutils',
    'setuptools',
    #'urllib',
    #'urllib2',
    'urlparse',
    'BaseHTTPServer',
    '_LWPCookieJar',
    '_MozillaCookieJar',
    'ftplib',
    'gopherlib',
    '_ssl',
    #'htmllib',
    #'httplib',
    'mimetools',
    'mimetypes',
    'rfc822',
    'tty',
    #'webbrowser',
    #'socket',
    'hashlib',
    #'base64',
    'compiler',
    'pydoc'
]

setup(
    windows = [
        { "script":SCRIPT_MAIN,
          "icon_resources":[(1, ICON_FILE)]
        }
    ],
    console = [SCRIPT_MAIN],
    #data_files = [('images', [LOGO_FILE])],
    options = {"py2exe": {
                        "optimize": 2,
                        "includes": MODULE_INCLUDES,
                        "compressed": 1,
                        "ascii": 1,
                        "bundle_files": 1, #1=all, 2=all except python interpreter
                        "ignores": ['tcl','AppKit','Numeric','Foundation'],
                        "excludes": MODULE_EXCLUDES,
                        "includes":'decimal',
                        }
               },
    name = PRODUCT_NAME,
    version = VERSION,
    #company_name = COMPANY_NAME,
    #copyright = COPYRIGHT,
    author = AUTHOR_NAME,
    author_email = AUTHOR_EMAIL,
    url = AUTHOR_URL,
    zipfile = None,
)
