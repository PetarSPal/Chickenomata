"""
Rule processing logic
"""

from math import log
import numpy as np
import numpy.typing as npt
from v1.utils.calc import _log
from functools import cache, cached_property


class Resolver:
    def __init__(
        self,
        rule: npt.ArrayLike = np.empty([]),
        cfg=None,
        insys: int = 2,
        numout: int = 1,
    ) -> None:
        """
        Rule resolver
        Stores a rule and and other information pertaining to the rule
        Takes neighbors -> outputs result

        Parameters
        ----------
        rule : np.ndarray
            ArrayLike housing decimal integers of arbitrary numerical system
            Resembles Wolfram code (reading occurrs right to left)
        in_system: int
            The numeric system used for the rule.
            2 = binary, 3 = ternary, etc.

        num_ouputs: int
            The expected number of outputs after processing the rule.
            Must be power of in_system and <= rule.size
            Example for in_system = 3:
                num_outputs MUST be in (1,3,9,27,81...)

        Example usage
        ------
            For -> Binary input, 3 neighbors:
                rule = [0,1,0,1,1,1,1,0]
                my_raptor = Raptor(2,rule)
        """
        rule = np.asarray(rule)
        self.cfg = cfg
        if cfg is not None:
            insys = cfg.in_system
            numout = cfg.num_outputs
        self._validate(rule, insys, numout)
        self._neighbor_count = self._calc_neighbor_count(rule, insys, numout)
        self._rule = rule
        self._num_outputs = numout
        self._in_system = insys
        # self._mode = 'legacy_tree'
        # self._mode = 'std_mem'
        self._mode = "np"

        if self._mode == "np":
            self._nest_rule()

    @property
    def num_outputs(self) -> int:
        return self._num_outputs

    @property
    def in_system(self) -> int:
        """Numeric system (N. possbile inputs)"""
        return self._in_system

    @property
    def rule(self) -> npt.NDArray:
        """Rule"""
        return self._rule

    @property
    def neighbor_count(self) -> int:
        """Expected N. of neighors to process"""
        return self._neighbor_count

    @num_outputs.setter
    def num_outputs(self, value: int):
        self._recalculate(numout=value)
        self._num_outputs = value

    @in_system.setter
    def in_system(self, value: int):
        self._recalculate(insys=value)
        self._in_system = value

    @rule.setter
    def rule(self, value: npt.ArrayLike):
        rule = np.asarray(value)
        self._recalculate(rule=rule)
        self._rule = rule

    def _fill_missing(self, rule=None, insys=None, numout=None):
        """Take current values for missing args"""
        rule = rule if rule is not None else self.rule
        numout = numout if numout is not None else self.num_outputs
        insys = insys if insys is not None else self.in_system
        return rule, insys, numout

    def _validate(self, rule=None, insys=None, numout=None):
        """Ensure settings are somewhat reasonable"""
        rule, insys, numout = self._fill_missing(rule, insys, numout)
        if insys == 0 and rule.size != 0:
            raise Exception(
                "Rule length: {} not 0 for in-sys: {}".format(len(rule), insys)
            )
        elif insys == 0 and not not _log(rule.size, insys)[0]:
            raise Exception(
                "Rule length: {} not power of in_system: {}".format(rule.size, insys)
            )
        if not _log(numout, insys)[0]:
            raise ValueError(
                """Invalid num_outputs: {} ->
                    expected pow of {}""".format(numout, self.in_system)
            )
        if 0 > numout > rule.size:
            raise ValueError(
                "num_outputs: {} -> less than 0 or greather than rule".format(numout)
            )

    def _recalculate(self, rule=None, insys=None, numout=None):
        """Recalculate other settings upon changing one setting"""
        self._validate(rule, insys, numout)
        if insys is not None:
            self._num_outputs = self._calc_num_outputs(
                self.rule, self.neighbor_count, insys
            )
        if numout is not None:
            self._in_system = self._calc_in_system(
                self.rule, self._neighbor_count, numout
            )
        if rule is not None:
            rule = np.asarray(rule)
        rule, insys, numout = self._fallback(rule, insys, numout)
        self._neighbor_count = self._calc_neighbor_count(
            self.rule, self._in_system, numout
        )

    def _nest_rule(self):
        """Nest the rule array"""
        rule_dim = self.neighbor_count + self.num_outputs - 1
        shape = np.full(rule_dim, self.in_system)
        self._rule = np.flip(self._rule).reshape(shape)

    def _calc_neighbor_count(
        self, rule: npt.NDArray, insys: int = 2, num_outputs: int = 1
    ) -> int:
        """Calculates anticipated total neighbor count (incl. center)"""
        rule_size = rule.size
        if insys < 2 or num_outputs in (0, rule_size):
            return 0
        valid, output_depth_offset = _log(num_outputs, insys)
        if not valid:
            raise ValueError(
                """Invalid num_outputs = {},
                    expected pow of {}""".format(num_outputs, insys)
            )
        valid, power = _log(rule_size, insys)
        if not valid:
            raise ValueError(
                """Invalid rule_len = {},
                    insys {},
                    expected rule_len to be pow of in_system""".format(rule_size, insys)
            )
        nc = power - output_depth_offset
        if nc < 0:
            raise ValueError(
                """Invalid in_system = {}
                    or num_outputs = {} ->
                    num_outputs perhaps too high?""".format(insys, num_outputs)
            )
        return nc

    def _calc_in_system(
        self, rule: npt.NDArray, neighbor_count: int = 0, num_outputs: int = 1
    ) -> int:
        """Calculates anticipated input numeric system"""
        rule_size = rule.size
        insys = int((rule_size // num_outputs) ** (1 / neighbor_count))
        valid, _ = _log(rule_size, insys)
        if not valid:
            raise ValueError(
                """Invalid value combination ->
                    rule_size: {},
                    neighbor_count: {},
                    num_outputs: {}""".format(rule_size, neighbor_count, num_outputs)
            )
        valid, _ = _log(num_outputs, insys)
        if not valid:
            raise ValueError(
                """Invalid insys for num_outputs = {},
                    expected numout to be pow of {}""".format(num_outputs, insys)
            )
        return insys

    def _calc_num_outputs(
        self, rule: npt.NDArray, neighbor_count: int = 0, insys: int = 2
    ) -> int:
        """Calculates anticipated number of outputs"""
        rule_size = rule.size
        numout, rem = divmod(rule_size, (insys**neighbor_count))
        if rem:
            raise ValueError(
                """Invalid value combination ->
                    rule_size: {}, neighbor_count: {}, insys: {}""".format(
                    rule_size, neighbor_count, insys
                )
            )
        return numout

    def _handle_mode(self, in_neighborhoods):
        if self._mode == "std_mem":
            return self.__legacy__apply_rule_std(
                in_neighborhoods, self.in_system, self.num_outputs, self.rule
            )
        elif self._mode == "legacy_tree":
            return self.__legacy__apply_rule(
                in_neighborhoods, self.in_system, self.num_outputs, self.rule
            )
        elif self._mode == "np":
            return self._apply_rule_np(in_neighborhoods)

    def resolve(self, input_neighbors=None):
        """Process input_neighbors based on the rule and return the output

        Args:
            input_neighbors (_type_): listlike object of neighbor values to process

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        if input_neighbors is None:
            input_neighbors = []
        if len(input_neighbors) != self._neighbor_count:
            raise Exception(
                "Expected {} neighbors got {}".format(
                    self._neighbor_count, len(input_neighbors)
                )
            )
        return self._handle_mode(input_neighbors)

    def resolve_batch(self, inp: npt.ArrayLike | None = None):
        inp = np.asarray(inp)
        if (inp is None or not inp.size) and self.num_outputs == self.rule.size:
            # TODO: I need a count here, since 0 inp is not practically used solve later
            return self.rule
        if inp.shape[0] != self._neighbor_count:
            raise Exception(
                "Expected {} neighbors got {}".format(
                    self._neighbor_count, inp.shape[0]
                )
            )
            # TODO: No point including obsolete processing methods here
        return self.rule[*inp].flatten()

    def _apply_rule_np(self, in_neighbors: npt.ArrayLike) -> npt.NDArray:
        in_neighbors = np.asarray(in_neighbors)
        if not in_neighbors.size and self.num_outputs == self.rule.size:
            return self.rule
        return self.rule[*in_neighbors].flatten()

    def __legacy__get_rule_slice(
        self, n: int, in_system: int, rule: np.ndarray = np.empty(())
    ):
        """
        Attempts to divide rule evenly, proportional to in_system
        Expects pre-validated inputs (does not validate)
        Returns the n-th slice
        """
        n, in_system = int(n), int(in_system)
        if n < 0 or n >= in_system:
            raise ValueError("min n = 0, max n = in_system")
        step = len(rule) // in_system
        return rule[step * n : step * (n + 1)]

    def __legacy__apply_rule(
        self,
        in_neighbors: np.ndarray,
        in_system: int,
        num_outputs: int,
        rule: np.ndarray,
    ) -> np.ndarray:
        """
        Obsolete rule processing logic
        Parameters:
            in_neighbors - neighbor elements to be processed
            in_system - possible neighbor values
                E.g. possible neighbors in (0, 1) -> in_system = 2
            rule - rule
        Returns:
            Result after applying rule to the neighbors
        """
        # TODO: Implement hybrid approach?
        part_rule = np.array(rule[::-1])
        part_neighbors = np.array(in_neighbors)
        while len(part_rule) > num_outputs:
            current_element = part_neighbors[0]
            remaining_neighbors = part_neighbors[1:]
            partial_rule = self.__legacy__get_rule_slice(
                current_element, in_system, part_rule
            )
            part_rule, part_neighbors = partial_rule, remaining_neighbors
        if part_neighbors.size > 0:
            # TODO: handle rule/input sizes mistmatch?
            return np.array([])
        return part_rule

    def __legacy__apply_rule_std(
        self,
        in_neighbors: np.ndarray,
        in_system: int,
        num_outputs: int,
        rule: np.ndarray,
    ) -> np.ndarray:
        """Obsolete rule processing logic"""
        # TODO: Handle partial neighbors?
        inp = tuple(enumerate(in_neighbors[::-1]))
        j = int(log(num_outputs, in_system))
        decimals = tuple((in_system ** (i + j)) * v for i, v in inp)
        decimal = sum(decimals)
        if decimal >= len(rule):
            return np.asarray([])
        return np.asarray(rule[::-1][decimal : decimal + num_outputs])
