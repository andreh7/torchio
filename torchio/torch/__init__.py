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

#----------------------------------------------------------------------

class LongStorage(GenericTorchObject):

    def customReader(self, inputFile):
        # see e.g. int torch_Storage_(read) in ~/torch/extra/cutorch/torch/generic/Storage.c
        self.size = inputFile.readLong()
        # not sure whether this is right but seems to work
        self.data = [ inputFile.readLong() for i in range(self.size) ]


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
