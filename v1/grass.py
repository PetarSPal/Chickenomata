"""
Data grids, currently only square
"""

from itertools import product, chain, cycle
import numpy as np
from numpy import typing
from v1.utils.calc import split_mnc, reduce_mnc
import random


class Square:
    def __init__(
            self,
            shape,
            init_fill: str = "center",
            history: int = 0,
            bg_value: int = 0,
            fg_value: int = 1,
            repeat_value: int = 3,
            dtype: np.dtype = np.dtype('uint32')) -> None:
        """
        Summary
        Grass is a container for the ndarray storing the data
        Can be modified via the provided routines or by directly chaging the

        Parameters:
            shape: -> numpy shape
            init_fill: str -> determines the initial condition
                "center" -> sets the middle element to fg_value
                "random" -> random
                "product" -> fills with product of range(fg_value) 
                    repeats for repeat_value times and cycles through them
            history: int -> how many historic states to store
            bg_value: int = 0 -> background value for initial fill
            fg_value: int = 1 -> foreground value for initial fill
            repeat_value: int = 3 -> num of repeats for "product" init_fill
            dtype: np.dtype -> numpy data type, default usigned int
        """
        # TODO: Some modifications may result in bugs, squash/restrict later
        self._history = history
        self._hist_data = []
        self.data = np.zeros(shape, dtype)
        match init_fill:
            case "random":
                self._set_random(fg_value)
            case "product":
                self._set_product(fg_value, repeat_value)
            case _:
                self._uniform_fill(bg_value)
                self._set_center(fg_value, False)
        self.linecount = 0

    @property
    def shape(self) -> tuple[int, ...]:
        """
        Returns:
           shape : tuple of ints
        """
        return self.data.shape

    @property
    def ndim(self) -> int:
        """
        Returns:
            int : number of dimensions
        """
        return self.data.ndim

    def _clean_history(self) -> None:
        """
        Cleans excessive history
        """
        while len(self._hist_data) > self._history:
            self._hist_data.pop(0)
        # self._hist_data = self._hist_data[len(self._hist_data)-self._history:]

    def _set_center(self, value: int, history=True) -> None:
        '''
        Sets the center-most element of ndarray to value
        Leans toward the negative if elements are even
        '''
        if self._history and history:
            self._hist_data.append(self.data.copy())
            self._clean_history()
        center_coords = map(lambda x: x//2, self.data.shape)
        self.data[*center_coords] = value

    def _uniform_fill(self, value: int, history=True) -> None:
        '''
        Fills the ndarray uniformly with the provided value
        '''
        if self._history and history:
            self._hist_data.append(self.data.copy())
            self._clean_history()
        self.data.fill(value)

    def _set_random(self, value, history=True):
        '''
        Fills the ndarray with random ints in the range from 0 to the value
        '''
        if self._history and history:
            self._hist_data.append(self.data.copy())
            self._clean_history()
        self.data[:] = np.random.randint(
            value, size=self.data.shape, dtype=self.data.dtype)

    def _set_product(self, in_system, neighbors):
        int_prod = product(range(in_system), repeat=neighbors)
        cchainprod = cycle(chain(*int_prod))
        self.data[:] = np.fromiter(
            cchainprod,
            dtype=self.data.dtype,
            count=self.data.size
        ).reshape(self.data.shape)

    def graze_all(self, flock, left=True, wrap='wrap'):
        if self._history:
            self._hist_data.append(self.data.copy())
            self._clean_history()
        self.data[:] = flock.graze_all(self.data, left, wrap)

    def graze_blade(self, idx, flock, left=True, wrap='wrap'):
        if self._history:
            self._hist_data.append(self.data.copy())
            self._clean_history()
        self.data[idx] = flock.graze_blade(self.data, idx, left, wrap)

    # def _get_linear_neighbors(
    #         self,
    #         coord,
    #         data,
    #         cheb_r,
    #         wrap='wrap',
    #         edge=False):
    #     neighbors = range(cheb_r[0]*-1, cheb_r[1]+1)
    #     idx = tuple(tuple(c if idx != 0 else (c+r) % data.shape[0]
    #                 for idx, c in enumerate(coord))
    #                 for r in neighbors)
    #     return tuple(data[i[0]] for i in idx)
