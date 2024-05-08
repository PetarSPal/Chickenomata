"""
Ad-hoc rule resolvers for the purpuse of boolean adjacency
"""

import numpy as np
from v1.grass import numpyGrass
from v1.resolver import Resolver
from v1.settings import Cfg
from v1.automata import Automata, Pre
from v1.utils.prepost import iterate_neighborhood, conway_test_preset


def moore_resolver(init_ranges: tuple, desired_range: int, ndim: int, mode="moore"):
    """
    Cellular automata for bit neighborhood morphology
    Can work with assymetric ranges (0,1 | 1,0)
        init_ranges: LR ranges (max 1,1)
        desired_range: desired output range
        ndim: dimensions
        mode: "moore" or "neumann" growth pattern
    """
    if 0 > len(init_ranges) > 2 or init_ranges[0] > 1 or init_ranges[1] > 1:
        raise ValueError(
            "invalid starting ranges {init_ranges}, each must be less than 1"
        )
    cfg = Cfg()
    cfg.runs = desired_range
    cfg.cols = 1 + (desired_range * 2)  # +1 to pad with 0s
    cfg.ndim = ndim
    otot = iterate_neighborhood()
    # rul = [0, 0, 1, 0]
    rul = [1, 1, 1, 0]
    beak = Pre(otot)
    rap = Resolver(rul, cfg=cfg)
    chick = Automata(rap, init_ranges, beak, mode=mode)
    gra = numpyGrass(cfg, dtype="b")
    for _ in range(cfg.runs):
        gra.graze_all(chick)
    # gra._set_center(0)
    return (gra, chick)


def test_resolver(desired_range: int, ndim: int, init_data=None):
    cfg = Cfg()
    cfg.runs = 1
    cfg.cols = 1 + (desired_range * 2)  # +1 to pad with 0s
    cfg.ndim = ndim
    totrap = Resolver([1, 0, 1, 0, 1, 1, 0, 1, 0], insys=9)

    def otot(value, automata, _):
        inner = value[0]
        outer = [sum(value[1:])]
        post_outer = totrap.resolve_batch(outer)
        return [inner, post_outer], None

    # rul = [0, 0, 1, 0]
    rul = [0, 1, 1, 0]
    beak = Pre(otot)
    rap = Resolver(rul, cfg=cfg)
    chick = Automata(rap, (1, 1), beak)
    gra = numpyGrass(cfg, dtype="b")
    if init_data is not None and all(np.asarray(init_data).shape == cfg.cols):
        gra.data[:] = init_data
    for _ in range(cfg.runs):
        gra.graze_all(chick)
    # gra._set_center(0)
    return (gra, chick)


def test_resolver2(desired_range: int, ndim: int, init_data=None):
    cfg = Cfg()
    cfg.runs = 3
    cfg.cols = 1 + (desired_range * 2)  # +1 to pad with 0s
    cfg.ndim = ndim
    totrap = Resolver([0, 1, 1, 1, 0, 1, 1, 0, 1], insys=9)
    # [1, 0, 1, 0, 1, 1, 0, 1, 0],

    def otot(value, automata, _):
        inner = value[0]
        outer = [sum(value[1:])]
        post_outer = totrap.resolve_batch(outer)
        return [inner, post_outer], None

    # rul = [0, 0, 1, 0]
    # [0, 1, 0, 1]
    rul = [0, 1, 0, 1]
    beak = Pre(otot)
    rap = Resolver(rul, cfg=cfg)
    chick = Automata(rap, (1, 1), beak)
    gra = numpyGrass(cfg, dtype="b")
    if init_data is not None and set(np.asarray(init_data).shape) == set((cfg.cols,)):
        gra.data[:] = init_data
    for _ in range(cfg.runs):
        gra.graze_all(chick)
    # gra._set_center(0)
    return (gra, chick)


def test_resolver3(desired_range: int, ndim: int, init_data=None):
    cfg = Cfg()
    cfg.runs = 3
    cfg.cols = 1 + (desired_range * 2)  # +1 to pad with 0s
    cfg.ndim = ndim
    totrap = Resolver([1, 0, 1, 0, 1, 1, 0, 1, 0], insys=9)
    # [1, 0, 1, 0, 1, 1, 0, 1, 0],

    def otot(value, automata, _):
        inner = value[0]
        outer = [sum(value[1:])]
        post_outer = totrap.resolve_batch(outer)
        return [inner, post_outer], None

    # rul = [0, 0, 1, 0]
    # [0, 1, 0, 1]
    rul = [0, 0, 1, 0]
    beak = Pre(otot)
    rap = Resolver(rul, cfg=cfg)
    chick = Automata(rap, (1, 1), beak)
    gra = numpyGrass(cfg, dtype="b")
    if init_data is not None and set(np.asarray(init_data).shape) == set((cfg.cols,)):
        gra.data[:] = init_data
    for _ in range(cfg.runs):
        gra.graze_all(chick)
    # gra._set_center(0)
    return (gra, chick)


def test_resolver4(desired_range: int, ndim: int, init_data=None):
    cfg = Cfg()
    cfg.runs = 3
    cfg.cols = 1 + (desired_range * 2)  # +1 to pad with 0s
    cfg.ndim = ndim
    totrap = Resolver([1, 0, 1, 0, 1, 1, 0, 1, 0], insys=9)
    # [1, 0, 1, 0, 1, 1, 0, 1, 0],

    def otot(value, automata, _):
        inner = value[0]
        outer = [sum(value[1:])]
        post_outer = totrap.resolve_batch(outer)
        return [inner, post_outer], None

    # rul = [0, 0, 1, 0]
    # [0, 1, 0, 1]
    rul = [0, 0, 1, 0]
    beak = Pre(otot)
    rap = Resolver(rul, cfg=cfg)
    chick = Automata(rap, (1, 1), beak, wrap=0)
    gra = numpyGrass(cfg, dtype="b")
    if init_data is not None and set(np.asarray(init_data).shape) == set((cfg.cols,)):
        gra.data[:] = init_data
    for _ in range(cfg.runs):
        gra.graze_all(chick)
    # gra._set_center(0)
    return (gra, chick)


def test_conway_resolver(
    desired_range: int, ndim: int, init_data=None, random=False, wrap="wrap"
):
    cfg = Cfg()
    cfg.runs = 0
    cfg.cols = 1 + (desired_range * 2)  # +1 to pad with 0s
    cfg.ndim = ndim
    rule_id = [1, 0]
    conway = conway_preset()

    beak = Pre(conway)
    rap = Resolver(rule_id, cfg)
    chick = Automata(rap, (1, 1), beak=beak, wrap=wrap)

    gra = numpyGrass(cfg, dtype="b")
    # print(np.asarray(init_data).shape, cfg.cols)
    if init_data is not None and set(np.asarray(init_data).shape) == set((cfg.cols,)):
        gra.data[:] = init_data
    if random:
        gra._set_random(2)
        print("data", gra.data)
    for _ in range(cfg.runs):
        print(gra.data)
        gra.graze_all(chick, wrap=0)
    #   gra._set_center(0)
    return (gra, chick)
