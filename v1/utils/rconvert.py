from math import log2
from itertools import product, repeat

def gen_rulespace(pow=0, in_symbols=['0', '1'], crashmypc=False):
    #This can and will eat your memmory nom nom nom nom
    if not crashmypc:
        return
    return product(in_symbols, repeat=len(in_symbols)**pow)

def calc_rulespace(pow=0, in_system=2, out_system=1, crashmypc=False):
    #This can and will also nom memmory
    if not crashmypc:
        return
    return in_system**in_system**pow

# print("test", calc_rulespace())

# print("aaa", *gen_rulespace(1, in_symbols=['0', '1', '2']))
# print(len([*gen_rulespace(0, in_symbols=['0', '1'])]))
    
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


# print(decstr_to_binstr(110, 256))
# print(binstr_to_decstr('01101110'))
# print(binstr_to_decstr('01110110'))