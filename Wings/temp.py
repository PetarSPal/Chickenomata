from math import log2
from itertools import product

def rules_2():
    return ['0', '1']

def rules_4():
    return [x+y for x in rules_2() for y in rules_2()]

# print(rules_4())
# print(list(permutations("01", r=2)))
    
def rules_16():
    return [x+y for x in rules_4() for y in rules_4()]
    
def rules_256():
    return [x+y for x in rules_16() for y in rules_16()]

print(list("".join(x) for x in product('01', repeat=3)))

# print(rules_256())
    
def decstr_to_binstr(rule, rule_count):
    rule_size = int(log2(rule_count))
    return bin(rule)[2:].zfill(rule_size)
    
def decrules_to_binrules(cls, rules, rule_count):
    args = map(int, rules), repeat(rule_count)
    return tuple(map(cls.decstr_to_binstr, *args))
    
def binstr_to_decstr(bin_rule):
    return str(int(bin_rule, 2))
    
def binrules_to_decrules(rules):
    return tuple(map(binstr_to_decstr, rules))

    
def dec_rule(rule):
    if isinstance(rule, (list, tuple)):
        return binrules_to_decrules(rule)
    return binstr_to_decstr(rule)


print(decstr_to_binstr(110, 256))
print(binstr_to_decstr('01101110'))
print(binstr_to_decstr('01110110'))