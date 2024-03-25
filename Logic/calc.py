from math import log


def power_of_x(n: int, x: int) -> tuple:
    '''
    Checks if n is a power of x
    Returns tuple
        First value contains bool for truth
        Second value contains the power (defaults to 0 if not)
    '''
    n, x = int(n), int(x)
    power = 0
    if n == 0:
        return (False, 0)
    if x == 1:
        return (True, 0)
    while n != 1:
        if (n % x) != 0:
            return (False, 0)
        n = n // x
        power += 1
    return (True, power)


def calc_neighbor_count(
        rule_len: int, in_system: int, num_outputs: int = 1) -> int:
    '''
    Calculates anticipated neighbor count (center element included)
    Parameters
        rule_len - size of the rule
        in_system - number of possible values in a rule element
            Example if only rule values are 0 or 1, then in_system=2
        num_outputs - number of output elements, default 1
    '''
    if num_outputs < 0:
        raise ValueError("num_outputs not gte 0")
    if num_outputs in (0, rule_len):
        return 0
    nc, rem = divmod(log(rule_len, in_system), num_outputs)
    if rem:
        raise ValueError("Invalid parameter combination")
    return int(nc)