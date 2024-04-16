"""
Temp -> for reference while I rework the neighbor finding logic
"""

def _graze_all(self, raptor, left=True, wrap='wrap'):
    if self._history:
        self._hist_data.append(self.data)
        self._clean_history()
    self._mutate_all_moore(
        raptor, left, wrap)

    
def __experimental__graze_all_multiraptor(self, raptors, cols, left=True):
    if self._history:
        self._hist_data.append(self.data)
        self._clean_history()
    self.data = self.__experimental__mutate_all_moore_raptors(
        raptors, self.data, cols, self.linecount, left)
    self.linecount +=1
    
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
    return tuple(data[i[0]] for i in idx)

def _get_moore_neighbors(
        self,
        coord,
        data,
        cheb_r,
        wrap='wrap',
        edge=False):
    dimensions = data.ndim
    if data.ndim == 1:
        return self._get_linear_neighbors(coord,data,cheb_r, wrap, edge)
    if dimensions < 1:
        raise ValueError("dimension must be gte 1")
    
    if not edge:
        def handle_edge(coord): return data[*coord]
    elif wrap == 'wrap':
        def handle_edge(coord): return data[*(x % data.shape[dim] for x in coord)]
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
    ##Decouple center
    ##Switch to TF for GPU
    return [data[center]] + out


def _mutate_moore(self, raptor, coord, data, cheby_range, wrap='wrap', edge=False):
    values = self._get_moore_neighbors(coord, data, cheby_range, wrap, edge)
    return raptor.io(values)
    
def _mutate_all_moore(self, raptor, left=True, wrap='wrap'):
    data = self.data
    new_data = np.zeros(data.shape, dtype=data.dtype)
    c_range = reduce_mnc(raptor.neighbor_count, data.ndim)
    b, e = split_mnc(c_range, left)
    c_range = c_range-1
    shape = np.zeros(data.shape)
    slis = (slice(b, -e) for _ in range(data.ndim))
    shape[*slis] = 1
    mid = np.where(shape == 1)
    edge = np.where(shape == 0)
    for i in range(mid[0].size):
        idx = tuple(mid[j][i] for j in range(data.ndim))
        values = self._get_moore_neighbors(idx, data, (b, e))
        # print(values)
        new_data[idx] = raptor.io(values)
    for i in range(edge[0].size):
        idx = tuple(edge[j][i] for j in range(data.ndim))
        values = self._get_moore_neighbors(idx, data, (b, e), wrap=wrap, edge=True)
        # print(values)
        new_data[idx] = raptor.io(values)
    self.data = new_data
    # return new_data

def __experimental__mutate_all_moore_raptors(self, raptors, data, cols, lines, left):
    new_data = np.zeros(data.shape, dtype=int)
    crap = cycle(raptors)
    step = cycle(range(10))
    for index, _ in np.ndenumerate(data):
        if next(step)== 0:
            cur = next(crap)
        m = self._mutate_moore(cur, index, data, left)
        new_data[index] = m
    if lines % 1 == 0 :
        rand = iter([[random.randint(0,4) for _ in range(125)] for _ in range(len(raptors))])
        # rand = iter([[random.randint(0,1) for _ in range(8)] for _ in range(len(raptors))])
        for rap in raptors:
            rap.rule = next(rand)
    return new_data

def __rework__get_neuman_idx(
        self, dimensions: int = 1, manhattan_range: int = 1) -> np.ndarray:
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
        
def __rework__get_neuman_neighbors(
        self,
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
    idxarr = self.__rework__get_neuman_idx(dimensions, neighbor_count) 
    return data[*(idxarr + coord).T]


# def __experimental__mutate_all_moore_raptors(self, raptors, data, left):
#     new_data = np.zeros(data.shape, dtype=int)
#     crap = cycle(raptors)
#     import random
#     for index, _ in np.ndenumerate(data):
#         # print(crap.rule)
#         m = mutate_moore(next(crap), index, data, left)
#         new_data[index] = m
#     rand = iter([[random.randint(0,1) for _ in range(8)] for _ in range(len(raptors))])
#     for rap in raptors:
#         rap.rule = next(rand)
#     return new_data