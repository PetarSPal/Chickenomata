# from itertools import combinations

# print(list("".join(x) for x in product('01', repeat=3)))
import numpy as np
row=[0]*320
data = np.array(row)
data = np.zeros([5,5,5])
in_system = 2
neighbors = 5


# str_prod = product("".join(map(str, range(in_system))), repeat=neighbors)
# str_prod = tuple("".join(x) for x in str_prod)
from itertools import product, chain, cycle
# int_prod = product(range(in_system), repeat=neighbors)
# cchainprod = cycle(chain(*int_prod))
# row = [next(cchainprod) for _ in range(len(row))]
# print(row)

int_prod = product(range(in_system), repeat=neighbors)
cchainprod = cycle(chain(*int_prod))
# data[:] = np.array([next(cchainprod) for _ in np.ndenumerate(data)]).reshape(data.shape)

data = np.fromiter(cchainprod, dtype=data.dtype, count=data.size).reshape(data.shape)

# it = np.nditer(data, flags=['multi_index'], op_flags=['writeonly'])
# for x in it:
#     x[...] = next(cchainprod)
    
    
# data[:] = np.vectorize(lambda _, next_val: next(next_val))(None, cchainprod).reshape(data.shape)

# data[:] = np.fromiter((next(cchainprod) for _ in np.ndindex(data.shape)), dtype=data.dtype).reshape(data.shape)

# for index,_ in np.ndenumerate(data):
#     data[index] = next(cchainprod)

print(data)


# print(int_prod)

# print(tuple(int_prod))








# for i in range(0, len(row)-neighbors+1, neighbors):
#     for j in range(neighbors):
#         row[i + j] = int_prod[(i // neighbors) % len(int_prod)][j]
    

