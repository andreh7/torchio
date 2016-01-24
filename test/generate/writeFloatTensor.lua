#!/usr/bin/env th

-- ----------
-- create and fill a tensor
-- ----------

sizes = { 2,3,4 }

tensor = torch.FloatTensor(sizes[1], sizes[2], sizes[3])

for i1 = 1,sizes[1] do
  for i2 = 1,sizes[2] do
    for i3 = 1,sizes[3] do
       tensor[{i1, i2, i3}] = 100 * i1 + 10 * i2 + i3
    end
  end

end 

-- ----------
-- write the tensor to a file
-- ----------

-- similar structure than example 2 from the tutorial
-- (except the 'size' function)

torch.save("../data/floatTensor-binary.t7", tensor, "binary")
torch.save("../data/floatTensor-ascii.t7",  tensor, "ascii")

