from math import log
import numpy as np
from Logic.calc import power_of_x, calc_neighbor_count
from Logic. rule import apply_rule_divconq


class Raptor:
    def __init__(self, rule=None, in_system: int = 0, num_outputs: int = 1) -> None:
        """Create a raptor (rule) object
        
        Args:\n
            in_system - count of possible input values\n
            num_outputs - count of outputs\n
            rule - listlike object, len should be power of in_system\n
        
        Example:\n
        Binary input, 3 neighbors:\n
            rule = [0,1,0,1,1,1,1,0]\n
            myRap = Raptor(2,rule)
        """
        
        #TODO - define rule data model, infer in-system from rule?
        #TODO - cachining or other optimizations to processing
        #TODO - figure out how to nest raptors in raptors
        #TODO - figure out how to override processing (E.g. 10 in-system rap only having 10 sub-rules ignoring neighbor size)
        #TODO - add support for other types of automata e.g. replacement to support asymmetric number of outputs (perhaps add to Claw?)
        
        self._rule = rule
        self.num_outputs = num_outputs
        self.in_system = in_system
        # self._neighbor_count = None
        #is specifying output system needed?
        # self.out_system = out_system
        
        # self.static = 1
        # self.memory = 1
        
    @property
    def num_outputs(self):
        return self._num_outputs
    
    @num_outputs.setter
    def num_outputs(self, value: int):
        if value < 0:
            raise Exception("invalid num outputs")
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
        self._neighbor_count = calc_neighbor_count(
                len(self.rule), value, self.num_outputs)
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
        self._neighbor_count = calc_neighbor_count(
                len(value), self.in_system, self.num_outputs)
        self._rule = value
        
    
    @property
    def neighbor_count(self):
        """Expected N. of neighors to process

        Returns:
            _type_: int
        """
        return self._neighbor_count
        
    def _validate(self, rule_len=None, insys=None):
        rule_len = rule_len or len(self.rule)
        if insys == 0:
            in_system = 0
            if len(self.rule) != 0:
                raise Exception("Rule length not 0 for in-sys 0")
        else:
            in_system = insys or self.in_system
            if not power_of_x(rule_len, in_system):
            # if rule_len % in_system != 0 and rule_len != 1:
                raise Exception("Rule length not power of in_system")
    
    def _interpreter(self, in_neighborhoods):
        return apply_rule_divconq(in_neighborhoods, self.in_system, self.num_outputs, self.rule)
    
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
    
    
# a = Raptor(2, 1)
# a.rule=[1,1,5,4]
# print(a.neighbor_count)
# print(a.io([0,0]))



# def _isPowerOfX(n, x):
#     pow = 0
#     if (n == 0):
#         return False
#     while (n != 1):
#         if (n % x != 0):
#             return False
#         n = n // x
#         pow += 1
            
#     return pow
    
    
# print(_isPowerOfX(1, 3))


# pow 0 -> rl 1 = only 1 output
# 1 -> 1
# pow 1 -> rl = num_sys => 1-2 outputs
# 11 -> 1

# pow 2 -> rl = 1-4 outputs
# 1111 ->


# pow 2
# 1111
# output 1
# req 2 ne
# 11
# 1

# output 2
# req 1 ne
# 11

# output 4
# req 0 ne
# 1111

# output 3
# undefined behaviour
# requires alternative handling
# 111