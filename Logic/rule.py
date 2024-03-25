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
        in_neighbors: int, in_system: int, rule: np.ndarray) -> np.ndarray:
    '''
    Uses divide and conquer to search the rule for the output
    Highly suboptimal for rule sizes that can be stored in memory
    Parameters:
        in_neighbors - neighbor elements to be processed
        in_system - possible neighbor values
            E.g. possible neighbors in (0, 1) -> in_system = 2
        rule - rule
    Returns:
        Result after applying rule to the neighbors
    '''
    #TODO: Implement hybrid approach
    #TODO: More than one output element
    part_rule = np.array(rule[::-1])
    part_neighbors = np.array(in_neighbors)
    while len(part_neighbors) >= 1:
        current_element = part_neighbors[0]
        remaining_neighbors = part_neighbors[1:]
        partial_rule = get_rule_slice(current_element, in_system, part_rule)
        part_rule, part_neighbors = partial_rule, remaining_neighbors
    return part_rule