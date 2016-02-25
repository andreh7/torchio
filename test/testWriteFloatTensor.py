#!/usr/bin/env python

# tests writing a float tensor from python
# then calls torch to read it again

#----------
# generate the tensor
#----------
import numpy as np

sizes = (2,3,4)

tensor = np.ndarray(sizes)

for i1 in range(sizes[0]):
    for i2 in range(sizes[1]):
        for i3  in range(sizes[2]):
            tensor[(i1, i2, i3)] = 100 * (i1 + 1) + 10 * (i2 + 1) + (i3 + 1)

#----------
# write it out 
#----------
import tempfile

fout = tempfile.NamedTemporaryFile(suffix = ".t7")

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
import torchio

output = torchio.OutputFile(fout, 'binary')

output.writeObject(torchio.torch.FloatTensor.create(tensor))

# do NOT close in order to avoid deletion
fout.flush()

print "wrote to",fout.name
#----------
# TODO: run lua / torch to print it
#----------

# os.system("hexdump -C " + fout.name)
