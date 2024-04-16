import numpy as np

from scipy import ndimage

# a = np.zeros((3,3), dtype=bool)
# a[1,1] = 1
# for i in a
# print(a)


class neighboohood():
    def __init__(self) -> None:
        pass
    
    
# starts at shape 3,3,3, ... ndim
# This is to capture the center and it's R1 neighbors
# Mutated with defined rule N times
# Shape adjusts to fit the data (border must have only 0s)
# When used offset by the coordinate to center
# When used add wrap/nowrap handling

#Problem -> we define neighborhood via CA
#To define the neighborhood we must define the neighborhood to define the CA
#Confusing

#Problem -> I thought of using a sparse array to capture the entire dataset
#However that would result in a lot of unecessary computation if we handle it element by element
#That doesn't mean it's entirelly not viable
#There's possible strategies to approach this
#For example one possibility would be only working on elements with value >0
#Then capturing the element's neighbors and working on the neighbors

#I don't know which is the better approach






# from numpy import array, argwhere

# A = array([[0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 1, 0, 0, 0, 0],
#            [0, 0, 1, 1, 0, 0, 0],
#            [0, 0, 0, 0, 1, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0]])

# A = array([[[0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 1, 0, 0, 0, 0],
#            [0, 0, 1, 1, 0, 0, 0],
#            [0, 0, 0, 0, 1, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0]],
#            [[0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 1, 0, 0, 0, 0],
#            [0, 0, 1, 1, 0, 0, 0],
#            [0, 0, 0, 0, 1, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0]],
#            [[0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 1, 0, 0, 0, 0],
#            [0, 0, 1, 1, 0, 0, 0],
#            [0, 0, 0, 0, 1, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0]]])


# B = argwhere(A)

# # print(B.min())

# (ystart, xstart, zstart), (ystop, xstop, zstop) = B.min(0)-1, B.max(0) + 2
# Atrim = A[ystart:ystop, xstart:xstop, zstart:zstop]

# print((ystart, xstart, zstart), (ystop, xstop, zstop))

# print(Atrim)

# print(A[0][0])

# def bbox2(img):
#     zax = np.any(img, axis=2)
#     rows = np.any(img, axis=1)
#     cols = np.any(img, axis=0)
#     zmin, zmax = np.where(zax)[0][[0, -1]]
#     ymin, ymax = np.where(rows)[0][[0, -1]]
#     xmin, xmax = np.where(cols)[0][[0, -1]]
#     print(zax, zmin, zmax)
#     print(rows, ymin, ymax)
#     print(cols, xmin, xmax)
#     return img[zmin:zmax+1, ymin:ymax+1, xmin:xmax+1]

# print(A)
# print(bbox2(A))

# an = np.any(A, axis=0)
# a = np.any(an, axis=0)
# b = np.any(an, axis=1)
# print(a)
# print(b)

# t = np.any(A, axis=1)
# c = np.any(t, axis=1)
# print(c)

# slices = np.where(A == 1)
# print(slices)
# print(A[slices])


# struct = ndimage.generate_binary_structure(2, 1).astype(int)
# struct = np.array([[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],
#     [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]],
#     [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]])

# print(struct)
# struct = ndimage.iterate_structure(struct, 2).astype(int)
# print(struct)


# print(int('101',2)^int('1010',2))



import numpy as np

from scipy.sparse import coo_array

# a = coo_array((3, 4), dtype=np.uint32).toarray()


# row  = np.array([0, 3, 1, 0])
# col  = np.array([0, 3, 1, 2])
# data = np.array([4, 5, 7, 9])
# a = coo_array((data, (row, col)), shape=(4, 4)).toarray()

def _von_neumann_1(data, coord):
    ##Hardcoded wrap -> decouple
    idx = tuple(tuple((el+d) % data.shape[0] if idx2 == idx else el 
                    for idx2,el in enumerate(coord))
                    for idx in range(len(coord))
                    for d in [-1,1])
    print(idx)
    return tuple(data[i] for i in idx)


def _moore_1(data, coord):
    ##Hardcoded wrap -> decouple
    for d in [-1,0,1]:
        for dim in range(len(coord)):
            for moord in tuple(c+d % data.shape[0] for c in coord[:dim+1]):
    # idx = tuple(tuple((el+d) % data.shape[0] if idx2 == idx else el 
    #                 for idx2,el in enumerate(coord))
    #                 for idx in range(len(coord))
    #                 for d in [-1,0,1])
    print(idx)
    return tuple(data[i] for i in idx)


a = np.repeat(0, 150*150).reshape(150, 150)
a[150//2, 150//2] = 1
# print(a)

_moore_1(np.zeros((3,3,3)), (1,1,1))

# _von_neumann_1(np.zeros((3,3,3)), (1,1,1))


# cp = a.copy()
# for idx, el in np.ndenumerate(a):
#     if sum(_moore_1(a, idx)) > 0:
#         cp[idx] = 1
# a[:] = cp


# cp = a.copy()
# for idx, el in np.ndenumerate(a):
#     if sum(_von_neumann_1(a, idx)) > 0:
#         cp[idx] = 1
# a[:] = cp

# cp = a.copy()
# for idx, el in np.ndenumerate(a):
#     if sum(_von_neumann_1(a, idx)) > 0:
#         cp[idx] = 1
# a[:] = cp


# cp = np.zeros(a.shape)
# for idx, el in np.ndenumerate(a):
#     if sum(_von_neumann_1(a, idx)) > 0:
#         cp[idx] = 1
# a[:] = cp

# cp = np.zeros(a.shape)
# for idx, el in np.ndenumerate(a):
#     if sum(_von_neumann_1(a, idx)) > 0:
#         cp[idx] = 1
# a[:] = cp

# cp = np.zeros(a.shape)
# for idx, el in np.ndenumerate(a):
#     if sum(_von_neumann_1(a, idx)) > 0:
#         cp[idx] = 1
# a[:] = cp
    
print(a[(150//2)-10:(150//2)+10,(150//2)-10:(150//2)+10])
# print(cp)
b = coo_array(a)

print(b)



        
# def _moore_1(data, coord):
#     ##Hardcoded wrap -> decouple
#     idx = tuple(tuple(el+d % data.shape[0] if idx2 != idx else el
#                             for idx, _ in enumerate(coord)
#                             for idx2,el in enumerate(coord)
#                             for d in [-1,1]))
#     return tuple(data[i[0]] for i in idx)

# def _get_moore1_neighbors(coord,data):
#     neighbors = range(cheb_r[0]*-1, cheb_r[1]+1)
#     idx = tuple(tuple(c if idx != 0 else (c+r) % data.shape[0]
#                 for idx, c in enumerate(coord))
#                 for r in neighbors)
#     return tuple(data[i[0]] for i in idx)
    
    
