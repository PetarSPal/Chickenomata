from scipy import ndimage
import numpy as np


def moore1(ndim):
    return ndimage.generate_binary_structure(ndim, ndim).astype(int)


def vn1(ndim):
    return ndimage.generate_binary_structure(ndim, 1).astype(int)


m1 = moore1(3)
m1 = ndimage.iterate_structure(m1, 2).astype(int)
v1 = vn1(5)
print(v1)
