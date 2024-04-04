from math import log
import numpy as np


def get_rule_slice(n: int, in_system: int, rule: np.ndarray = np.empty(())):
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


def apply_rule_divconq(
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
        partial_rule = get_rule_slice(current_element, in_system, part_rule)
        part_rule, part_neighbors = partial_rule, remaining_neighbors
    if part_neighbors.size > 0:
        # print(part_neighbors)
        ##TODO: handle rule/input sizes mistmatch better
        return np.array([])
    return part_rule

def apply_rule_std(
        in_neighbors: np.ndarray,
        in_system: int,
        num_outputs: int,
        rule: np.ndarray) -> np.ndarray:
    ##TODO: Both apply rules currently can't handle insufficient neighbors reliably
    ## Cause different issues. divconq errors out, std provides a wrong value
    ## This is expected to be validated before calling, but still worth mentioning
    
    inp = tuple(enumerate(in_neighbors[::-1]))
    j = output_depth_offset = int(log(num_outputs, in_system))
    decimals = tuple((in_system**(i+j))*v for i,v in inp)
    decimal = sum(decimals)
    if decimal >= len(rule):
        return np.array([])
    return np.array(rule[::-1][decimal:decimal+num_outputs])


# nei = [3,1,2]
# insys = 4
# numout = 1
# # rule = [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
# rule = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0
# ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# ,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# a = apply_rule_divconq(nei, insys, numout, rule)
# print(a)
# b = apply_rule_std(nei, insys, numout, rule)
# print(b)

# 1 3 9


# test = [1,2,3,4,5]
# b = test[:len(test)+1-2]
# print(b)
