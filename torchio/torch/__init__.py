#!/usr/bin/env python

from ..GenericTorchTensor import GenericTorchTensor
from ..GenericTorchObject import GenericTorchObject

#----------------------------------------------------------------------

class CudaTensor(GenericTorchTensor):
    pass

#----------------------------------------------------------------------

class DoubleTensor(GenericTorchTensor):
    pass

#----------------------------------------------------------------------

class FloatTensor(GenericTorchTensor):

    # create a FloatTensor object from an ndarray
    # (which can then be serialized)
    # 
    # note that this DOES make a copy of the
    # given ndarray for the moment
    @staticmethod
    def create(data):
        # data must be a numpy.ndarray like object

        import numpy as np

        retval = FloatTensor()
        
        retval.dimension = len(data.shape)
        retval.size = tuple(data.shape) # make a copy to be sure


        # we re-use the stride parameters of the given nparray
        # data.stride however is in units of bytes, not
        # in units

        # guess the stride parameters from whether it's
        # C or Fortran contiguous

        if data.flags.c_contiguous:
            # set this such that the stride of the last coordinate
            # is one, the second last is the size of the last coordinate
            # etc.
            #
            # for example: sizes = [ 2, 3, 4 ] should give strides = [ 12, 4, 1 ]
            retval.stride = np.cumprod([1] + list(retval.size)[::-1])[-2::-1]

            # flatten(..) actually makes a copy
            retval.storage = FloatStorage()
            retval.storage.data = data.flatten(order ='C').astype('f')
            retval.storage.size = len(retval.storage.data)

        else:
            raise Exception('only C contiguous ndarrays are supported for the moment')

        retval.storageOffset = 0

        return retval

    #----------------------------------------
    def writeStorage(self, outputFile):
        
        outputFile.writeObject(self.storage)
        
    
#----------------------------------------------------------------------

class IntTensor(GenericTorchTensor):
    pass
    
#----------------------------------------------------------------------

class ByteTensor(GenericTorchTensor):
    pass

#----------------------------------------------------------------------
    
class CudaStorage(GenericTorchObject):

    def customReader(self, inputFile):
        # see e.g. int torch_Storage_(read) in ~/torch/extra/cutorch/torch/generic/Storage.c
        self.size = inputFile.readLong()
        self.data = inputFile.readFloats(self.size)

#----------------------------------------------------------------------

class FloatStorage(GenericTorchObject):

    def customReader(self, inputFile):
        # same as for CudaStorage 
        # see e.g. int torch_Storage_(read) in ~/torch/extra/cutorch/torch/generic/Storage.c
        self.size = inputFile.readLong()
        self.data = inputFile.readFloats(self.size)

    def customWriter(self, outputFile):
        outputFile.writeLong(self.size)
        outputFile.writeFloats(self.data)
        
#----------------------------------------------------------------------

class LongStorage(GenericTorchObject):

    def customReader(self, inputFile):
        # see e.g. int torch_Storage_(read) in ~/torch/extra/cutorch/torch/generic/Storage.c
        self.size = inputFile.readLong()
        # not sure whether this is right but seems to work
        self.data = [ inputFile.readLong() for i in range(self.size) ]

#----------------------------------------------------------------------

class IntStorage(GenericTorchObject):

    def customReader(self, inputFile):
        # see e.g. int torch_Storage_(read) in ~/torch/extra/cutorch/torch/generic/Storage.c
        self.size = inputFile.readLong()
        # not sure whether this is right but seems to work
        self.data = [ inputFile.readInt() for i in range(self.size) ]


#----------------------------------------------------------------------
class DoubleStorage(GenericTorchObject):

    def customReader(self, inputFile):
        # see e.g. int torch_Storage_(read) in ~/torch/extra/cutorch/torch/generic/Storage.c
        self.size = inputFile.readLong()
        self.data = inputFile.readDoubles(self.size)

#----------------------------------------------------------------------
class ByteStorage(GenericTorchObject):

    def customReader(self, inputFile):
        # see e.g. int torch_Storage_(read) in ~/torch/extra/cutorch/torch/generic/Storage.c
        self.size = inputFile.readLong()
        self.data = inputFile.readBytes(self.size)

#----------------------------------------------------------------------
