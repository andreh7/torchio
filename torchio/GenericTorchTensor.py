#!/usr/bin/env python

from GenericTorchObject import GenericTorchObject

# has functionality to easily access
# tensor elements etc.
class GenericTorchTensor(GenericTorchObject):
    def __getitem__(self, indices):
        # see https://github.com/torch/torch7/blob/master/doc/tensor.md

        combinedIndex = self.storageOffset
        assert len(indices) == len(self.stride)

        for ind, strid, thisSize in zip(indices, self.stride, self.size):
            # we do NOT subtract 1 from the indices
            # to keep the python indexing convention
            assert ind >= 0
            assert ind < thisSize

            combinedIndex += ind * strid
        
        return self.storage.data[combinedIndex]

    #----------------------------------------

    def linearToIndices(self, linearIndex):
        retval = []
        for thisStride in self.stride:
            retval.append(linearIndex // thisStride)
            linerIndex = linearIndex % thisStride

    #----------------------------------------

    def customReader(self, inputFile):
        # for torch.CudaTensor, the next few numbers are the dimensions ?!
        # see e.g. ~/torch/extra/cutorch/torch/generic/Tensor.c : int torch_Tensor_(read)

        self.dimension = inputFile.readInt()
        self.size      = [ inputFile.readLong() for dim in range(self.dimension) ]
        self.stride    = [ inputFile.readLong() for dim in range(self.dimension) ]

        # TODO: the torch version decreases this by one because lua
        #       indices start at 1 . We do the same here.

        self.storageOffset = inputFile.readLong() - 1

        self.storage = inputFile.readObject()

    #----------------------------------------

    def customWriter(self, outputFile):

        print "in customWriter"
        
        outputFile.writeInt(self.dimension)
        outputFile.writeLongs(self.size)
        outputFile.writeLongs(self.stride)

        # TODO: the torch version decreases this by one because lua
        #       indices start at 1 when reading. When writing
        #       we must to the opposite
        outputFile.writeLong(self.storageOffset + 1)

        # must be implemented in inheriting classes
        self.writeStorage(outputFile)

    #----------------------------------------
    
    def asndarray(self):
        # TODO: see http://stackoverflow.com/questions/4365964/numpy-efficiently-reading-a-large-array
        #       instead of reading things to memory, we could leave them memory mapped ?

        import numpy as np

        # note: this does not make a copy (?!)
        return np.asarray(self.storage.data).reshape(self.size)

    #----------------------------------------        
