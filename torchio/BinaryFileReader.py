#!/usr/bin/env python

import struct

class BinaryFileReader:    
    def __init__(self, infile):
        self.infile = infile

    def readInt(self):
        # reads a single integer
        # (currently only native endianness is supported)
        # assume 32 bit integers

        # default is native order
        return struct.unpack('i', self.infile.read(4))[0]

    def readDouble(self):
        # reads a single double
        # (currently only native endianness is supported)
        # assume 32 bit integers

        # default is native order
        return struct.unpack('d', self.infile.read(8))[0]

    def readDoubles(self, size):
        # default is native order
        return struct.unpack('d' * size, self.infile.read(8 * size))

    def readBytes(self, size):
        # default is native order
        return struct.unpack('B' * size, self.infile.read(1 * size))



    def readLong(self):
        # assume 64 bit longs

        # default is native order
        return struct.unpack('l', self.infile.read(8))[0]

    def readBool(self):
        return self.readInt() == 1

    
    #----------------------------------------
    
    def readChars(self, size):
        return struct.unpack(str(size) + 's', self.infile.read(size))[0]

    #----------------------------------------

    def readFloats(self, size):
        return struct.unpack('f' * size, self.infile.read(4 * size))
    #----------------------------------------
