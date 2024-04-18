"""
Ad-hoc templates to prevent myself from testing too much in main
"""
import random
import numpy as np
from v1.grass import Square
from v1.wings import time_engine, test_engine, pygame_engine
from v1.raptor import Raptor
from v1.settings import Cfg
from v1.chicken import Flock, Chicken


def chicken_test(engine):

    cfg = Cfg()
    cfg.runs = 50
    cfg.cols = 15
    cfg.ndim = 1
    cfg.in_sys = 2

    # rule = [0,1,0,1,1,1,1,0]
    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    print(rule110)

    rap = Raptor(rule110, cfg.in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape)
    gra._set_random(2)

    engine(flock, gra, cfg)


def Rule110(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 250
    cfg.ndim = 1
    cfg.in_sys = 2

    # rule = [0,1,0,1,1,1,1,0]
    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    print(rule110)

    rap = Raptor(rule110, cfg.in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape)
    # gra._set_product(2, 3)

    engine(flock, gra, cfg)


def gray(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 250
    cfg.ndim = 1
    cfg.in_sys = 5
    cfg.grayscale = True

    # rule = [0, 0, 3, 3, 4, 1, 2, 3, 3, 0, 0, 4, 1, 3, 0, 2, 3, 2, 3, 2, 2, 2, 0, 4, 0, 0, 3, 2, 4, 0, 3, 3, 2, 0, 3, 4, 1, 4, 3, 0, 3, 3, 4, 3, 1, 1, 1, 0, 0, 0, 2, 3, 2, 2, 4, 2, 1, 4, 3, 2, 0, 4, 4, 2, 0, 4, 0, 3, 3, 1, 3, 0, 3, 2, 0, 1, 1, 0, 2, 3, 2, 3, 4, 0, 0, 2, 3, 1, 1, 4, 4, 3, 0, 1, 4, 4, 4, 0, 4, 0, 4, 2, 0, 2, 0, 3, 2, 2, 0, 2, 2, 2, 4, 0, 1, 2, 4, 2, 1, 1, 1, 0, 1, 0, 4]
    # rule = [4, 0, 0, 1, 1, 2, 1, 2, 1, 1, 3, 2, 4, 4, 4, 3, 1, 2, 3, 4, 1, 0, 2, 1, 4, 2, 4, 3, 2, 4, 2, 3, 4, 2, 0, 4, 1, 3, 1, 2, 2, 0, 3, 4, 3, 2, 0, 0, 4, 2, 2, 4, 0, 2, 4, 2, 0, 4, 0, 0, 1, 3, 3, 2, 3, 3, 4, 0, 1, 1, 4, 0, 3, 4, 3, 3, 4, 4, 0, 4, 4, 2, 0, 4, 1, 4, 3, 0, 1, 0, 2, 2, 3, 4, 2, 3, 4, 2, 3, 2, 2, 2, 1, 4, 3, 3, 4, 2, 2, 2, 0, 0, 0, 4, 4, 4, 2, 3, 0, 2, 2, 2, 4, 1, 0]
    # rule = [0, 4, 4, 1, 4, 3, 3, 1, 3, 4, 3, 4, 4, 1, 0, 4, 1, 1, 3, 1, 3, 3, 4, 0, 4, 3, 0, 1, 3, 4, 0, 3, 0, 3, 3, 1, 4, 3, 1, 2, 0, 4, 4, 2, 4, 2, 4, 1, 1, 4, 4, 0, 0, 4, 1, 3, 3, 4, 0, 0, 4, 4, 3, 2, 0, 2, 1, 3, 3, 2, 1, 1, 1, 3, 4, 4, 2, 4, 3, 1, 3, 2, 0, 1, 1, 3, 0, 3, 0, 0, 0, 2, 2, 3, 2, 2, 1, 4, 2, 1, 1, 1, 1, 2, 1, 1, 0, 0, 4, 4, 4, 0, 1, 0, 0, 2, 1, 2, 2, 1, 4, 4, 1, 0, 3]
    # rule = [0, 4, 3, 2, 4, 2, 3, 1, 0, 4, 3, 4, 3, 1, 2, 4, 0, 0, 3, 1, 3, 1, 4, 0, 4, 3, 0, 1, 3, 4, 0, 3, 0, 1, 2, 1, 4, 3, 1, 2, 0, 4, 4, 2, 3, 2, 0, 1, 1, 4, 2, 0, 0, 4, 1, 3, 3, 4, 0, 2, 4, 4, 3, 2, 0, 1, 1, 3, 2, 2, 1, 3, 1, 3, 4, 4, 2, 4, 3, 1, 3, 2, 0, 1, 4, 3, 0, 3, 0, 3, 0, 2, 2, 3, 2, 2, 1, 4, 2, 1, 1, 1, 1, 2, 1, 1, 0, 0, 4, 2, 4, 0, 1, 0, 0, 2, 1, 3, 2, 1, 4, 4, 1, 0, 3]
    # rule = [0, 3, 2, 2, 3, 2, 1, 0, 1, 4, 1, 3, 3, 4, 3, 4, 2, 2, 2, 4, 4, 4, 1, 0, 0, 0, 0, 0, 4, 1, 3, 3, 3, 3, 4, 2, 1, 3, 2, 2, 3, 0, 0, 2, 3, 0, 2, 1, 1, 4, 0, 1, 0, 4, 1, 4, 2, 0, 4, 2, 2, 4, 2, 4, 1, 0, 2, 0, 2, 1, 1, 0, 0, 0, 4, 3, 3, 1, 3, 0, 2, 1, 4, 3, 3, 4, 4, 3, 4, 2, 0, 1, 2, 2, 4, 1, 1, 1, 0, 1, 4, 2, 3, 1, 4, 0, 3, 3, 3, 2, 1, 4, 0, 0, 3, 3, 0, 2, 4, 1, 4, 1, 3, 1, 2]
    # ruke = [3, 0, 4, 2, 4, 3, 2, 4, 3, 4, 0, 1, 1, 2, 1, 4, 0, 0, 4, 0, 4, 2, 3, 1, 3, 2, 3, 1, 4, 0, 4, 0, 2, 4, 2, 1, 3, 4, 4, 4, 1, 3, 0, 3, 0, 2, 1, 1, 1, 0, 3, 0, 2, 3, 0, 3, 0, 3, 2, 2, 1, 3, 0, 1, 1, 1, 4, 1, 0, 4, 3, 4, 2, 2, 4, 2, 4, 1, 2, 2, 4, 2, 1, 3, 1, 0, 3, 1, 1, 2, 2, 1, 0, 4, 3, 0, 3, 2, 4, 0, 3, 3, 0, 4, 2, 2, 3, 1, 1, 0, 0, 4, 0, 4, 0, 2, 4, 0, 3, 3, 3, 1, 2, 2, 1]
    rule = [3, 0, 4, 2, 4, 3, 2, 4, 3, 4, 0, 1, 1, 2, 1, 4, 0, 0, 4, 0, 4, 2, 3, 1, 3, 2, 3, 1, 4, 0, 4, 0, 2, 4, 2, 1, 3, 4, 4, 4, 1, 3, 0, 3, 0, 2, 1, 1, 1, 0, 3, 0, 2, 3, 0, 3, 0, 3, 2, 2, 1,
            3, 0, 1, 1, 1, 4, 1, 0, 4, 3, 4, 2, 2, 4, 2, 4, 1, 2, 2, 4, 2, 1, 3, 1, 0, 3, 1, 1, 2, 2, 1, 0, 4, 3, 0, 3, 2, 4, 0, 3, 3, 0, 4, 2, 2, 3, 1, 1, 0, 0, 4, 0, 4, 0, 2, 4, 0, 3, 3, 3, 1, 2, 2, 1]
    # rand = [[random.randint(0,4) for _ in range(144)] for _ in range(5)]
    # print(len(rule))
    rap = Raptor(rule, cfg.in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape)
    print(gra.shape)
    gra._set_random(5)

    engine(flock, gra, cfg)


def colors(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 250
    cfg.ndim = 1
    cfg.in_sys = 12

# rand = [random.randint(0,10) for _ in range(121)]
    rand = [random.randint(0, 11) for _ in range(1728)]
    print(rand)
    # print(len(rule))
    rap = Raptor(rand, cfg.in_sys)
    print(rap.neighbor_count)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape)
    # gra._set_random(12)

    engine(flock, gra, cfg)


def discrete_conway(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 150
    cfg.ndim = 2
    cfg.in_sys = 2

    conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    conwayrule = [*conwayrule]
    conwayrule = list(map(int, conwayrule))
    rap = Raptor(conwayrule, cfg.in_sys)
    print(rap.neighbor_count, rap.in_system)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape)
    gra._set_random(2)

    engine(flock, gra, cfg)


def color_conway(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 150
    cfg.ndim = 2
    cfg.in_sys = 12

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0, 11) for _ in range(12)]
    print(rand)
    rap = Raptor(rand, cfg.in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape)
    print(gra.shape)
    gra._set_random(11)

    engine(flock, gra, cfg)


def test_high(engine):
    cfg = Cfg()
    cfg.runs = 300000
    cfg.cols = 100
    cfg.ndim = 1
    cfg.in_sys = 2048*2

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0, (2048*2)-1) for _ in range((2048*2)**2)]
    print(rand)
    rap = Raptor(rand, cfg.in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape)
    print(gra.shape)
    gra._set_center(1)

    engine(flock, gra, cfg)


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
    rap = Raptor(rand, cfg.in_sys)
    # print(rap.neighbor_count)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape, dtype='b')
    # print(gra.shape)
    gra._set_center(1)
    # gra._set_random(2)
    # print(gra.data)

    engine(flock, gra, cfg)


def test_pygame(engine):
    cfg = Cfg()
    cfg.runs = 1000
    cfg.cols = 100
    cfg.ndim = 1
    cfg.in_sys = 2

    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))

    rap = Raptor(rule110, cfg.in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    # maxl = height//(width//cfg.cols)
    gra = Square(cfg.shape)
    # gra._set_product(2, 3)

    engine(flock, gra, cfg)


def test_pygame_nd(engine):
    cfg = Cfg()
    cfg.runs = 3000
    cfg.cols = 150
    cfg.ndim = 2
    cfg.in_sys = 2

    conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    conwayrule = [*conwayrule]
    conwayrule = list(map(int, conwayrule))
    rap = Raptor(conwayrule, cfg.in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(cfg.shape)
    gra._set_random(2)

    engine(flock, gra, cfg)


def test_pygdim(engine):
    cfg = Cfg()
    cfg.runs = 10000
    cfg.cols = 10
    cfg.ndim = 3
    cfg.in_sys = 10

    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0, 9) for _ in range(10*10*10)]
    print(rand)
    rap = Raptor(rand, cfg.in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    gra = Square(cfg.shape, dtype='b')
    gra._set_center(1)
    # gra._set_random(2)
    gra = Square(cfg.shape)
    gra._set_random(2)

    engine(flock, gra, cfg)
