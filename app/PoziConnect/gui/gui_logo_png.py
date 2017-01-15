"""
Script generated by _generate_gui_logo.py for use in POZI Connect GUI 
"""
from StringIO import StringIO
from base64 import b64decode
imageBase64 = """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"""
imageBinary = b64decode(imageBase64)
imageStream = StringIO(imageBinary)
