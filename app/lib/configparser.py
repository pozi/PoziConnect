#!/usr/bin/env python

# Make app dir available to the sys path
import sys
sys.path.extend(['.', '..', 'lib'])

import iniparse
import logging
import os
import re
import StringIO

from logger import *

class ConfigParser(iniparse.RawConfigParser):
    def __init__(self, options = {}):
        super(ConfigParser, self).__init__()

        # Store default options first
        self.options = {
            'lowerKeys': False,
            'booleaniseValues': True,
            'globalSections': ['Settings']
        }

        # Then merge provided options with the default ones
        self.options.update(options)

        # Preserve the case for keywords 
        # (ie: 'InputDir' does not change into 'inputdir') 
        self.optionxform = str 

        #if self.options.get('configFile'):
            #self.read(self.options['configFile'])

        loggerName = 'ConfigParser'
        if 'logger' in options:
            logger = options.get('logger')
            self.logger = logger.clone(loggerName) 
        else:
            self.logger = Logger(loggerName)

    def items(self, section, recurse = False):
        items = Items(super(ConfigParser, self).items(section))

        self.logger.debug(items)

        # Loop through all global sections and incrementally
        # build up the vars dictionary by:
        # - First getting the vars from first global section
        # - Then substituting vars from the next section with 
        #   the vars from the previous section until we have
        #   had all sections
        # We add the recurse option to prevent infinite recursion
        vars = self.GetGlobalVars() if not recurse else {}

        # Replace add variables from within the section
        # to the dictionary of vars too. They have 
        # precedence over any previously defined vars
        for index, item in enumerate(items):

            # Replace vars from within own section
            itemsVars = items[:] #copy items

            itemsVars.pop(index) #take out current item
            item = item.SubstituteVars(itemsVars)

            # Do normal variable substitution
            item = item.SubstituteVars(vars)

            if self.options.get('booleaniseValues'):
                item = item.Booleanise()

            if self.options.get('lowerKeys'):
                item = item.lowerKey() 

            items[index] = item

        # Booleanise values 
        """
        if self.options.get('booleaniseValues'):
            for item in items:
                self.logger.info(item, item.Booleanise)
            self.logger.info([item.Booleanise for item in items])
            self.logger.info(map(lambda x: x.Booleanise, items))
            items = Items([item.Booleanise for item in items])
"""
        # Make the 'keys' lower case
        #if not self.options.get('lowerKeys'):
            #items = [(k.lower(), v) for k,v in items]

        return items

    #def sections(self):
        #sections = Sections(super(ConfigParser, self).sections())
        #return sections

    def GetGlobalSections(self):
        return self.GetOption('globalSections', [])

    def GetGlobalVars(self):
        vars = {}
        for globalSection in self.GetGlobalSections():

            # Continue if config does not have this global section
            if not self.has_section(globalSection):
                continue

            # Get items for this global section and
            # add recurse = True to prevent infinite looping
            items = self.items(globalSection, True)

            # Perform variable substitution using vars that
            # have been gathered from previous section(s)
            items = items.SubstituteVars(vars)

            vars.update(items)
        return vars 

    def GetOption(self, option, default = None):
        #self.logger.info("OPTIONS", self.options, option)
        return self.options.get(option, default)

    def SetOption(self, option, value = None):
        self.options[option] = value

    def SubstituteVars(self, vars):
        #self.logger.info("SubstituteVars", vars)

        # Create a new config and fill it 
        # with substituted variables
        config = self.__class__(self.options)

        # Loop through all sections and 
        # fill new config with sections and
        # it's items with subtituted variables
        for section in self.sections():
            self.logger.debug("Section:", section)
            config.add_section(section)
            items = self.items(section)
            for index, item in enumerate(items):
                key, value = item #extract key & value
                config.set(section, key, value) #store
        return config

    def ToString(self):
        # Create a file-like object so we can read/write 
        # Config2 into/from a string
        strio = StringIO.StringIO()

        vars = self.GetGlobalVars()
        clone = self.SubstituteVars(vars)
        clone.write(strio) # write config to StringIO object
        configString = strio.getvalue() # get config as a string
        return configString

    # Make nice printable version of object
    def __str__(self):
        return self.ToString() 

class Item(tuple):
    def __init__(self, item):
        super(Item, self).__init__()
        #self.logger.info("Init: Item", item )

    def SubstituteVars(self, vars):
        # Force vars to be a dictionary
        vars = dict(vars)

        # Get key and value
        key, value = self

        # Replace variables like {OutputFolder} with their corresponding
        # value in the vars dictionary. Uses a regular expression (re)
        # Returns a list of tuples like ("{OutputFolder}", "OutputFolder")
        # Note: We force value to be string since it could be a boolean
        for match in re.finditer(r'({(.+?)})',str(value)): 
            varBracket, varPlain = match.groups()
            if varPlain in vars:
                value = value.replace(varBracket, vars.get(varPlain))
        return Item((key, value))

    def Booleanise(self):

        false = ['false', 'no', 'off', 'disable']
        true = ['true', 'yes', 'on', 'enable']
            
        key, value = self

        value2 = str(value).strip().lower()
        if value2 in false:
            return Item((key, False))
        elif value2 in true:
            return Item((key, True))
        else:
            return Item(self)

    def lowerKey(self):
        key, value = self
        return Item((key.lower(), value))
 
class Items(list):
    def __init__(self, items):

        # Transform all items into our own item classes
        items = map(Item, items)

        super(Items, self).__init__(items)

    def SubstituteVars(self, vars):
        #self.logger.info("SubstituteVars", vars)
        items = []
        for item in self:
            items.append(item.SubstituteVars(vars))
        return items

    def LowerKeys(self):
        items = Items([(k.lower(), v) for k,v in self])
        return items


#class Sections(list):
    #def __init__(self, sections):
        ##self.logger.info("Init: SECTIONS:", sections )
        #super(Sections, self).__init__(sections)

#for i in re.finditer(r'({(.+?)})',s): s1, s2 = i.groups(); self.logger.info(s1, ":", s2; s0 = s0.replace(s1, d.get(s2)))

if __name__ == "__main__":
    d = {'a': 'b', 'Pathway_Settings': 'pathwaysettings', 'Pathway_DSN': 'pathwaydsnyeah'}

    f = '../../config/button.ini'
    f = '../../PlaceLab.ini'
    options = {
        #'configFile': f,
#        'globalSections': ['Settings']
        'globalSections': ['Settings', 'User Settings', 'Application Settings']

        }
    #options = {}

    #items = Items( [('a', 'b')])
    #self.logger.info(items)
    #sys.exit()
    c = ConfigParser(options)
    c.read(f)

    logger = c.logger

    logger.debug("GET option", c.GetOption('globalSections'))

    #c2 = c.SubstituteVars(d)
    logger.info("*=" * 40)
    logger.info(c)
    logger.info("*=" * 40)
    logger.info(c.items('ENV'))

    """
    for section in c.sections():
        logger.info("SECTION:", section)
        logger.info("----------------------")
        items = c.items(section)
        logger.info("items:", items, len(items))
        logger.info("subs", items.SubstituteVars(d))
    """

    #logger.info("config", c, c.sections(), c.items('Settings'))
    sys.exit()

