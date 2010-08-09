
import os
import StringIO
import sys
from base64 import b64encode, b64decode

imageFileName = sys.argv[1]
imageFileName = sys.argv[1]

if not imageFileName:
    print "provide image file"
    sys.exit()

print imageFileName

infile = open(imageFileName, 'rb');
binImage = infile.read()
infile.close()
base64Image = b64encode(binImage)

outputString = """

from StringIO import StringIO
from base64 import b64decode

imageBase64 = \"""%s\"""

imageBinary = b64decode(imageBase64)

imageStream = StringIO(imageBinary)

""" % base64Image

outFileName = imageFileName.replace(' ', '_')
outFileName = outFileName.replace('.', '_')
outfile = open(outFileName + '.py', 'w')
outfile.write(outputString)
outfile.close()
