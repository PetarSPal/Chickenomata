from itertools import product, chain, cycle
import numpy as np
from Logic import data


class Grass:
    def __init__(
        self,
        shape,
        init_fill: str = "center",
        history: int = 0,   
        bg_value: int = 0,
        fg_value: int = 1,
        dtype: np.dtype = np.dtype('uint32')) -> None:
        '''
        Grass is a container on top of a numpy ndarray
        For the purpouses of storing data to be processed by automata and storing routines.
        The array can be accessed and modified directly via the instance .data
        Parameters:
            shape -> numpy shape
            default_value -> default fill value, default 0
            dtype -> numpy dtype, default unsigned int
        '''
        #TODO: Some modifications may result in bugs, squash/restrict later
        self._history = history
        self._hist_data = []
        match init_fill:
            case "random":
                self.data = np.random.randint(
                    fg_value, size=shape, dtype=dtype)
            case _:
                self.data = np.full(shape, bg_value, dtype)
                self._set_center(fg_value, False)
        self.linecount = 0
    

    @property
    def shape(self):
        return self.data.shape
    
    @property
    def dimensions(self):
        return self.data.ndim
    
    def _erase_history(self):
        self._hist_data = self._hist_data[:self._history]
    
    def _set_center(self, value, history=True):
        if self._history and history:
            self._hist_data.append(self.data)
            self._erase_history()
        data.set_center(value, self.data)
        
    def _uniform_fill(self, value, history=True):
        if self._history and history:
            self._hist_data.append(self.data)
            self._erase_history()
        data.uniform_fill(value, self.data)
        
    def _set_random(self, value, history=True):
        if self._history and history:
            self._hist_data.append(self.data)
            self._erase_history()
        data.random_fill(value, self.data)
        
    def _set_product(self, in_system, neighbors):
        int_prod = product(range(in_system), repeat=neighbors)
        cchainprod = cycle(chain(*int_prod))
        self.data[:] = np.fromiter(
            cchainprod,
            dtype=self.data.dtype,
            count=self.data.size
            ).reshape(self.data.shape)
    
    def mutate_all_moore(self, raptor, left=True):
        if self._history:
            self._hist_data.append(self.data)
            self._erase_history()
        self.data = data.mutate_all_moore(
            raptor, self.data, left)
        
    def mutate_all_moore_raptors(self, raptors, cols, left=True):
        if self._history:
            self._hist_data.append(self.data)
            self._erase_history()
        self.data = data.mutate_all_moore_raptors(
            raptors, self.data, cols, self.linecount, left)
        self.linecount +=1
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def _calc_begin_end(self, neighbor_count, left):
    #     #nc-1 because there's always a center pixel
    #     #div by 2 to check if the LR pixels are symmetrical
    #     offset, even = divmod((neighbor_count-1), 2)
    #     left = 1 if even and left else 0
    #     right = 1 if even and not left else 0
    #     #range of pixels in 1D
    #     return(-offset-left, offset+1+right)

    # def _calc_base_moore_idx(self, neighbor_count, left=True):
        
    #     def valid_ncount(number, base):
    #         '''
    #         Supposed to divide the ncount by the base
    #         to validate the ncount is fully divisible
    #         Is this curret that it's only done once?
    #         '''
    #         if not (1 == base):
    #             ncount, rem = divmod(number, base)
    #             if not rem:
    #                 return ncount
    #             raise Exception(f"invalid neighbor count for {base+1} dimensions")
    #         return number
        
    #     #3 to the power of dimensions-1 -- forgot
    #     #I believe it had to do with there being 3 directions in each dimensions, center and one in each vector
    #     #Aka when extruding to a new dimension we preserve the old dimension and then extrude in each vector in the new dim
    #     #IDK
    #     #1D automata -> 3**(1-1) = 1
    #     #2D automata -> 3**(2-1) = 3
    #     #3D automata -> 3**(3-1) = 9
    #     #So here we're validating the count is divisible by the dimension multiplier?
    #     neighbor_count = valid_ncount(neighbor_count, 3**(self.dimensions-1))
    #     b,e = self._calc_begin_end(neighbor_count, left)
    #     neighbor_range = range(b,e)
    #     #obtaining the product of the range repeated in x dimensions thereby obtaining the range in all dim
    #     neighbor_idxs = list(product(neighbor_range, repeat=self.dimensions))
    #     arr = np.array(neighbor_idxs)
    #     ##offsetting by the coord
    #     ##since all the work pertaining to the coord is done here
    #     ##we can cache all previous steps
    #     ##to avoid calculating for every coord
    #     return arr
        
    # def _get_moore_idx(self, coord, neighbor_count, left=True):
    #     arr = self._calc_base_moore_idx(neighbor_count, left)
    #     return arr + coord
        
    # def get_moore_neighbors(self, coord, neighbor_count, left=True):
    #     idxarr = self._get_moore_idx(coord, neighbor_count, left)
    #     return self.data[*idxarr.T]
    
    # def mutate_moore_neighbors(self, coord, values, neighbor_count, left=True):
    # why mutate the actual neighbors??
    #     idxarr = self._get_moore_idx(coord, neighbor_count, left)
    #     self.data[*idxarr.T] = values
        
    # def mutate_all(self, raptor, left=True):
    #     baseidx = self._calc_base_moore_idx(raptor.neighbor_count, left)
    #     begin, end = self._calc_begin_end(raptor.neighbor_count, left)
    #     print("be",begin,end)
    #     for i in range(-begin):
    #         idxarr = baseidx + i
    #         print("b")
    #         print(i)
    #         print(*idxarr.T)
    #         self.data[i] = raptor.io(self.data[*idxarr.T])
    #     for i in range(-begin, len(self.data)-end+1):
    #         idxarr = baseidx + i
    #         print(i)
    #         print(*idxarr.T)
    #         self.data[i] = raptor.io(self.data[*idxarr.T])
    #     for i in range(len(self.data)-end+1, len(self.data)):
    #         idxarr = baseidx + i
    #         for index, x in np.ndenumerate(idxarr)
                
                
    #         print("e")
    #         print(i)
    #         print(*idxarr.T)
    #         self.data[i] = raptor.io(self.data[*idxarr.T])
        
    # # def apply_moore_rule(self, coord, rule, neighbor_count, left=True):
    # #     idxarr = self._get_moore_idx(coord, neighbor_count, left)
    # #     self.data[*idxarr.T] = rule(self.data[*idxarr.T])
    
    # def get_von_neuman_neighbors(self):
    #     pass
    
    
    
# testG = Grass(100,1)
# testG.set_random(2)
# print(testG.data)
