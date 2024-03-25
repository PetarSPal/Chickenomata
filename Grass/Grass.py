from itertools import product
import numpy as np


class Grass:
    def __init__(self, width, dimensions) -> None:
        self._width = width
        self._dimensions = dimensions
        self.data = np.zeros(tuple(width for _ in range(dimensions)))

    @property
    def width(self):
        return self._width
    
    @property
    def dimensions(self):
        return self._dimensions
    
    def set_center(self, value):
        half_width = self.width // 2
        self.data[(tuple(half_width for _ in range(self.dimensions)))] = value
        
    def fill(self, value):
        self.data.fill(value)
        
    def set_random(self, value):
        size = tuple(self.width for _ in range(self.dimensions))
        self.data = np.random.randint(value, size=size)
    
    
    def _calc_begin_end(self, neighbor_count, left):
        #nc-1 because there's always a center pixel
        #div by 2 to check if the LR pixels are symmetrical
        offset, even = divmod((neighbor_count-1), 2)
        left = 1 if even and left else 0
        right = 1 if even and not left else 0
        #range of pixels in 1D
        return(-offset-left, offset+1+right)

    def _calc_base_moore_idx(self, neighbor_count, left=True):
        
        def valid_ncount(number, base):
            '''
            Supposed to divide the ncount by the base
            to validate the ncount is fully divisible
            Is this curret that it's only done once?
            '''
            if not (1 == base):
                ncount, rem = divmod(number, base)
                if not rem:
                    return ncount
                raise Exception(f"invalid neighbor count for {base+1} dimensions")
            return number
        
        #3 to the power of dimensions-1 -- forgot
        #I believe it had to do with there being 3 directions in each dimensions, center and one in each vector
        #Aka when extruding to a new dimension we preserve the old dimension and then extrude in each vector in the new dim
        #IDK
        #1D automata -> 3**(1-1) = 1
        #2D automata -> 3**(2-1) = 3
        #3D automata -> 3**(3-1) = 9
        #So here we're validating the count is divisible by the dimension multiplier?
        neighbor_count = valid_ncount(neighbor_count, 3**(self.dimensions-1))
        b,e = self._calc_begin_end(neighbor_count, left)
        neighbor_range = range(b,e)
        #obtaining the product of the range repeated in x dimensions thereby obtaining the range in all dim
        neighbor_idxs = list(product(neighbor_range, repeat=self.dimensions))
        arr = np.array(neighbor_idxs)
        ##offsetting by the coord
        ##since all the work pertaining to the coord is done here
        ##we can cache all previous steps
        ##to avoid calculating for every coord
        return arr
        
    def _get_moore_idx(self, coord, neighbor_count, left=True):
        arr = self._calc_base_moore_idx(neighbor_count, left)
        return arr + coord
        
    def get_moore_neighbors(self, coord, neighbor_count, left=True):
        idxarr = self._get_moore_idx(coord, neighbor_count, left)
        return self.data[*idxarr.T]
    
    # def mutate_moore_neighbors(self, coord, values, neighbor_count, left=True):
    # why mutate the actual neighbors??
    #     idxarr = self._get_moore_idx(coord, neighbor_count, left)
    #     self.data[*idxarr.T] = values
        
    def mutate_all(self, raptor, left=True):
        baseidx = self._calc_base_moore_idx(raptor.neighbor_count, left)
        begin, end = self._calc_begin_end(raptor.neighbor_count, left)
        print("be",begin,end)
        for i in range(-begin):
            idxarr = baseidx + i
            print("b")
            print(i)
            print(*idxarr.T)
            self.data[i] = raptor.io(self.data[*idxarr.T])
        for i in range(-begin, len(self.data)-end+1):
            idxarr = baseidx + i
            print(i)
            print(*idxarr.T)
            self.data[i] = raptor.io(self.data[*idxarr.T])
        for i in range(len(self.data)-end+1, len(self.data)):
            idxarr = baseidx + i
            for index, x in np.ndenumerate(idxarr)
                
                
            print("e")
            print(i)
            print(*idxarr.T)
            self.data[i] = raptor.io(self.data[*idxarr.T])
        
    # def apply_moore_rule(self, coord, rule, neighbor_count, left=True):
    #     idxarr = self._get_moore_idx(coord, neighbor_count, left)
    #     self.data[*idxarr.T] = rule(self.data[*idxarr.T])
    
    def get_von_neuman_neighbors(self):
        pass
    
    
    
# testG = Grass(100,1)
# testG.set_random(2)
# print(testG.data)
