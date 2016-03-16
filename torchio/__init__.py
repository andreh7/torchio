#!/usr/bin/env python

# from .torchio import *

from .InputFile        import InputFile
from .BinaryFileReader import BinaryFileReader

from .OutputFile       import OutputFile
from .BinaryFileWriter import BinaryFileWriter


#----------------------------------------------------------------------
def read(fname, mode = "binary"):
    """reads an object from the given file name"""
    
    fin = InputFile(fname, mode)

    return fin.readObject()

#----------------------------------------------------------------------
    
