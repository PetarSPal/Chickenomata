"""
Rule processing logic
"""

from math import log
import numpy as np
from v1.utils.calc import _log


class Raptor:
    def __init__(
        self,
        rule=None,
        in_system: int = 0,
        num_outputs: int = 1
    ) -> None:
        """
        Object housing a rule and other state relevant to the rule

        Parameters
        ----------
        rule : np.ndarray
            Rule is a collection housing decimal integers of arbitrary numerical system
            It is read similar to Wolfram code (right to left)
        in_system: int
            The numeric system used for the rule.
            2 = binary, 3 = ternary and so on.
            
        num_ouputs: int
            The expected number of outputs after processing the rule.
            Must be power of in_system and <= rule.size
            Example:
                in_system=3 -> num_outputs in (1,3,9,27,81...)
        
        Example usage
        ------
            For -> Binary input, 3 neighbors:
                rule = [0,1,0,1,1,1,1,0]
                my_raptor = Raptor(2,rule)
        """
        self._rule = rule
        self._num_outputs = None
        self._in_system = None
        self.num_outputs = num_outputs
        self.in_system = in_system
        # self._mode = 'legacy_tree'
        # self._mode = 'std_mem'
        self._mode = 'np'
        
        if self._mode == 'np':
            shape = np.full((self.neighbor_count+self.num_outputs-1,), self.in_system)
            self._rule = np.flip(np.asarray(self._rule)).reshape(shape)
        
        #TODO - add caching / other optimizations
        #TODO - onsider raptors in-between raptors
        #TODO - pre/post
        #TODO - investigate other automata type compatibility. add replacement ca.
        
        
    def _validate(self, rule_len=None, insys=None, numout=None):
        rule_len = rule_len or len(self.rule)
        numout = numout or self.num_outputs
        insys = insys or self.in_system
        if insys == 0:
            in_system = 0
            if len(self.rule) != 0:
                raise Exception("Rule length not 0 for in-sys 0")
        else:
            in_system = insys or self.in_system
            if not _log(rule_len, in_system)[0]:
            # if rule_len % in_system != 0 and rule_len != 1:
                raise Exception("Rule length not power of in_system")
        if not _log(numout, insys)[0]:
            raise ValueError(
                f"""Invalid num_outputs = {numout},
                    expected pow of {self.in_system}""")
        if 0 > numout > rule_len:
            raise ValueError("num_outputs less than 0 or greather than rule")
            
    @property
    def num_outputs(self):
        return self._num_outputs
    
    @num_outputs.setter
    def num_outputs(self, value: int):
        """Possbile output count

        Returns:
            _type_: int
        """
        ##TODO: VALIDATION -> MUST BE POW of in_sys, must be lesser than rule len
        if self._rule and self._in_system:
            self._validate(numout=value) 
        if self._in_system and self._neighbor_count:
            self._in_system = self._calc_in_system(len(self.rule), self._neighbor_count, value)
            self._neighbor_count = self._calc_neighbor_count(len(self.rule), self._in_system, value)
        self._num_outputs = value
        
    @property
    def in_system(self):
        """Numeric system (N. possbile inputs)

        Returns:
            _type_: int
        """
        return self._in_system
    
    @in_system.setter
    def in_system(self, value: int):
        if self._rule:
            self._validate(insys=value) 
        self._neighbor_count = self._calc_neighbor_count(
                len(self.rule), value, self.num_outputs)
        # if self._num_outputs:
        self._num_outputs = self._calc_num_outputs(len(self.rule), self.neighbor_count, value)
        self._in_system = value

    @property
    def rule(self):
        """Rule

        Returns:
            _type_: Undefined
        """
        return self._rule
    
    @rule.setter
    def rule(self, value: list):
        if self.in_system:
            self._validate(rule_len=len(value))
        self._neighbor_count = self._calc_neighbor_count(
                len(value), self.in_system, self.num_outputs)    
        self._rule = value
        
    
    @property
    def neighbor_count(self):
        """Expected N. of neighors to process

        Returns:
            _type_: int
        """
        return self._neighbor_count
    
    def _interpreter(self, in_neighborhoods):
        if self._mode == 'std_mem':
            return self.__legacy__apply_rule_std(in_neighborhoods, self.in_system, self.num_outputs, self.rule)
        elif self._mode == 'legacy_tree':
            return self.__legacy__apply_rule(in_neighborhoods, self.in_system, self.num_outputs, self.rule)
        elif self._mode == 'np':
            return self._apply_rule_np(in_neighborhoods, self.in_system, self.num_outputs, self.rule)
    
    def io(self, input_neighbors=None):
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
            raise Exception(f"Expected {self._neighbor_count} neighbors got {len(input_neighbors)}")
        return self._interpreter(input_neighbors)
    
        
    def _apply_rule_np(
    #     rule: np.ndarray,
    #     in_neighbors: np.ndarray | None = None,
    #     in_system: int = 2,
    #     output: int = 1
    # ) -> np.ndarray:
        self,
        in_neighbors: np.ndarray,
        in_system: int,
        num_outputs: int,
        rule: np.ndarray
    ) -> np.ndarray:
        rule = np.asarray(rule)
        in_neighbors = np.asarray(in_neighbors)
        if not in_neighbors.size and num_outputs == rule.size:
            return rule
        # shape = np.full((in_neighbors.size+num_outputs-1,), in_system)
        # rule = np.flip(rule).reshape(shape)
        return rule[*in_neighbors].flatten()

    def __legacy__get_rule_slice(self, n: int, in_system: int, rule: np.ndarray = np.empty(())):
        '''
        Attempts to divide rule evenly, proportional to in_system
        Expects pre-validated inputs (does not validate)
        Returns the n-th slice
        '''
        n, in_system = int(n), int(in_system)
        if n < 0 or n >= in_system:
            raise ValueError("min n = 0, max n = in_system")
        step = len(rule)//in_system
        return rule[step*n:step*(n+1)]


    def __legacy__apply_rule(
            self,
            in_neighbors: np.ndarray,
            in_system: int,
            num_outputs: int,
            rule: np.ndarray) -> np.ndarray:
        '''
        Uses divide and conquer to search the rule for the output
        Suboptimal for rule sizes that can be stored in memory
        Implemented because it seems easier to reason with than large decimals
        Parameters:
            in_neighbors - neighbor elements to be processed
            in_system - possible neighbor values
                E.g. possible neighbors in (0, 1) -> in_system = 2
            rule - rule
        Returns:
            Result after applying rule to the neighbors
        '''
        #TODO: Implement hybrid approach
        part_rule = np.array(rule[::-1])
        part_neighbors = np.array(in_neighbors)
        # while len(part_neighbors) >= 1:
        while len(part_rule) > num_outputs:
            current_element = part_neighbors[0]
            remaining_neighbors = part_neighbors[1:]
            partial_rule = self.__legacy__get_rule_slice(current_element, in_system, part_rule)
            part_rule, part_neighbors = partial_rule, remaining_neighbors
        if part_neighbors.size > 0:
            # print(part_neighbors)
            ##TODO: handle rule/input sizes mistmatch better
            return np.array([])
        return part_rule


    def __legacy__apply_rule_std(
            self,
            in_neighbors: np.ndarray,
            in_system: int,
            num_outputs: int,
            rule: np.ndarray) -> np.ndarray:
        ##TODO: Both apply rules currently can't handle insufficient neighbors reliably
        ## Cause different issues. divconq errors out, std provides a wrong value
        ## This is expected to be validated before calling, but still worth mentioning
        
        inp = tuple(enumerate(in_neighbors[::-1]))
        j = int(log(num_outputs, in_system))
        decimals = tuple((in_system**(i+j))*v for i,v in inp)
        decimal = sum(decimals)
        if decimal >= len(rule):
            return np.asarray([])
        return np.asarray(rule[::-1][decimal:decimal+num_outputs])


    def _calc_neighbor_count(
            self,
            rule_size: int,
            in_system: int = 2,
            num_outputs: int = 1) -> int:
        '''
        Calculates anticipated total neighbor count (center element included)
        Parameters
            rule_len - size of the rule
            in_system - number of possible values in a rule element
                Example if only rule values are 0 or 1, then in_system=2
            num_outputs - number of output elements, default 1
        '''
        if in_system < 2 or num_outputs in (0, rule_size):
            return 0
        valid, output_depth_offset = _log(num_outputs, in_system)
        if not valid:
            raise ValueError(
                f"""Invalid num_outputs = {num_outputs},
                    expected pow of {in_system}""")
        valid, power = _log(rule_size, in_system)
        if not valid:
            raise ValueError(
                f"""Invalid rule_len = {rule_size},
                    in_system {in_system},
                    expected rule_len to be pow of in_system""")
        nc = power - output_depth_offset
        if nc < 0:
            raise ValueError(
                f"""Invalid in_system = {in_system}
                    or num_outputs = {num_outputs} ->
                    num_outputs perhaps too high?""")
        return nc


    def _calc_in_system(
            self,
            rule_size: int,
            neighbor_count: int = 0,
            num_outputs: int = 1) -> int:
        '''
        Calculates anticipated in system
        Parameters
            rule_size - size of the rule
            neighbor_count - number of total neighbors (including center)
            num_outputs - number of output elements, default 1
        '''
        insys = int((rule_size//num_outputs)**(1 / neighbor_count))
        valid, _ = _log(rule_size, insys)
        if not valid:
            raise ValueError(
                f"""Invalid value combination ->
                    rule_size: {rule_size},
                    neighbor_count: {neighbor_count},
                    num_outputs: {num_outputs}""")
        valid, _ = _log(num_outputs, insys)
        if not valid:
            raise ValueError(
                f"""Invalid insys for num_outputs = {num_outputs},
                    expected numout to be pow of {insys}""")
        return insys

    def _calc_num_outputs(
            self,
            rule_size: int,
            neighbor_count: int = 0,
            in_system: int = 2) -> int:
        '''
        Calculates anticipated number of outputs
        Parameters
            rule_size - size of the rule
            neighbor_count - number of total neighbors (including center)
            in_system - numeric system (2 = binary)
        '''
        numout, rem = divmod(rule_size, (in_system**neighbor_count))
        if rem:
            raise ValueError(
                f"""Invalid value combination ->
                    rule_size: {rule_size},
                    neighbor_count: {neighbor_count},
                    in_system: {in_system}""")
        return numout


# class RaptorMini:
#     def __init__(
#         self,
#         rule=None,
#     ) -> None:
#         """
#         """
#         self._rule = rule
        
        
#     def _apply_rule_np(
#     #     rule: np.ndarray,
#     #     in_neighbors: np.ndarray | None = None,
#     #     in_system: int = 2,
#     #     output: int = 1
#     # ) -> np.ndarray:
#         self,
#         in_neighbors: np.ndarray,
#         in_system: int,
#         num_outputs: int,
#         rule: np.ndarray
#     ) -> np.ndarray:
#         rule = np.array(rule)
#         in_neighbors = np.array(in_neighbors)
#         if not in_neighbors.size and num_outputs == rule.size:
#             return rule
#         shape = np.full((in_neighbors.size+num_outputs-1,), in_system)
#         rule = np.flip(rule).reshape(shape)
#         return rule[*in_neighbors].flatten()