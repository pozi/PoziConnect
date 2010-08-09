# testing a simple xor encryption/decryption
# tested with Python24      vegaseat    02oct2005
# Original Source: http://www.daniweb.com/code/snippet216632.html

import StringIO
import operator
import re
from base64 import b64encode, b64decode

# PlaceLab's modules
from logger import *

class Crypt:
    def __init__(self, options = {}):
        loggerName = 'CryptXOR'
        if 'logger' in options:
            logger = options.get('logger')
            self.logger = logger.clone(loggerName) 
        else:
            self.logger = Logger(loggerName)

        # Store default options first
        self.options = {
            'password': 'xkcd',
            'prefix': '!PL!',
            'postfix': '!',
            'base64test': '(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?', #Example: =PL=GRsTFA4TEQ4=
        }

        # Then merge provided options with the default ones
        self.options.update(options) 

        self.regexp = self.options.get('prefix', '') + self.options.get('base64test', '') + self.options.get('postfix', '')

    def Encrypt(self, string):
        self.logger.debug('Encrypt', string)
        password = self.options.get('password')
        encrypted = self.CryptXOR(string, password)
        output = self.options.get('prefix', '') + b64encode(encrypted) + self.options.get('postfix', '')
        self.logger.debug('Encrypted: ', output)
        return output

    def Decrypt(self, string, hidePassword = False):
        self.logger.debug('Decrypt', string)

        output = string

        if self.IsPassword(string):
            self.logger.debug("Is a password", string)
            password = self.options.get('password')

            string = string.lstrip(self.options.get('prefix', ''))
            string = string.rstrip(self.options.get('postfix', ''))

            output = self.CryptXOR(b64decode(string), password)
            self.logger.debug('Decrypted: ', output)

        elif self.ContainsPassword(string):
            self.logger.debug("Contains passwords", string)

            for password in re.findall(self.regexp, output):
                decrypted = "******" if hidePassword else self.Decrypt(password) 
                output = output.replace(password, decrypted)

        self.logger.debug('Decrypted: ', output)
        return output

    def IsPassword(self, string):
        self.logger.debug('isEncrypted', string)

        # Force match to be from start to end
        regexp = '^' + self.regexp + '$'

        if re.match(regexp, string):
            return True
        else:
            return False

    def ContainsPassword(self, string):
        self.logger.debug('ContainsPassword', string)
        if re.search(self.regexp, string):
            return True
        else:
            return False

    
    def CryptXOR(self, string, pw):
        """
        cryptXOR(filename, pw) takes the string and xor encrypts/decrypts it against the password pw
        """
        # create two streams in memory the size of the string str2
        # one stream to read from and the other to write the XOR crypted character to
        sr = StringIO.StringIO(string)
        sw = StringIO.StringIO(string)
        # make sure we start both streams at position zero (beginning)
        sr.seek(0)
        sw.seek(0)
        n = 0
        #str3 = ""  # test
        for k in range(len(string)):
            # loop through password start to end and repeat
            if n >= len(pw) - 1:
                n = 0
            p = ord(pw[n])
            n += 1
            
            # read one character from stream sr
            c = sr.read(1)
            b = ord(c)
            # xor byte with password byte
            t = operator.xor(b, p)
            z = chr(t)
            # advance position to k in stream sw then write one character
            sw.seek(k)
            sw.write(z)
            #str3 += z  # test
        # reset stream sw to beginning
        sw.seek(0)

        output = sw.read()

        # clean up
        sr.close()
        sw.close()

        return output
    
# allows cryptXOR() to be used as a module
if __name__ == '__main__':

    crypt = Crypt()

    str1 = "applepie"
    str2 = "muffin"

    # let's use a fixed password for testing
    password = "nixon"
   
    #print "String:", str1
    #print "password:", password

    # encrypt the text file to "Music101.txp" (check with an editor, shows a mess)
    #encrypted =  b64encode(cryptXOR(str1, password))
    encrypted =  crypt.Encrypt(str1)
    encrypted2 =  crypt.Encrypt(str2)
    
    #print "encrypted:", encrypted

    print "iscrypted:", crypt.IsPassword(encrypted)
    sentence = " fsakjkdjf kadsjf" + encrypted+ "asfadsf" + encrypted2

    #print "has crypted:", crypt.ContainsPassword(" fsakjkdjf kadsjf" + encrypted+ "asfadsf")
    print "DECRYPTED:", crypt.Decrypt(sentence, False)

    # decrypt the text file back to "Music101.txt" (check with an editor, normal text again)
    #decrypted = cryptXOR(b64decode(encrypted), password)
    decrypted =  crypt.Decrypt(encrypted)
    print "decrypted:", decrypted
    decrypted2 =  crypt.Decrypt(encrypted2)
    print "decrypted2:", decrypted2

    print "ASFASF",  Crypt().Encrypt(str1)

