import numpy as np
from itertools import product


def set_center(
        value: int, data: np.ndarray) -> None:
    '''
    Sets the center-most element of ndarray to value
    Parameters:
        value - value to set the element to
        data - ndarray
    '''
    def floor_round(x):
        return x // 2
    #In even-sized matrices, take the floor medians for center
    #To get all possible centers we'll need all combinations of all floor and ceil medians across all dimensions
    #Not worth
    # def ceil_round(x):
    #     res, rem = divmod(x, 2)
    #     return res-(rem ^ 1)
    center_coords = map(floor_round, data.shape)
    data[*center_coords] = value


def uniform_fill(value: int, data: np.ndarray) -> None:
    '''
    Fills the ndarray uniformly with the provided value
    '''
    data.fill(value)


def random_fill(value: int, data: np.ndarray) -> None:
    '''
    Fills the ndarray with random ints in the range from 0 to the value
    '''
    data = np.random.randint(value, size=data.shape)


def moore_one_d_ncount(totalncount: int, dimensions: int) -> int:
    '''
    Takes total neighbor count and dimensions as parameters
    For the purpouses of Moore neighborhood shape
    Returns an equivalent neighbor count in 1D (e.g. 1D= 3 -> 2d= 9 -> 3d= 27)
    Throws exception is the ncount shape is not rationally reducible to 1D
    (Aka if not Von Neuman or Moore -like shape)
    '''
    base = 3**(dimensions-1)
    if not (1 == base):
        one_d_ncount, rem = divmod(totalncount, base)
        if not rem:
            return one_d_ncount
        raise Exception(f"invalid neighbor count for {base+1} dimensions")
    return totalncount


def moore_one_d_range_limits(
        total_ncount: int, dimensions: int, tend_left: bool = True) -> tuple:
    '''
    Takes total neighbor count, dimensions as parameters.
    Optionally takes direction to tend when not perfectly symmetrical
        (default left)
    
    For the purpouses of drawing a Moore neighbors shape
    Generates the 1D line coordinates to be used as foundation of the shape
    
    Returns begin and end (+1) coordinates of the line
    (end is +1 to account for usage in py range)
    '''
    one_d_ncount = moore_one_d_ncount(total_ncount, dimensions)
    half_distance, even = divmod((one_d_ncount-1), 2)
    #Handling even sized neighborhoods (asymmetric)
    tendl, tendr = int(even and tend_left), int(even and (not tend_left))
    begin, end = (-half_distance-tendl, half_distance+tendr+1)
    return (begin, end)


def calc_base_moore_idx(
        neighbor_count: int, dimensions: int, left: bool = True) -> np.ndarray:
    '''
    Parameters:
        neighbor_count - total neighbor count
        dimensions - self explanatory
        left - should automata lean left or right in even sized neighboohoods
    Returns:
        np.ndarray containing the indexes for a general moore neighboorhood
        Center has 0 coordinates
    '''
    b, e = moore_one_d_range_limits(neighbor_count, dimensions, left)
    neighbor_range = range(b, e)
    neighbor_idxs = list(product(neighbor_range, repeat=dimensions))
    arr = np.array(neighbor_idxs)
    return arr


def get_moore_idx(
        coord: np.ndarray,
        neighbor_count: int,
        dimensions: int,
        left: bool = True):
    '''
    Parameters:
        coord - coordinate of center element
        neighbor_count - total neighbor count
        dimensions - self explanatory
        left - should automata lean left or right in even sized neighboohoods
    Returns:
        np.ndarray of a moore neighborhood with the provider coord as center
    '''
    arr = calc_base_moore_idx(neighbor_count, dimensions, left)
    return arr + coord


def get_moore_neighbors(
        coord: np.ndarray,
        data: np.ndarray,
        neighbor_count: int,
        dimensions: int,
        left: bool = True):
    '''
    Parameters:
        coord - coordinate of center element
        data - data source
        neighbor_count - total neighbor count
        dimensions - self explanatory
        left - should automata lean left or right in even sized neighboohoods
    Returns:
        np.ndarray with the daya of the moore neighbors
    '''
    #Is this needed as is?
    idxarr = get_moore_idx(coord, neighbor_count, dimensions, left)
    return data[*idxarr.T]

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





# g = np.zeros(tuple(4 for _ in range(2)))
# print(g)

# print(set_center(2, g))

print(calc_begin_end(81,3))