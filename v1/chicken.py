"""
Structural logic
Very far from being implemented, conceptually I am going for:
    Flock -> contains and manages multiple chicken
    Chicken -> 1:1 relationship with a raptor, also holds a beak and an egg
    Beak/Egg -> pre/post 
    Head -> This was meant to expose the Flock to the chicken, but I'm not sure it's needed
"""

from itertools import chain
import numpy as np
from v1.utils.calc import split_mnc, reduce_mnc


class Beak:
    def __init__(self, sieve, head) -> None:
        self.sieve = sieve
        self.head = head

    def peck(self, value):
        sieved, leftovers = self.sieve(value)
        # Passing self won't work, I need to manage self-rerence in the container housing the self
        # Aka I need to work with the flock and and identifier for the beak in the flock
        self.head.beak_spit(self, leftovers)
        return sieved


class Egg:
    def __init__(self, sieve, head) -> None:
        self.sieve = sieve
        self.head = head

    def hatch(self, value):
        sieved, leftovers = self.sieve(value)
        # Passing self won't work, I need to manage self-rerence in the container housing the self
        # Aka I need to work with the flock and and identifier for the beak in the flock
        self.head.egg_crack(self, leftovers)
        return sieved


class Flock:
    def __init__(self, chicks, head) -> None:
        self.chicks = chicks
        self.head = head

    # def graze_blade(self, data, idx, left, wrap):
    #     # return self.chicks[idx].graze(idx, data, left, wrap)
    #     return self.chicks[0].graze(idx, data, left, wrap)

    def graze_all(self, data, left, wrap):
        new_data = np.zeros(data.shape, dtype=data.dtype)
        for idx in np.ndindex(data.shape):
            new_data[idx] = self.chicks[0].graze(
                idx, data, left, wrap, edge=True)
        return new_data

    def graze_blade(self, data, idx, left, wrap="wrap", edge=True):
        # return self.chicks[idx].graze(idx, data, left, wrap)
        return self.chicks[0].graze(idx, data, left, wrap, edge)

    def graze_all(self, data, left, wrap):
        new_data = np.zeros(data.shape, dtype=data.dtype)

        test = False
        if self.chicks[0].mode == 'slice':
            test = True
        c_range = reduce_mnc(
            self.chicks[0].raptor.neighbor_count, data.ndim, test)
        b, e = split_mnc(c_range, left)
        c_range = c_range-1
        shape = np.zeros(data.shape)
        slis = (slice(b, -e) for _ in range(data.ndim))
        shape[*slis] = 1
        mid = np.where(shape == 1)
        edge = np.where(shape == 0)
        for i in range(mid[0].size):
            idx = tuple(mid[j][i] for j in range(data.ndim))
            new_data[idx] = self.chicks[0].graze(
                idx, data, left, wrap, edge=False)
        for i in range(edge[0].size):
            idx = tuple(edge[j][i] for j in range(data.ndim))
            new_data[idx] = self.chicks[0].graze(
                idx, data, left, wrap, edge=True)
        return new_data

    # def hatch(self, value):
    #     ##I forgot what this was meant for
    #     ##I suspect it was a concept for multi-flocks
    #     self.side_effect(leftovers)
    #     return sieved


class Head:
    def __init__(self) -> None:
        self.beak_effect = lambda _, __: __
        self.egg_effect = lambda _, __: __

    def beak_spit(self, beak, value):
        self.beak_effect(beak, value)

    def egg_crack(self, egg, value):
        self.egg_effect(egg, value)


class Chicken:
    def __init__(self, raptor, beak=None, egg=None) -> None:
        def blank(_): return _
        self.raptor = raptor
        self.beak = beak or blank
        self.egg = egg or blank

        self.mode = 'slice'

    def graze(self, idx, data, left, wrap, edge):
        # cheb_r = split_mnc(self.raptor.neighbor_count, left)
        # neighbors = self._get_linear_neighbors(idx, data, cheb_r, wrap)

        test = False
        if self.mode == 'slice':
            test = True
        reduced_r = reduce_mnc(self.raptor.neighbor_count, data.ndim, test)
        cheb_r = split_mnc(reduced_r, left)
        neighbors = self._get_moore_neighbors(idx, data, cheb_r, wrap, edge)

        crop = self.beak(neighbors)
        if test:
            heritage = self.raptor.io(crop[:self.raptor.neighbor_count])
        else:
            heritage = self.raptor.io(crop)
        new_blade = self.egg(heritage)
        return new_blade

    def _get_linear_neighbors(
            self,
            coord,
            data,
            cheb_r,
            wrap='wrap',
            edge=False):
        neighbors = range(cheb_r[0]*-1, cheb_r[1]+1)
        idx = tuple(tuple(c if idx != 0 else (c+r) % data.shape[0]
                    for idx, c in enumerate(coord))
                    for r in neighbors)
        return tuple(data[i] for i in idx)

    def _get_moore_neighbors(
            self,
            coord,
            data,
            cheb_r,
            wrap='wrap',
            edge=False):
        dimensions = data.ndim
        if data.ndim == 1:
            return self._get_linear_neighbors(coord, data, cheb_r, wrap, edge)
        if dimensions < 1:
            raise ValueError("dimension must be gte 1")

        if not edge:
            def handle_edge(coord): return data[*coord]
        elif wrap == 'wrap':
            def handle_edge(
                coord): return data[*(x % data.shape[dim] for x in coord)]
        else:
            def handle_edge(coord): return wrap

        center = tuple(coord)
        currcoords = (center, )
        oldcoords = set(currcoords)
        out = []
        no_center = tuple(chain(
            range((cheb_r[0]*-1), 0),
            range(1, cheb_r[1]+1)))
        for dim in range(0, dimensions):
            for curr_coord, direction in ((curr_coord, direction)
                                          for curr_coord in currcoords
                                          for direction in no_center):
                new_coord = tuple(el if idx != dim
                                  else el+direction
                                  for idx, el in enumerate(curr_coord))
                oldcoords.add(new_coord)
                out.append(handle_edge(new_coord))
            currcoords = tuple(oldcoords)
        # Decouple center
        # Switch to TF for GPU
        return [data[center]] + out
