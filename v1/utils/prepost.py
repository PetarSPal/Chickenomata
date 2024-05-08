"""
Ad-hoc filters for the purpouse of pre/post or neighborhood adjacency
"""

import numpy as np
from v1.resolver import Resolver


def fit_nc(value, automata, ndim):
    return (
        value[: automata.resolver.neighbor_count],
        value[automata.resolver.neighbor_count :],
    )


def ofit_nc(value, automata, ndim):
    return (
        value[-automata.resolver.neighbor_count :],
        value[: -automata.resolver.neighbor_count],
    )


def sum_treshold_tst(value, automata, ndim):
    l3 = len(value) // 3
    rem = len(value) - (l3 * 3)
    v1 = (sum(value[:l3]) > (l3 // 2) * (automata.resolver.in_system - 1)).astype(int)
    v2 = (sum(value[l3 : l3 * 2]) > l3 // 2 * (automata.resolver.in_system - 1)).astype(
        int
    )
    v3 = (
        sum(value[l3 * 2 : l3 * 3]) > l3 // 2 * (automata.resolver.in_system - 1)
    ).astype(int)
    out = ((v1, v2, v3), rem)
    return out


def sum_filt(value, automata, ndim):
    return [sum(value)], None


def outer_sum_filt(rule):
    def otot(value, automata, ndim):
        # maxsum = (automata.resolver.neighbor_count-1)*(automata.raptor.in_system-1)
        maxsum = (3**ndim) * (automata.resolver.in_system - 1)
        totrap = Resolver(rule, insys=maxsum)
        inner = value[0]
        outer = [sum(value[1:])]
        post_outer = totrap.resolve_batch(outer)
        return [inner, post_outer], None

    return otot


def conway_test_preset():
    def otot(value, automata, ndim):
        inner = value[0]
        outer = sum(value[1:])
        out = np.bitwise_or(outer == 3, np.bitwise_and(inner == 1, outer == 2))
        return [np.array(out).astype(int)], None

    return otot


def conway_test_preset2():
    def otot(value, automata, ndim):
        inner = value[0]
        outer = sum(value[1:])
        reprlo = len(value) // 4
        reprhi = (len(value) + 1) // 3
        out = np.bitwise_or(
            np.isin(outer, range(reprlo, reprhi + 1)),
            np.bitwise_and(inner == 1, outer == reprlo),
        )
        return [np.array(out).astype(int)], None

    return otot


def conway_test_preset3():
    def otot(value, automata, ndim):
        inner = value[0]
        outer = sum(value[1:])
        repr = len(value) // 4
        out = np.bitwise_or(
            outer == repr + 1, np.bitwise_and(inner == 1, outer == repr)
        )
        return [np.array(out).astype(int)], None

    return otot


def blinker_preset():
    def otot(value, automata, ndim):
        # maxsum = (3**ndim)*(automata.resolver.in_system-1)
        inner = value[0]
        outer = sum(value[1:])
        out = np.bitwise_or(
            np.isin(outer, range(2, 3)), np.bitwise_and(inner == 1, outer > 0)
        )
        return [np.array(out).astype(int)], None

    return otot


def test_preset():
    def otot(value, automata, ndim):
        inner = value[0]
        outer = sum(value[1:])
        # out = np.bitwise_or(
        #     np.isin(outer, range(2, 3)), np.bitwise_and(inner == 1, outer > 0))
        out = np.bitwise_or(
            np.isin(outer, range(0, 1)), np.bitwise_and(inner == 1, outer > 3)
        )
        return [np.array(out).astype(int)], None

    return otot


def test_preset2():
    def otot(value, automata, ndim):
        inner = value[0]
        outer = sum(value[1:])
        out = np.bitwise_or(
            np.isin(outer, range(7, 8)), np.bitwise_and(inner == 1, outer > 3)
        )
        return [np.array(out).astype(int)], None

    return otot


def test_preset3():
    def otot(value, automata, ndim):
        inner = value[0]
        outer = sum(value[1:])
        reprlo, lorem = divmod((len(value) - 1), 9)
        lorem = lorem // 4
        reprhi, hirem = divmod(len(value), 10)
        hirem = hirem // 3
        minrepr = min(lorem, hirem)
        maxrepr = max(lorem, hirem)
        out = np.bitwise_or(
            np.isin(outer, range(reprhi * minrepr, reprlo * maxrepr)),
            np.bitwise_and(inner == 1, outer <= (minrepr * hirem)),
        )
        return [np.array(out).astype(int)], None

    return otot


def test_preset4():
    def otot(value, automata, ndim):
        inner = value[0]
        outer = sum(value[1:])
        reprlo, lorem = divmod((len(value) - 1), 9)
        lorem = lorem // 4
        reprlo += 1
        reprhi, hirem = divmod(len(value), 10)
        hirem = hirem // 3
        reprhi += 1
        minrepr = min(lorem, hirem) + 1
        maxrepr = max(lorem, hirem) + 1
        lo = (reprlo * minrepr) - 2
        hi = (reprhi * maxrepr) - 1
        out = np.bitwise_or(
            np.isin(outer, range(lo, hi)), np.bitwise_and(inner == 1, outer == lo)
        )
        return [np.array(out).astype(int)], None

    return otot


def iterate_neighborhood():
    def otot(value, automata, ndim):
        inner, outer = value[0], sum(value[1:])
        return (inner, outer > 0), None

    return otot
