#!/usr/bin/env python

import struct

class BinaryFileWriter:

    def __init__(self, outfile):

        self.outfile = outfile

    #----------------------------------------

    def writeInt(self, value):
        # writes a single integer
        # (currently only native endianness is supported)
        # assume 32 bit integers

        # default is native order
        self.outfile.write(struct.pack('i', value))

    #----------------------------------------

    def writeDouble(self, value):
        # writes a single double
        # (currently only native endianness is supported)
        # assume 32 bit integers

        # default is native order
        self.outfile.write(struct.pack('d', value))

    #----------------------------------------

    def writeDoubles(self, data):
        # default is native order
        self.outfile.write(struct.pack('d' * len(data), *data))

    #----------------------------------------

    def writeBytes(self, data):
        # default is native order
        self.outfile.write(struct.pack('B' * len(data), *data))

    #----------------------------------------

    def writeLong(self, value):
        # assume 64 bit longs

        # default is native order
        self.outfile.write(struct.pack('l', value))

    #----------------------------------------

    def writeLongs(self, values):
        # assume 64 bit longs

        # default is native order
        self.outfile.write(struct.pack('l' * len(values), *values))

    #----------------------------------------

    def writeBool(self, value):
        if value:
            self.writeInt(1)
        else:
            self.writeInt(0)
    
    #----------------------------------------
    
    def writeChars(self, text):
        # TODO: is this really necessary, can't we just write the string out ?!
        self.outfile.write(struct.pack('c' * len(text), *text))

    #----------------------------------------

    def writeFloats(self, data):
        self.outfile.write(struct.pack('f' * len(data), *data))
    #----------------------------------------
