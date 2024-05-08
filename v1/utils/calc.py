def reduce_mnc(totalncount: int, dimensions: int) -> int:
    """
    Projects a (Moore) total neighbor count (center included) onto 1D
    (e.g. 3D: 27 -> 2D: 9 -> 1D: 3 -> return 3)
    """
    base = 3 ** (dimensions - 1)
    if not (1 == base):
        reduced_ncount, rem = divmod(totalncount, base)
        if not rem:
            return reduced_ncount
        raise Exception(
            f"invalid neighbor count {totalncount} for {dimensions} dimensions"
        )
    return totalncount


def split_mnc(total_nc: int, tend_left: bool = True) -> tuple:
    """
    Reduces total (Moore) neighbor count (center included) to two chebyshev ranges
        One for each direction of a 1D axis
    If tend_left is true and total_nc is even ->
        Then the first value will be +1 compared to the second
        If tend_left is false second value will be +1
        Otherwise they are the same due to symmetry
    Returns a tuple
    """
    half_distance, even = divmod((total_nc - 1), 2)
    tendl, tendr = int(even and tend_left), int(even and (not tend_left))
    begin, end = (half_distance + tendl, half_distance + tendr)
    return tuple([begin, end])


def _log(n: int, x: int) -> tuple:
    """
    Checks if n is a power of x
    Returns tuple
        First value contains bool for truth
        Second value contains the power (defaults to 0 if not a pow)
    """
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
