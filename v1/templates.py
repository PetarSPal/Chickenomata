"""
Ad-hoc templates
"""

import random
import numpy as np
from v1.grass import numpyGrass
from v1.resolver import Resolver
from v1.settings import Cfg
from v1.automata import Automata, Pre, Post
from v1.utils.prepost import (
    conway_test_preset,
    conway_test_preset2,
    blinker_preset,
    fit_nc,
    sum_treshold_tst,
    test_preset,
    test_preset2,
    test_preset3,
    test_preset4,
    sum_filt,
    ofit_nc,
    outer_sum_filt,
)


def automata_test(engine):
    cfg = Cfg()
    cfg.runs = 50
    cfg.cols = 15
    cfg.ndim = 1

    # rule = [0,1,0,1,1,1,1,0]
    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    print(rule110)

    rap = Resolver(rule110, cfg)
    chick = Automata(rap)

    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def Rule110(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 250
    cfg.ndim = 1

    # rule = [0,1,0,1,1,1,1,0]
    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    print(rule110)

    rap = Resolver(rule110, cfg)
    chick = Automata(rap)

    gra = numpyGrass(cfg)
    # gra._set_product(2, 3)

    engine(chick, gra, cfg)


def gray(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 250
    cfg.ndim = 1
    cfg.in_system = 5
    cfg.grayscale = True

    # rule = [0, 0, 3, 3, 4, 1, 2, 3, 3, 0, 0, 4, 1, 3, 0, 2, 3, 2, 3, 2, 2, 2, 0, 4, 0, 0, 3, 2, 4, 0, 3, 3, 2, 0, 3, 4, 1, 4, 3, 0, 3, 3, 4, 3, 1, 1, 1, 0, 0, 0, 2, 3, 2, 2, 4, 2, 1, 4, 3, 2, 0, 4, 4, 2, 0, 4, 0, 3, 3, 1, 3, 0, 3, 2, 0, 1, 1, 0, 2, 3, 2, 3, 4, 0, 0, 2, 3, 1, 1, 4, 4, 3, 0, 1, 4, 4, 4, 0, 4, 0, 4, 2, 0, 2, 0, 3, 2, 2, 0, 2, 2, 2, 4, 0, 1, 2, 4, 2, 1, 1, 1, 0, 1, 0, 4]
    # rule = [4, 0, 0, 1, 1, 2, 1, 2, 1, 1, 3, 2, 4, 4, 4, 3, 1, 2, 3, 4, 1, 0, 2, 1, 4, 2, 4, 3, 2, 4, 2, 3, 4, 2, 0, 4, 1, 3, 1, 2, 2, 0, 3, 4, 3, 2, 0, 0, 4, 2, 2, 4, 0, 2, 4, 2, 0, 4, 0, 0, 1, 3, 3, 2, 3, 3, 4, 0, 1, 1, 4, 0, 3, 4, 3, 3, 4, 4, 0, 4, 4, 2, 0, 4, 1, 4, 3, 0, 1, 0, 2, 2, 3, 4, 2, 3, 4, 2, 3, 2, 2, 2, 1, 4, 3, 3, 4, 2, 2, 2, 0, 0, 0, 4, 4, 4, 2, 3, 0, 2, 2, 2, 4, 1, 0]
    # rule = [0, 4, 4, 1, 4, 3, 3, 1, 3, 4, 3, 4, 4, 1, 0, 4, 1, 1, 3, 1, 3, 3, 4, 0, 4, 3, 0, 1, 3, 4, 0, 3, 0, 3, 3, 1, 4, 3, 1, 2, 0, 4, 4, 2, 4, 2, 4, 1, 1, 4, 4, 0, 0, 4, 1, 3, 3, 4, 0, 0, 4, 4, 3, 2, 0, 2, 1, 3, 3, 2, 1, 1, 1, 3, 4, 4, 2, 4, 3, 1, 3, 2, 0, 1, 1, 3, 0, 3, 0, 0, 0, 2, 2, 3, 2, 2, 1, 4, 2, 1, 1, 1, 1, 2, 1, 1, 0, 0, 4, 4, 4, 0, 1, 0, 0, 2, 1, 2, 2, 1, 4, 4, 1, 0, 3]
    # rule = [0, 4, 3, 2, 4, 2, 3, 1, 0, 4, 3, 4, 3, 1, 2, 4, 0, 0, 3, 1, 3, 1, 4, 0, 4, 3, 0, 1, 3, 4, 0, 3, 0, 1, 2, 1, 4, 3, 1, 2, 0, 4, 4, 2, 3, 2, 0, 1, 1, 4, 2, 0, 0, 4, 1, 3, 3, 4, 0, 2, 4, 4, 3, 2, 0, 1, 1, 3, 2, 2, 1, 3, 1, 3, 4, 4, 2, 4, 3, 1, 3, 2, 0, 1, 4, 3, 0, 3, 0, 3, 0, 2, 2, 3, 2, 2, 1, 4, 2, 1, 1, 1, 1, 2, 1, 1, 0, 0, 4, 2, 4, 0, 1, 0, 0, 2, 1, 3, 2, 1, 4, 4, 1, 0, 3]
    # rule = [0, 3, 2, 2, 3, 2, 1, 0, 1, 4, 1, 3, 3, 4, 3, 4, 2, 2, 2, 4, 4, 4, 1, 0, 0, 0, 0, 0, 4, 1, 3, 3, 3, 3, 4, 2, 1, 3, 2, 2, 3, 0, 0, 2, 3, 0, 2, 1, 1, 4, 0, 1, 0, 4, 1, 4, 2, 0, 4, 2, 2, 4, 2, 4, 1, 0, 2, 0, 2, 1, 1, 0, 0, 0, 4, 3, 3, 1, 3, 0, 2, 1, 4, 3, 3, 4, 4, 3, 4, 2, 0, 1, 2, 2, 4, 1, 1, 1, 0, 1, 4, 2, 3, 1, 4, 0, 3, 3, 3, 2, 1, 4, 0, 0, 3, 3, 0, 2, 4, 1, 4, 1, 3, 1, 2]
    # ruke = [3, 0, 4, 2, 4, 3, 2, 4, 3, 4, 0, 1, 1, 2, 1, 4, 0, 0, 4, 0, 4, 2, 3, 1, 3, 2, 3, 1, 4, 0, 4, 0, 2, 4, 2, 1, 3, 4, 4, 4, 1, 3, 0, 3, 0, 2, 1, 1, 1, 0, 3, 0, 2, 3, 0, 3, 0, 3, 2, 2, 1, 3, 0, 1, 1, 1, 4, 1, 0, 4, 3, 4, 2, 2, 4, 2, 4, 1, 2, 2, 4, 2, 1, 3, 1, 0, 3, 1, 1, 2, 2, 1, 0, 4, 3, 0, 3, 2, 4, 0, 3, 3, 0, 4, 2, 2, 3, 1, 1, 0, 0, 4, 0, 4, 0, 2, 4, 0, 3, 3, 3, 1, 2, 2, 1]
    rule = [
        3,
        0,
        4,
        2,
        4,
        3,
        2,
        4,
        3,
        4,
        0,
        1,
        1,
        2,
        1,
        4,
        0,
        0,
        4,
        0,
        4,
        2,
        3,
        1,
        3,
        2,
        3,
        1,
        4,
        0,
        4,
        0,
        2,
        4,
        2,
        1,
        3,
        4,
        4,
        4,
        1,
        3,
        0,
        3,
        0,
        2,
        1,
        1,
        1,
        0,
        3,
        0,
        2,
        3,
        0,
        3,
        0,
        3,
        2,
        2,
        1,
        3,
        0,
        1,
        1,
        1,
        4,
        1,
        0,
        4,
        3,
        4,
        2,
        2,
        4,
        2,
        4,
        1,
        2,
        2,
        4,
        2,
        1,
        3,
        1,
        0,
        3,
        1,
        1,
        2,
        2,
        1,
        0,
        4,
        3,
        0,
        3,
        2,
        4,
        0,
        3,
        3,
        0,
        4,
        2,
        2,
        3,
        1,
        1,
        0,
        0,
        4,
        0,
        4,
        0,
        2,
        4,
        0,
        3,
        3,
        3,
        1,
        2,
        2,
        1,
    ]
    # rand = [[random.randint(0,4) for _ in range(144)] for _ in range(5)]
    # print(len(rule))
    rap = Resolver(rule, cfg)
    chick = Automata(rap)

    gra = numpyGrass(cfg)
    print(gra.shape)
    gra._set_random(5)

    engine(chick, gra, cfg)


def colors(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 250
    cfg.ndim = 1
    cfg.in_system = 12

    # rand = [random.randint(0,10) for _ in range(121)]
    rand = [random.randint(0, 11) for _ in range(1728)]
    print(rand)
    # print(len(rule))
    rap = Resolver(rand, cfg)
    print(rap.neighbor_count)
    chick = Automata(rap)

    gra = numpyGrass(cfg)
    # gra._set_random(12)

    engine(chick, gra, cfg)


def discrete_conway(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 150
    cfg.ndim = 2

    conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    conwayrule = [*conwayrule]
    conwayrule = list(map(int, conwayrule))
    rap = Resolver(conwayrule, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap)

    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def color_conway(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 150
    cfg.ndim = 2
    cfg.in_system = 12

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0, 11) for _ in range(12)]
    print(rand)
    pre = Pre(fit_nc)
    rap = Resolver(rand, cfg)
    chick = Automata(rap, (1, 1), pre=pre)

    gra = numpyGrass(cfg)
    print(gra.shape)
    gra._set_random(11)

    engine(chick, gra, cfg)


def test_high(engine):
    cfg = Cfg()
    cfg.runs = 300000
    cfg.cols = 100
    cfg.ndim = 1
    cfg.in_system = 2048 * 2

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0, (2048 * 2) - 1) for _ in range((2048 * 2) ** 2)]
    print(rand)
    rap = Resolver(rand, cfg)
    chick = Automata(rap)

    gra = numpyGrass(cfg)
    print(gra.shape)
    gra._set_center(1)

    engine(chick, gra, cfg)


def test_dim(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 5
    cfg.ndim = 5

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0, 1) for _ in range(1024)]
    print(rand)
    pre = Pre(fit_nc)
    rap = Resolver(rand, cfg)
    # print(rap.neighbor_count)
    chick = Automata(rap, (1, 1), pre=pre)

    gra = numpyGrass(cfg, dtype="b")
    # print(gra.shape)
    gra._set_center(1)
    # gra._set_random(2)
    # print(gra.data)

    engine(chick, gra, cfg)


def test_pygame(engine):
    cfg = Cfg()
    cfg.runs = 1000
    cfg.cols = 100
    cfg.ndim = 1
    cfg.in_system = 2

    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))

    rap = Resolver(rule110, cfg)
    chick = Automata(rap)

    # maxl = height//(width//cfg.cols)
    gra = numpyGrass(cfg)
    # gra._set_product(2, 3)

    engine(chick, gra, cfg)


def test_pygame_nd(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 150
    cfg.ndim = 2
    cfg.in_system = 2

    conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    conwayrule = [*conwayrule]
    conwayrule = list(map(int, conwayrule))
    rap = Resolver(conwayrule, cfg)
    chick = Automata(rap)

    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def test_pygdim(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 10
    cfg.ndim = 4
    cfg.in_system = 10

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0, 9) for _ in range(10 * 10 * 10)]
    print(rand)
    rap = Resolver(rand, cfg)
    pre = Pre(fit_nc)
    chick = Automata(rap, (1, 1), pre=pre)
    gra = numpyGrass(cfg, dtype="b")
    gra._set_center(1)
    # gra._set_random(2)
    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def test_pygdimn(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 20
    cfg.ndim = 3
    cfg.in_system = 28

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    # rand = [random.randint(0, 1) for _ in range(2**9)]

    # [0, 1, 0, 0, 1, 1, 0, 0, 0, 0]

    # [0, 1, 1, 0, 0, 0, 1, 0, 0, 0]
    rand = [random.randint(0, 1) for _ in range(28)]
    print(rand)
    pre = Pre(sum_filt)
    post = Post()
    rap = Resolver(rand, cfg)
    chick = Automata(rap, (1, 1), pre, post)
    gra = numpyGrass(cfg, dtype="b")
    gra._set_center(1)
    # gra._set_random(2)
    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def test_pygdim3(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 20
    cfg.ndim = 2
    cfg.in_system = 10

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    # rand = [random.randint(0, 1) for _ in range(2**9)]

    # [0, 1, 0, 0, 1, 1, 0, 0, 0, 0]

    # [0, 1, 1, 0, 0, 0, 1, 0, 0, 0]
    rand = [random.randint(0, 1) for _ in range(10)]
    print(rand)
    pre = Pre(sum_filt)
    post = Post()
    rap = Resolver(rand, cfg)
    chick = Automata(rap, (1, 1), pre, post)
    gra = numpyGrass(cfg, dtype="b")
    gra._set_center(1)
    # gra._set_random(2)
    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def test_pygdim2(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 40
    cfg.ndim = 2
    cfg.in_system = 76

    # for sum_filt ->
    # "insys" = neighbors*(realinsys-1) + 1
    # aka  9 nei binary -> maxsum 9 -> rules for 0 to 9 inclusive -> 10 rules
    # 9 nei ternary -> maxsum 18 -> rules for 0 to 18 inclusive -> 19 rules
    # 9 nei quad -> maxsum 27 -> 28 rules

    # how to decouple insys from rule len
    # in elementary automata rule is nested and insys == rule len on any depth
    # in sum_filt rule is linear and rule len

    # separate resolver function for sum_filt processing?
    # when i define a resolver i give it a rule and insys
    # i would need to define the resolver differently or have a different resolver
    # can i convert a non-totalitic rule to sum_filt?
    # 0 sum_filt maps to rightmost non-sum_filt (0000..)
    # 1 sum_filt maps to leftmost non-sum_filt (1111...)
    # rest map to

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    # rand = [random.randint(0, 1) for _ in range(2**9)]

    # [0, 1, 0, 0, 1, 1, 0, 0, 0, 0]

    # [0, 1, 1, 0, 0, 0, 1, 0, 0, 0]
    rand = [random.randint(0, 3) for _ in range(76)]
    print(rand)
    pre = Pre(sum_filt)
    post = Post()
    rap = Resolver(rand, cfg)
    chick = Automata(rap, (2, 2), pre, post)
    gra = numpyGrass(cfg, dtype="b")
    gra._set_center(1)
    # gra._set_random(2)
    gra = numpyGrass(cfg)
    gra._set_random(4)

    engine(chick, gra, cfg)


def discrete_conwayvar(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 150
    cfg.ndim = 2
    cfg.in_system = 2

    conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"

    c1 = "0000000000000000000000000000000100000000000000000000000000000001"
    c2 = "0000000000000001000000010001011100000000000000010000000100010110"
    c3 = "0000000000000001000000010001011100000000000000010000000100010110"
    c4 = "0000000100010111000101110111111000000001000101100001011001101000"
    c5 = "0000000000000001000000010001011100000000000000010000000100010110"
    c6 = "0000000100010111000101110111111000000001000101100001011001101000"
    c7 = "0000000100010111000101110111111000000001000101100001011001101000"
    c8 = "0001011101111110011111101110100000010110011010000110100010000000"

    c1 = "0000000000000000000000000000000100000000000000000000000000000001"
    c2 = "0000000000000001000000010001011100000000000000010000000100010110"
    c3 = "0000000000000001000000010001011100000000000000010000000100010110"
    c4 = "0000000100010111000101110111111000000001000101100001011001101000"
    c5 = "0000000000000001000000010001011100000000000000010000000100010110"
    c6 = "0000000100010111000101110111111000000001000101100001011001101000"
    c7 = "0000000100010111000101110111111000000001000101100001011001101000"
    c8 = "0001011101111110011111101110100000010110011010000110100000010000"

    conwayrule = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8
    conwayrule = [*conwayrule]
    random.shuffle(conwayrule)
    conwayrule = [
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        0,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        1,
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
    ]
    conwayrule = list(map(int, conwayrule))
    print(conwayrule)
    rap = Resolver(conwayrule, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, (1, 1))

    gra = numpyGrass(cfg)
    #   gra._set_random(2)
    # gra._set_product(2, 9)

    engine(chick, gra, cfg)


def test_c0d(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 100
    cfg.ndim = 1
    cfg.in_system = 10

    rand = [random.randint(0, 9) for _ in range(10)]
    print(rand)

    rap = Resolver(rand, cfg)
    chick = Automata(rap, (0, 0))

    gra = numpyGrass(cfg)
    gra._set_random(10)

    engine(chick, gra, cfg)


def test_neigbor_rule(engine):
    cfg = Cfg()
    cfg.runs = 5
    cfg.cols = 11
    cfg.ndim = 2
    cfg.in_system = 10

    # rand = [random.randint(0, 0) for _ in range(2**9)]
    # rand = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    rand = [random.randint(0, 1) for _ in range(10)]
    rand = [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    # [1, 1, 0, 1, 0, 1, 1, 1, 1, 0]
    # [1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
    # [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    # [0, 1, 0, 1, 1, 1, 1, 0, 1, 0]
    #   [0, 0, 1, 0, 1, 0, 0, 1, 1, 0]
    # [0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    print(rand)
    pre = Pre(sum_filt)
    rap = Resolver(rand, cfg)
    chick = Automata(rap, (1, 1), pre)

    gra = numpyGrass(cfg)
    gra._set_center(1)
    print(gra.data)

    engine(chick, gra, cfg)


def test_pygdim2d(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 10
    cfg.ndim = 3
    cfg.in_system = 2

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0, 1) for _ in range(2**4)]
    print(rand)
    rap = Resolver(rand, cfg)
    pre = Pre(fit_nc)
    chick = Automata(rap, (1, 1), pre=pre)
    gra = numpyGrass(cfg, dtype="b")
    gra._set_center(1)
    # gra._set_random(2)
    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def test_neigbor_rule2(engine):
    cfg = Cfg()
    cfg.runs = 10
    cfg.cols = 21
    cfg.ndim = 2

    # rand = [random.randint(0, 0) for _ in range(2**9)]
    # rand = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    rand = [random.randint(0, 1) for _ in range(9)]
    # rand = [1, 1, 1, 1, 1, 1, 1, 1, 0]
    # [1, 1, 0, 1, 0, 1, 1, 1, 1, 0]
    # [1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
    # [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    # [0, 1, 0, 1, 1, 1, 1, 0, 1, 0]
    #   [0, 0, 1, 0, 1, 0, 0, 1, 1, 0]
    # [0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    print(rand)

    totrap = Resolver(rand, insys=9)

    def otot(value, automata, _):
        inner = value[0]
        outer = [sum(value[1:])]
        post_outer = totrap.claw_batch(outer)
        return [inner, post_outer], None

    # moore = [1,1,1,0] [1, 1, 1, 1, 1, 1, 1, 1, 0]
    # hole = [0, 0, 1, 0]
    rul = [random.randint(0, 1) for _ in range(4)]
    # 11 10 01 00
    # rul = [1, 1, 1, 0]
    print(rul)

    # rand = [0, 1, 0, 1, 1, 0, 0, 0, 1]
    # rul = [1, 0, 0, 1]
    pre = Pre(otot)
    rap = Resolver(rul, cfg)
    chick = Automata(rap, (1, 1), pre)

    gra = numpyGrass(cfg)
    gra._set_center(1)

    engine(chick, gra, cfg)


def test_neigbor_rule3(engine):
    cfg = Cfg()
    cfg.runs = 10
    cfg.cols = 21
    cfg.ndim = 2
    cfg.in_system = 3

    # rand = [random.randint(0, 0) for _ in range(2**9)]
    # rand = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    rand = [random.randint(0, 2) for _ in range(27)]
    # rand = [1, 1, 1, 1, 1, 1, 1, 1, 0]
    # [1, 1, 0, 1, 0, 1, 1, 1, 1, 0]
    # [1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
    # [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    # [0, 1, 0, 1, 1, 1, 1, 0, 1, 0]
    #   [0, 0, 1, 0, 1, 0, 0, 1, 1, 0]
    # [0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    print(rand)

    totrap = Resolver(rand, insys=27)

    def otot(value, automata, _):
        inner = value[0]
        outer = [sum(value[1:])]
        post_outer = totrap.claw_batch(outer)
        return [inner, post_outer], None

    # moore = [1,1,1,0]
    # hole = [0, 0, 1, 0]
    rul = [random.randint(0, 2) for _ in range(9)]
    # 11 10 01 00
    # rul = [1, 1, 1, 0]
    print(rul)

    # rand = [0, 1, 0, 1, 1, 0, 0, 0, 1]
    # rul = [1, 0, 0, 1]
    pre = Pre(otot)
    rap = Resolver(rul, cfg)
    chick = Automata(rap, (1, 1), pre)

    gra = numpyGrass(cfg)
    gra._set_center(1)

    engine(chick, gra, cfg)


def test_neigbor_rule4(engine):
    cfg = Cfg()
    cfg.runs = 6
    cfg.cols = 11
    cfg.ndim = 3
    cfg.in_system = 2

    # rand = [random.randint(0, 0) for _ in range(2**9)]
    # rand = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    rand = [random.randint(0, 1) for _ in range(27)]
    rand = [1 for _ in range(26)] + [0]
    print(rand)

    # 27 = max input value
    # 27 = every neighbor except center if max value
    # For moore R1 -> (3**dim)*(insys-1)
    #
    # def outer_sum_filt(rule):
    #     def otot(value, automata, ndim):
    #         # maxsum = (automata.resolver.neighbor_count-1)*(automata.resolver.in_system-1)
    #         maxsum = (3**ndim)*(automata.resolver.in_system-1)
    #         totrap = Resolver(rule, insys=maxsum)
    #         inner = value[0]
    #         outer = [sum(value[1:])]
    #         post_outer = totrap.claw_batch(outer)
    #         return [inner, post_outer], None
    #     return otot

    otot = outer_sum_filt(rand)

    # moore = [1,1,1,0]
    # hole = [0, 0, 1, 0]
    rul = [random.randint(0, 1) for _ in range(4)]
    rul = [1, 1, 1, 0]

    # 11 10 01 00
    # rul = [1, 1, 1, 0]
    print(rul)

    # rand = [0, 1, 0, 1, 1, 0, 0, 0, 1]
    # rul = [1, 0, 0, 1]
    pre = Pre(otot)
    rap = Resolver(rul, cfg=cfg)
    chick = Automata(rap, (1, 1), pre)

    gra = numpyGrass(cfg)
    gra._set_center(1)

    engine(chick, gra, cfg)


def test_neigbor_rule4(engine):
    from v1.utils.resolvers import moore_resolver

    ngra, nchick = moore_resolver((1, 0), 1, 4)
    print(ngra.data)


def test_neigbor_rule5(engine):
    from v1.utils.resolvers import test_resolver

    ngra, nchick = test_resolver(2, 2)
    print(ngra.data)
    for i in range(30):
        ngra.graze_all(nchick)
        ngra._set_center(0)
        print(ngra.data)


def test_neigbor_rule6(engine):
    from v1.utils.resolvers import test_conway_resolver

    tdata = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    t = test_conway_resolver(1, 2, tdata)
    print(t[0].data)


def adj_conway(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 150
    cfg.ndim = 2

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # rand = [random.randint(0, 1) for _ in range(9)]
    # rand2 = [random.randint(0, 1) for _ in range(2)]
    # rand = [0, 0, 0, 0, 0, 1, 1, 0, 0]
    # rand2 = [0, 0, 1, 0]
    rand2 = [1, 0]
    # print(rand, rand2)
    # otot = outer_sum_filt(rand)
    conway = conway_test_preset()
    # adj = [[0, 0, 1, 0, 0],
    #        [0, 1, 0, 1, 0],
    #        [1, 0, 0, 0, 1],
    #        [0, 1, 0, 1, 0],
    #        [0, 0, 1, 0, 0]]
    # adj = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    adj = [
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
    ]
    ngra = numpyGrass(cfg)
    ngra.data = np.asarray(adj)
    # conwayrule = list(map(int, conwayrule))
    pre = Pre(conway)
    rap = Resolver(rand2, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=ngra)

    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobilen_conway(engine):
    from v1.utils.resolvers import test_resolver

    ngra, nchick = test_resolver(3, 2)
    ngra.graze_all(nchick)
    ngra._set_center(0)
    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 50
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = conway_test_preset()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobilen2_conway(engine):
    from v1.utils.resolvers import test_resolver2

    ngra, nchick = test_resolver2(2, 2)
    ngra.graze_all(nchick)
    ngra._set_center(0)
    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 50
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = conway_test_preset()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg)
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobilen3_conway(engine):
    from v1.utils.resolvers import test_resolver2

    ngra, nchick = test_resolver2(2, 2)
    ngra.graze_all(nchick)
    ngra._set_center(0)
    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 150
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = conway_test_preset2()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobilen4_conway(engine):
    from v1.utils.resolvers import test_conway_resolver

    tdata = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    ngra, nchick = test_conway_resolver(1, 2, tdata, wrap=0)

    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 150
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = blinker_preset()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobilen5_conway(engine):
    from v1.utils.resolvers import test_conway_resolver

    init_data = [
        [1, 0, 1, 1, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ]
    ngra, nchick = test_conway_resolver(2, 2, init_data=init_data)
    # ngra, nchick = test_conway_resolver(2, 2, random=True)

    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 150
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = conway_test_preset2()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobile_neighbor_experiment_6(engine):
    from v1.utils.resolvers import test_conway_resolver

    init_data = [
        [1, 0, 1, 1, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ]
    ngra, nchick = test_conway_resolver(2, 2, init_data=init_data)
    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 150
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = test_preset()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobile_neighbor_experiment_7(engine):
    from v1.utils.resolvers import test_conway_resolver

    init_data = [
        [1, 0, 1, 1, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ]
    ngra, nchick = test_conway_resolver(2, 2, init_data=init_data)
    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 150
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = test_preset2()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobile_neighbor_experiment_8(engine):
    from v1.utils.resolvers import test_resolver3

    ngra, nchick = test_resolver3(2, 2)
    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 150
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = test_preset3()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobile_neighbor_experiment_9(engine):
    from v1.utils.resolvers import test_resolver4

    ngra, nchick = test_resolver4(2, 2)
    print(ngra.data)

    adj = ngra

    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 150
    cfg.ndim = 2
    rule_id = [1, 0]
    conway = test_preset4()
    pre = Pre(conway)
    rap = Resolver(rule_id, cfg)
    print(rap.neighbor_count, rap.in_system)
    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    gra._set_random(2)

    engine(chick, gra, cfg)


def mobile_neighbor_experiment_10(engine):
    ncfg = Cfg()
    ncfg.runs = 1
    ncfg.cols = 27
    adj = ngra = numpyGrass(ncfg, dtype="b")

    cfg = Cfg()
    cfg.runs = 100000
    cfg.cols = 150
    cfg.ndim = 1

    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))

    # pre = Pre(fit_nc)
    pre = Pre(sum_treshold_tst)

    rap = Resolver(rule110, cfg)

    nchick = Automata(rap, wrap="wrap")
    for i in range(ncfg.runs):
        adj.graze_all(nchick)
    # nchick.period = 1

    print(adj.data)

    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    # gra._set_product(ncfg.in_system, 3)
    # gra._set_random(2)

    engine(chick, gra, cfg)
    print(gra.data)
    print(adj.data)


def mobile_neighbor_experiment_11(engine):
    ncfg = Cfg()
    ncfg.runs = 3
    ncfg.cols = 9
    adj = ngra = numpyGrass(ncfg, dtype="b")

    cfg = Cfg()
    cfg.runs = 100000
    cfg.cols = 150
    cfg.ndim = 1

    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))

    # pre = Pre(fit_nc)
    pre = Pre(sum_treshold_tst)

    rap = Resolver(rule110, cfg)

    nchick = Automata(rap, wrap="wrap")
    for i in range(ncfg.runs):
        adj.graze_all(nchick)
    nchick.period = 5

    print(adj.data)

    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    # gra._set_product(ncfg.in_system, 3)
    # gra._set_random(2)

    engine(chick, gra, cfg)
    print(gra.data)
    print(adj.data)


def mobile_neighbor_experiment_12(engine):
    ncfg = Cfg()
    ncfg.runs = 3
    ncfg.cols = 9
    adj = ngra = numpyGrass(ncfg, dtype="b")

    cfg = Cfg()
    cfg.runs = 100000
    cfg.cols = 150
    cfg.ndim = 1
    cfg.in_system = 4

    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    #
    # mrule = "012012101001211020112012201"
    # mrule = [*mrule]
    # mrule = list(map(int, mrule))
    mrule = [random.randint(0, 3) for _ in range(64)]
    print(mrule)

    # [1, 1, 0, 1, 1, 2, 2, 1, 3, 0, 3, 3, 1, 1, 1, 1, 3, 1, 0, 0, 1, 3, 2, 3, 1, 2, 0, 3, 1, 1, 1, 1, 1, 0, 3, 3, 2, 1, 1, 0, 0, 3, 3, 2, 1, 3, 0, 2, 3, 3, 0, 1, 0, 3, 2, 2, 3, 2, 0, 0, 2, 2, 2, 1]

    # pre = Pre(fit_nc)
    pre = Pre(sum_treshold_tst)

    nrap = Resolver(rule110, ncfg)
    rap = Resolver(mrule, cfg)

    nchick = Automata(nrap, wrap="wrap")
    for i in range(ncfg.runs):
        adj.graze_all(nchick)
    # nchick.period = 5

    print(adj.data)

    chick = Automata(rap, pre=pre, adjacency=adj, adjacency_auto=nchick)

    gra = numpyGrass(cfg, dtype="b")
    # gra._set_product(ncfg.in_system, 3)
    # gra._set_random(2)

    engine(chick, gra, cfg)
    print(gra.data)
    print(adj.data)
    print(mrule)
