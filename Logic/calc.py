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
        rule_len: int, in_system: int = 2, num_outputs: int = 1) -> int:
    '''
    Calculates anticipated neighbor count (center element included)
    Parameters
        rule_len - size of the rule
        in_system - number of possible values in a rule element
            Example if only rule values are 0 or 1, then in_system=2
        num_outputs - number of output elements, default 1
    '''
    if in_system < 2:
        return 0
    if num_outputs < 0:
        raise ValueError("num_outputs not gte 0")
    if num_outputs in (0, rule_len):
        return 0
    ##Irrational output depths unsupported in this func
    ##Consider handling irrational output (not pow of in_sys) as a postprocessing automata
    output_depth_offset = log(num_outputs, in_system)
    if output_depth_offset % 1:
        raise ValueError(f"Invalid num_outputs {num_outputs}, expected pow of {in_system}")
    valid, power = power_of_x(rule_len, in_system)
    # base_nc = log(rule_len, in_system)
    # print(base_nc)
    # if base_nc % 1:
    if not valid:
        raise ValueError(f"Invalid rule_len {rule_len}, in_system {in_system}, expected rule_len to be pow of in_system")
    nc = log(rule_len, in_system) - output_depth_offset
    # print('nc', nc)
    return int(nc)