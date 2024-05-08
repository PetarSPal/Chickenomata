"""
Automata logic
"""

from itertools import chain
import numpy as np
from v1.utils.calc import split_mnc, reduce_mnc


class Pre:
    def __init__(self, sieve=None) -> None:
        def blank(_, *__):
            return _, None

        self.sieve = sieve if callable(sieve) else blank

    def __call__(self, value, automata, ndim) -> None:
        sieved, leftovers = self.sieve(value, automata, ndim)
        if leftovers is not None:
            automata.peck(leftovers)
        return sieved


class Post(Pre):
    def __init__(self, sieve=None) -> None:
        super().__init__(sieve)


class Automata:
    def __init__(
        self,
        resolver,
        lr_range=None,
        pre=None,
        post=None,
        head=None,
        chicks=None,
        adjacency=None,
        adjacency_auto=None,
        mode="moore",
        wrap="wrap",
        left=True,
        period=0,
        timer=0,
    ) -> None:
        def blank(_, *__):
            return _

        self.resolver = resolver
        self.pre = pre or blank
        self.post = post or blank
        self.head = head
        self.chicks = chicks or self
        self.lr_range = (
            lr_range if isinstance(lr_range, tuple) else (lr_range, lr_range)
        )
        if adjacency is not None:
            self.adjacency = adjacency
            self.adjacency_auto = adjacency_auto
            self.adj = np.vstack(np.where(np.asarray(self.adjacency.data) == 1)).T
            self.adj -= tuple((i - 1) // 2 for i in self.adjacency.data.shape)
        else:
            self.adjacency = adjacency
            self.adj = None
        self.mode = mode
        self.wrap = wrap
        self.left = left
        self.period = period
        self.timer = timer

    def peck(self, value):
        pass

    def graze(self, idx, data, edge):
        # cheb_r = split_mnc(self.resolver.neighbor_count, left)
        # neighbors = self._get_linear_neighbors(idx, data, cheb_r, wrap)

        if self.lr_range is None or self.lr_range[0] is None:
            reduced_r = reduce_mnc(self.resolver.neighbor_count, data.ndim)
            cheb_r = split_mnc(reduced_r, self.left)
            lr_range = cheb_r
        else:
            lr_range = self.lr_range

        if self.adjacency is not None:
            neighbors = self._get_by_bit_adjacency(idx, data, self.wrap, edge)
        elif self.mode == "moore":
            neighbors = self._get_moore_neighbors(idx, data, lr_range, self.wrap, edge)
        else:
            neighbors = self.__rework__get_neumann_neighbors(
                idx, data, lr_range, self.wrap, edge
            )

        crop = self.pre(np.asarray(neighbors), self, data.ndim)
        heritage = self.resolver.resolve(crop)
        new_blade = self.post(heritage, self)
        return new_blade

    def graze_batch(self, indices, data, edge):
        # cheb_r = split_mnc(self.resolver.neighbor_count, left)
        # neighbors = self._get_linear_neighbors(idx, data, cheb_r, wrap)
        if self.adjacency is None and (
            self.lr_range is None or self.lr_range[0] is None
        ):
            reduced_r = reduce_mnc(self.resolver.neighbor_count, data.ndim)
            cheb_r = split_mnc(reduced_r, self.left)
            lr_range = cheb_r
        elif self.adjacency is None:
            lr_range = self.lr_range

        if self.adjacency is not None:
            neighbors = np.array(
                [self._get_by_bit_adjacency(idx, data, edge) for idx in indices]
            ).T
        elif self.mode == "moore":
            neighbors = np.array(
                [
                    (self._get_moore_neighbors(idx, data, lr_range, edge))
                    for idx in indices
                ]
            ).T
        else:
            neighbors = np.array(
                [
                    (self.__rework__get_neumann_neighbors(idx, data, lr_range, edge))
                    for idx in indices
                ]
            ).T

        crop = self.pre(neighbors, self, data.ndim)
        heritage = self.resolver.resolve_batch(crop)
        new_blades = self.post(heritage, self, data.ndim)
        return new_blades

    def graze_all(self, data):
        if self.mode != "moore":
            return self.graze_all_iterative(data)
        new_data = np.zeros(data.shape, dtype=data.dtype)

        bitarray = np.zeros(data.shape, dtype="b")
        if self.adjacency is not None:
            bit_region = (
                slice(
                    (max(self.adjacency.data.shape) - 1) // 2,
                    -(max(self.adjacency.data.shape) - 1) // 2,
                )
                for _ in range(data.ndim)
            )
        elif self.adjacency is None and (
            self.lr_range is None or self.lr_range[0] is None
        ):
            c_range = reduce_mnc(self.chicks.resolver.neighbor_count, data.ndim)
            b, e = split_mnc(c_range, self.left)
            bit_region = (slice(b, -e) for _ in range(data.ndim))
        else:  # self.adjacency is None:
            b, e = self.lr_range
            bit_region = (slice(b, -e) for _ in range(data.ndim))
        bitarray[*bit_region] = 1
        mid_mask = np.where(bitarray == 1)
        edge_mask = np.where(bitarray == 0)
        if mid_mask[0].size:
            mid_results = self.chicks.graze_batch(
                np.vstack(mid_mask).T, data, edge=False
            )
            new_data[mid_mask] = mid_results.flatten()
        edge_results = self.chicks.graze_batch(np.vstack(edge_mask).T, data, edge=True)
        new_data[edge_mask] = edge_results.flatten()
        if self.adjacency is not None and self.adjacency_auto is not None:
            # TODO: collect this print
            # print(self.adjacency.data)
            self.adjacency.graze_all(self.adjacency_auto)
            # TODO: Display this!
            # TODO: Get wrap from state
            # print(self.adjacency.data)
            adj_center = self.adjacency.get_center()
            self.adjacency._set_center(0)
            self.adj = np.vstack(np.where(np.asarray(self.adjacency.data) == 1)).T
            self.adj -= tuple((i - 1) // 2 for i in self.adjacency.data.shape)
            # if preserve center:
            self.adjacency._set_center(adj_center)

        return new_data

    def graze_all_iterative(self, data):
        new_data = np.zeros(data.shape, dtype=data.dtype)

        if self.lr_range is None or self.lr_range[0] is None:
            c_range = reduce_mnc(self.chicks.resolver.neighbor_count, data.ndim)
            b, e = split_mnc(c_range, self.left)
        else:
            b, e = self.lr_range
        bitarray = np.zeros(data.shape)
        bit_region = (slice(b, -e) for _ in range(data.ndim))
        bitarray[*bit_region] = 1
        mid_mask = np.where(bitarray == 1)
        edge_mask = np.where(bitarray == 0)
        mid_results = np.array(
            [
                self.chicks.graze(idx, data, self.left, self.wrap, edge=False)
                for idx in np.vstack(mid_mask).T
            ]
        )
        edge_results = np.array(
            [
                self.chicks.graze(idx, data, self.left, self.wrap, edge=True)
                for idx in np.vstack(edge_mask).T
            ]
        )
        new_data[mid_mask] = mid_results.flatten()
        new_data[edge_mask] = edge_results.flatten()
        return new_data

    def _get_by_bit_adjacency(self, idx, data, edge):
        if not edge:

            def handle_edge(coord):
                return data[*coord]
        elif self.wrap == "wrap":

            def handle_edge(coord):
                return data[*(x % data.shape[idx] for idx, x in enumerate(coord))]
        else:

            def handle_edge(coord):
                for i, x in enumerate(coord):
                    if 0 > x or x >= data.shape[i]:
                        return self.wrap
                return data[*coord]

        adj = self.adj + idx
        out = [handle_edge(idx) for idx in adj]
        return [data[*idx]] + out

    def _get_linear_neighbors(self, coord, data, cheb_r, edge=False):
        # TODO: Hardcoded wrap
        neighbors = range(cheb_r[0] * -1, cheb_r[1] + 1)
        idx = tuple(
            tuple(
                c if idx != 0 else (c + r) % data.shape[0]
                for idx, c in enumerate(coord)
            )
            for r in neighbors
        )
        return tuple(data[i] for i in idx)

    def _get_moore_neighbors(self, coord, data, cheb_r, edge=False):
        dimensions = data.ndim
        if data.ndim == 1:
            return self._get_linear_neighbors(coord, data, cheb_r, edge)
        if dimensions < 1:
            raise ValueError("dimension must be gte 1")

        if not edge:

            def handle_edge(coord):
                return data[*coord]
        elif self.wrap == "wrap":

            def handle_edge(coord):
                return data[*(x % data.shape[dim] for dim, x in enumerate(coord))]
        else:

            def handle_edge(coord):
                for i, x in enumerate(coord):
                    if 0 > x or x >= data.shape[i]:
                        return self.wrap
                return data[*coord]

        center = tuple(coord)
        currcoords = (center,)
        oldcoords = set(currcoords)
        out = []
        no_center = tuple(chain(range((cheb_r[0] * -1), 0), range(1, cheb_r[1] + 1)))
        for dim in range(0, dimensions):
            for curr_coord, direction in (
                (curr_coord, direction)
                for curr_coord in currcoords
                for direction in no_center
            ):
                new_coord = tuple(
                    el if idx != dim else el + direction
                    for idx, el in enumerate(curr_coord)
                )
                oldcoords.add(new_coord)
                out.append(handle_edge(new_coord))
            currcoords = tuple(oldcoords)
        # Decouple center
        # Switch to TF for GPU
        return [data[center]] + out

    def __rework__get_neumann_neighbors(
        self, coord, data, manhattan_r: int = 1, edge=False
    ) -> np.ndarray:
        """
        Usage:
            Generates a Von Neumann neighborhood, by given dimensions (>1) and range
        Parameters:
            dimensions
            manhattan_range
        Returns:
            array containing indexes of a Von Neuman neighborhood with center abs 0
        """
        dimensions = data.ndim
        if dimensions < 1:
            raise ValueError("dimension must be gte 1")
        if dimensions == 1:
            return self._get_linear_neighbors(coord, data, manhattan_r, self.wrap, edge)
        center = list(coord)
        # center = [0 for _ in range(dimensions)]
        finalcoords = [
            center,
        ]
        ndimension_coords = {}

        if not edge:

            def handle_edge(coord):
                return data[*coord]
        elif self.wrap == "wrap":

            def handle_edge(coord):
                return data[*(x % data.shape[idx] for idx, x in enumerate(coord))]
        else:

            def handle_edge(coord):
                for i, x in enumerate(coord):
                    if 0 > x or x >= data.shape[i]:
                        return wrap
                return data[*coord]

        def split_direction(
            basecoord: list,
            index: int,
            dimension: int,
            finalcoords: list,
            n_dimension_coords: dict,
        ) -> tuple:
            """
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
            """
            # TODO: Rework this eventually (works for now)
            temp_dcoords = n_dimension_coords.copy()
            temp_finalcoords = finalcoords.copy()
            if dimension not in temp_dcoords:
                temp_dcoords[dimension] = []
            for increment in [-manhattan_r[0], manhattan_r[1]]:
                new_coord = basecoord.copy()
                new_coord[index] += increment
                temp_finalcoords.append(new_coord)
                temp_dcoords[dimension].append(new_coord)
            return temp_finalcoords, temp_dcoords

        # R = 1
        for index in range(len(center)):
            finalcoords, ndimension_coords = split_direction(
                center, index, index + 1, finalcoords, ndimension_coords
            )
        # R > 1
        for _R in range(2, max(manhattan_r) + 1):
            new_ndimension_coords = {}
            # for dimension in range(1, dimensions+1):
            #     for coords in ndimension_coords[dimension]:
            #         for index, axis_coord in enumerate(coords[:dimension]):
            nested_loop = [
                (index, axis_coord, coords, dimension)
                for dimension in range(1, dimensions + 1)
                for coords in ndimension_coords[dimension]
                for index, axis_coord in enumerate(coords[:dimension])
            ]
            for index, axis_coord, coords, dimension in nested_loop:
                if axis_coord == center[dimension]:
                    finalcoords, new_ndimension_coords = split_direction(
                        coords, index, dimension, finalcoords, new_ndimension_coords
                    )
                else:
                    if dimension not in new_ndimension_coords:
                        new_ndimension_coords[dimension] = []
                    straight_direction = coords.copy()
                    direction = -1 if axis_coord < center[dimension] else 1
                    straight_direction[index] = axis_coord + direction
                    new_ndimension_coords[dimension].append(straight_direction)
                    finalcoords.append(straight_direction)
                    break
            ndimension_coords = new_ndimension_coords
        # TODO: left
        # idx = np.array(sorted(finalcoords)).T
        out = [handle_edge(idx) for idx in finalcoords]
        return out

    def __legacy__graze_all_iterative(self, data, left, wrap):
        """Obsolete grid processing logic"""
        new_data = np.zeros(data.shape, dtype=data.dtype)

        if self.lr_range is None:
            c_range = reduce_mnc(self.chicks.resolver.neighbor_count, data.ndim)
            b, e = split_mnc(c_range, left)
        else:
            b, e = self.lr_range

        shape = np.zeros(data.shape)
        bit_region = (slice(b, -e) for _ in range(data.ndim))
        shape[*bit_region] = 1
        mid_mask = np.where(shape == 1)
        edge_mask = np.where(shape == 0)
        for i in range(mid_mask[0].size):
            idx = tuple(mid_mask[j][i] for j in range(data.ndim))
            result = self.chicks.graze(idx, data, left, wrap, edge=False)
            new_data[idx] = result
        for i in range(edge_mask[0].size):
            idx = tuple(edge_mask[j][i] for j in range(data.ndim))
            new_data[idx] = self.chicks.graze(idx, data, left, wrap, edge=True)
        return new_data

    # def graze_blade(self, data, idx, left, wrap="wrap", edge=True):
    #     # return self.chicks[idx].graze(idx, data, left, wrap)
    #     return self.chicks.graze(idx, data, left, wrap, edge)

    # def graze_blade(self, data, idx, left, wrap):
    #     # return self.chicks[idx].graze(idx, data, left, wrap)
    #     return self.chicks[0].graze(idx, data, left, wrap)

    # def graze_all(self, data, left, wrap):
    #     new_data = np.zeros(data.shape, dtype=data.dtype)
    #     for idx in np.ndindex(data.shape):
    #         new_data[idx] = self.chicks.graze(
    #             idx, data, left, wrap, edge=True)
    #     return new_data
    #

    # def hatch(self, value):
    #     ##I forgot what this was meant for
    #     ##I suspect it was a concept for multi-flocks
    #     self.side_effect(leftovers)
    #     return sieved


# class Flock:
#     def __init__(self, chicks, head) -> None:
#         self.chicks = chicks
#         self.head = head
#
#     # def graze_blade(self, data, idx, left, wrap):
#     #     # return self.chicks[idx].graze(idx, data, left, wrap)
#     #     return self.chicks[0].graze(idx, data, left, wrap)
#
#     def graze_all(self, data, left, wrap):
#         new_data = np.zeros(data.shape, dtype=data.dtype)
#         for idx in np.ndindex(data.shape):
#             new_data[idx] = self.chicks[0].graze(
#                 idx, data, left, wrap, edge=True)
#         return new_data
#
#     def graze_blade(self, data, idx, left, wrap="wrap", edge=True):
#         # return self.chicks[idx].graze(idx, data, left, wrap)
#         return self.chicks[0].graze(idx, data, left, wrap, edge)
#
#     def graze_all(self, data, left, wrap):
#         new_data = np.zeros(data.shape, dtype=data.dtype)
#
#         test = False
#         if self.chicks[0].mode == 'slice':
#             test = True
#         c_range = reduce_mnc(
#             self.chicks[0].resolver.neighbor_count, data.ndim, test)
#         b, e = split_mnc(c_range, left)
#         c_range = c_range-1
#         shape = np.zeros(data.shape)
#         slis = (slice(b, -e) for _ in range(data.ndim))
#         shape[*slis] = 1
#         mid = np.where(shape == 1)
#         edge = np.where(shape == 0)
#         for i in range(mid[0].size):
#             idx = tuple(mid[j][i] for j in range(data.ndim))
#             new_data[idx] = self.chicks[0].graze(
#                 idx, data, left, wrap, edge=False)
#         for i in range(edge[0].size):
#             idx = tuple(edge[j][i] for j in range(data.ndim))
#             new_data[idx] = self.chicks[0].graze(
#                 idx, data, left, wrap, edge=True)
#         return new_data
#
#     # def hatch(self, value):
#     #     ##I forgot what this was meant for
#     #     ##I suspect it was a concept for multi-flocks
#     #     self.side_effect(leftovers)
#     #     return sieved


# class Head:
#     def __init__(self) -> None:
#         self.pre_effect = lambda _, __: __
#         self.post_effect = lambda _, __: __
#
#     def pre_spit(self, pre, value):
#         self.pre_effect(pre, value)
#
#     def post_crack(self, egg, value):
#         self.post_effect(egg, value)
#
