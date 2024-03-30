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
    #TODO: Maybe better to return and deref?
    data[:] = np.random.randint(value, size=data.shape, dtype=int)


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
        chebyshev_range: int, tend_left: bool = True) -> tuple:
    '''
    Takes total neighbor count, dimensions as parameters.
    Optionally takes direction to tend when not perfectly symmetrical
        (default left)
    
    For the purpouses of drawing a Moore neighbors shape
    Generates the 1D line coordinates to be used as foundation of the shape
    
    Returns begin and end (+1) coordinates of the line
    (end is +1 to account for usage in py range)
    '''
    half_distance, even = divmod((chebyshev_range-1), 2)
    #Handling even sized neighborhoods (asymmetric)
    tendl, tendr = int(even and tend_left), int(even and (not tend_left))
    begin, end = (-half_distance-tendl, half_distance+tendr+1)
    return (begin, end)


def get_moore_idx(
        chebyshev_range: int, dimensions: int, left: bool = True) -> np.ndarray:
    '''
    Parameters:
        neighbor_count - total neighbor count
        dimensions - self explanatory
        left - should automata lean left or right in even sized neighboohoods
    Returns:
        np.ndarray containing the indexes for a general moore neighboorhood
        Center has 0 coordinates
    '''
    b, e = moore_one_d_range_limits(chebyshev_range, left)
    neighbor_range = range(b, e)
    neighbor_idxs = list(product(neighbor_range, repeat=dimensions))
    arr = np.array(neighbor_idxs)
    return arr

def get_moore_neighbors(
        coord: np.ndarray,
        data: np.ndarray,
        chebyshev_range: int,
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
    b, e = moore_one_d_range_limits(chebyshev_range, left)
    idxarr = get_moore_idx(chebyshev_range, dimensions, left)
    padding = max(abs(b), e)
    padded = np.pad(data, padding, "wrap")
    ##TODO: Careful here regarding rule ::-1
    ##This is a bit of a mess partly due to left
    #Parly because the coord starts at negative values
    #I need the left-most coord begin at 0 in order to properly work with padding
    #The alternive is to create wrap padding on the left then MOVE it to the right
    #Otherwise both left and right out of boundary take info from the same columns
    remove = 0 if left else -1
    offset = padding - (1 if left else 0)
    for dim in range(padded.ndim):
        padded = np.delete(padded, remove, dim)
    # print([(idxarr + coord).T])
    # print("pad", padded)
    return padded[*(idxarr + coord + offset).T]

# def mutate_moore_neighbors(self, coord, values, neighbor_count, left=True):
# why mutate the actual neighbors??
#     idxarr = self._get_moore_idx(coord, neighbor_count, left)
#     self.data[*idxarr.T] = values


def mutate_moore(raptor, coord, data, dimensions, neighbor_count, left=True):
    values = get_moore_neighbors(coord, data, neighbor_count, dimensions, left)
    # print("coord", coord, values)
    return raptor.io(values)
    
def mutate_all_moore(raptor, data, dimensions, neighbor_count, left):
    new_data = np.zeros(data.shape, dtype=int)
    for index, _ in np.ndenumerate(data):
        m = mutate_moore(raptor, index, data, dimensions, neighbor_count, left)
        new_data[index] = m
    return new_data
    
# def mutate_all(raptor, data, dimensions, left=True):
#     baseidx = calc_base_moore_idx(raptor.neighbor_count, dimensions, left)
#     begin, end = moore_one_d_range_limits(raptor.neighbor_count, left)
#     print("be",begin,end)
#     for i in range(-begin):
#         idxarr = baseidx + i
#         print("b")
#         print(i)
#         print(*idxarr.T)
#         data[i] = raptor.io(data[*idxarr.T])
#     for i in range(-begin, len(data)-end+1):
#         idxarr = baseidx + i
#         print(i)
#         print(*idxarr.T)
#         data[i] = raptor.io(data[*idxarr.T])
#     for i in range(len(data)-end+1, len(data)):
#         idxarr = baseidx + i
#         for index, x in np.ndenumerate(idxarr)
            
            
#         print("e")
#         print(i)
#         print(*idxarr.T)
#         self.data[i] = raptor.io(self.data[*idxarr.T])





def get_neuman_idx(
        dimensions: int = 1, manhattan_range: int = 1) -> np.ndarray:
    '''
    Usage:
        Generates a Von Neumann neighborhood, by given dimensions (>1) and range
    Parameters:
        dimensions
        manhattan_range
    Returns:
        array containing indexes of a Von Neuman neighborhood with center abs 0
    '''
    
    if dimensions < 1:
        raise ValueError("dimension must be gte 1")
    center = [0 for _ in range(dimensions)]
    finalcoords = [center,]
    ndimension_coords = {}

    def split_direction(
        basecoord: list,
        index: int,
        dimension: int,
        finalcoords: list,
        n_dimension_coords: dict
    ) -> tuple:
        '''
        Usage:
            Given a starting coordinate, index and dimension
            Produces two new coordinates which instead contain -1 and 1 at the given index
            Adds the two new coordinates to the finalcoord list
            Adds the two new coordinates n_dimension_coords dict with dimension as key
        Params:
            basecoord -> starting coordinate
            index -> current index (movement dimension)
            dimension -> current dimension (parent dimension)
            finalcoords -> list of all coords
            n_dimension_coords -> dict of coords of N dimension
        Returns:
            Tuple with updated finalcoords, n_dimension_coords
        '''
        temp_dcoords = n_dimension_coords.copy()
        temp_finalcoords = finalcoords.copy()
        if dimension not in temp_dcoords:
            temp_dcoords[dimension] = []
        for increment in [-1, 1]:
            new_coord = basecoord.copy()
            new_coord[index] = increment
            temp_finalcoords.append(new_coord)
            temp_dcoords[dimension].append(new_coord)
        return temp_finalcoords, temp_dcoords
    ##R = 1
    for index in range(len(center)):    
        finalcoords, ndimension_coords = split_direction(
            center, index, index+1, finalcoords, ndimension_coords)
    ##R > 1
    for _R in range(2, manhattan_range+1):
        new_ndimension_coords = {}
        # for dimension in range(1, dimensions+1):
        #     for coords in ndimension_coords[dimension]:
        #         for index, axis_coord in enumerate(coords[:dimension]):
        nested_loop = [(index, axis_coord, coords, dimension)
                       for dimension in range(1, dimensions + 1)
                       for coords in ndimension_coords[dimension]
                       for index, axis_coord in enumerate(coords[:dimension])]
        for index, axis_coord, coords, dimension in nested_loop:
            if axis_coord == 0:
                finalcoords, new_ndimension_coords = split_direction(
                    coords,
                    index,
                    dimension,
                    finalcoords,
                    new_ndimension_coords)
            else:
                if dimension not in new_ndimension_coords:
                    new_ndimension_coords[dimension] = []
                straight_direction = coords.copy()
                direction = -1 if axis_coord < 0 else 1
                straight_direction[index] = axis_coord + direction
                new_ndimension_coords[dimension].append(straight_direction)
                finalcoords.append(straight_direction)
                break
        ndimension_coords = new_ndimension_coords
    ##TODO: left
    return np.array(sorted(finalcoords))
        
    
def get_neuman_neighbors(
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
    idxarr = get_neuman_idx(dimensions, neighbor_count) 
    return data[*(idxarr + coord).T]








# g = np.zeros(tuple(4 for _ in range(2)))
# print(g)

# print(set_center(2, g))

# print(calc_begin_end(81,3))







# 0 -> 1, -1 -> 2, -2

# 0,0 -> (+1,-1) -> 1,0 0,1 -1,0 0,-1 ->
