from math import log
from itertools import product, repeat
from functools import cached_property
import numpy as np                                              
    
    # def process_row(self, old_row, settings):
    #     new_row = []
    #     asym = 1 if settings.asym == 'right' and not self.neighbors % 2 else 0
    #     for idx in range(len(old_row)):
    #         offset = self.neighbors//2
    #         elements = ''
    #         beginning = idx-offset+asym
    #         end = idx+self.neighbors-offset+asym
    #         for input_element in range(beginning, end):
    #             wrapped = self._wrap_handler(input_element, old_row, settings.wrap)
    #             elements += str(wrapped)
    #         new_row.append(self.io(elements))
    #     return new_row
    
     
    # def _wrap_handler(self, input_element, row, wrap):
    #     left_bound, right_bound = input_element >= 0, input_element < len(row)
    #     if left_bound and right_bound:
    #         return row[input_element]
    #     if wrap == '0':
    #         return 0
    #     if wrap == '1':
    #         return 1
    #     if not left_bound:
    #         return row[input_element]
    #     if not right_bound:
    #         return row[input_element - len(row)]
    #     return row[input_element]
        
    # @cached_property
    # def rules_4(self):
    #     return ['00', '01', '10', '11']
    
    # @cached_property
    # def rules_16(self):
    #     return [x+y for x in self.rules_4 for y in self.rules_4]
    
    # @cached_property
    # def rules_256(self):
    #     return [x+y for x in self.rules_16 for y in self.rules_16]
    
    # @classmethod    
    # def decstr_to_binstr(cls, rule, rule_count):
    #     rule_size = int(log2(rule_count))
    #     return bin(rule)[2:].zfill(rule_size)
    
    # @classmethod
    # def decrules_to_binrules(cls, rules, rule_count):
    #     args = map(int, rules), repeat(rule_count)
    #     return tuple(map(cls.decstr_to_binstr, *args))
    
    # @classmethod
    # def binstr_to_decstr(cls, bin_rule):
    #     return str(int(bin_rule, 2))
    
    # @classmethod
    # def binrules_to_decrules(cls, rules):
    #     return tuple(map(cls.binstr_to_decstr, rules))

    # @property
    # def rule(self):
    #     return self._rule
    
    # @property
    # def dec_rule(self):
    #     if isinstance(self._rule, (list, tuple)):
    #         return self.binrules_to_decrules(self._rule)
    #     return self.binstr_to_decstr(self._rule)
    
    # @property
    # def neighbors(self):
    #     return self._neighbors
    
    # @property
    # def rule_count(self):
    #     return self._rule_count

    # @rule.setter
    # def rule(self, rule):
    #     self._validate_rule(rule)
    #     prop = self._calc_properties(rule)
    #     self._rule, self._neighbors, self._rule_count = prop


# a = CA('010101010', 4, 3)

# # print(a.neighbor_count)
# print("end:", a._rule_interpreter('0100010001000100', '11'))

a = Data(10, 1)
# a.set_random(2)
a.set_center(1)
print(a.data)
b =a.get_moore_neighbors((0),3)
print("b",b)
# new = [1 for x in range(81)]
# a.mutate_moore_neighbors((0,0,0,0),new,81)
# b =a.get_moore_neighbors((0,0,0,0),81)
# print("b",b)    

# r = Rule(['1','2'])
# print(r.rule)
# r.rule = ['1']

b = CA('010101010', 4, 3)
print(b.neighbor_count)
print("end:", b._rule_interpreter('0100010001000100', '11'))
