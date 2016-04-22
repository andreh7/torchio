#!/usr/bin/env python


import re

import nn
import torch

from .BinaryFileReader import BinaryFileReader
import iocommon

#----------------------------------------------------------------------

def getClass(className):
    # deals with dots in the name
    parts = className.split('.')

    className = parts.pop(-1)

    module = globals()

    for moduleName in parts:
        # print "module=",module

        if isinstance(module, dict):
            module = module[moduleName]
        else:
            module = getattr(module, moduleName)
        
    return getattr(module, className)

#----------------------------------------------------------------------


class InputFile:

    #----------------------------------------
    
    def __init__(self, infile, mode):

        if isinstance(infile, str):
            # open the file ourselves, assume infile is the name
            # of a file to be opened for reading
            
            if infile.endswith(".gz"):

                import gzip
                self.infile = gzip.open(infile, "r")

            elif infile.endswith(".bz2"):
                import bz2
                self.infile = bz2.BZ2File(infile)
            
            else:
                self.infile = open(infile, "r")

        else:
            # assume infile is already an underlying file like object
            # from which we want to read
            self.infile = infile

        if mode == 'binary':
            self.reader = BinaryFileReader(self.infile)
        else:
            raise Exception("mode " + str(mode) + " not supported")

        # maps from object index to object
        self.objectCache = {}
        
    #----------------------------------------
    # methods delegated to self.reader
    #----------------------------------------

    def readInt(self):
        return self.reader.readInt()

    def readChars(self, size):
        return self.reader.readChars(size)

    def readLong(self):
        return self.reader.readLong()

    def readFloats(self, size):
        return self.reader.readFloats(size)

    def readDouble(self):
        return self.reader.readDouble()

    def readBool(self):
        return self.reader.readBool()
    
    #----------------------------------------

    def readString(self):
        length = self.readInt()

        retval = self.readChars(length)
        # print "read string",retval
        return retval
    
    #----------------------------------------

    def readTorchType(self, objectIndex):
        # must read the actual object
        versionString = self.readString()

        # print "VersionString=",versionString

        mo = re.match('^V (.*)$', versionString)

        if mo:
            versionNumber = int(mo.group(1))
            className = self.readString()

        else:
            # versioning string not used in the beginning
            className = versionString
            versionNumber = 0

        # print "className=",className

        # className = classNameMapping.get(className, className)

        
        # create an instance of this object type
        obj = getClass(className)()

        # put the object into the cache
        # note: do this before reading the members
        #       as a member may refer back to this
        #       object already
        self.objectCache[objectIndex] = obj

        # check for custom readers
        if hasattr(obj, 'customReader'):
            obj.customReader(self)

            return obj

        # default (generic) method of deserializing

        # for the moment assume that there is no
        # specialized read method for any object
        # and treat them all as a table
        tableData = self.readObject()

        # copy the attributes of the read object over
        # note that the empty object above may already
        # have been referenced while reading
        # so we can't just replace it

        # tableData is a dict here
        obj.__dict__.update(tableData)
        
        return obj
        
    #----------------------------------------    

    def readTable(self, objectIndex):
        size = self.readInt()
        obj = {}
        self.objectCache[objectIndex] = obj

        # print "Reading table of size",size
        
        for i in range(size):
            key = self.readObject()
            value = self.readObject()
            # print "key=",key,"value=",value
            obj[key] = value
            
        return obj

    #----------------------------------------
    
    def readObject(self):
        typeNumber = self.readInt()

        if typeNumber == iocommon.MAGIC_NIL:
            return None

        if typeNumber == iocommon.MAGIC_NUMBER:
            # try to convert to int if possible
            value = self.readDouble()

            # requires python >= 2.6
            if value.is_integer():
                return int(value)
            else:
                return value

        if typeNumber == iocommon.MAGIC_STRING:
            return self.readString()

        if typeNumber == iocommon.MAGIC_BOOLEAN:
            return self.readBool()

        
        # check object index
        if typeNumber in (iocommon.MAGIC_TORCH, iocommon.MAGIC_TABLE):
            objectIndex = self.readInt()

            # check the cache
            if self.objectCache.has_key(objectIndex):
                # this assumes that if an object index is appearing
                # the second time the actual object is not written after the object
                # index
                return self.objectCache[objectIndex]

        if typeNumber == iocommon.MAGIC_TORCH:
            return self.readTorchType(objectIndex)
            
        if typeNumber == iocommon.MAGIC_TABLE:
            return self.readTable(objectIndex)
        
        raise Exception("unknown type number %d" % typeNumber)

    #----------------------------------------            
