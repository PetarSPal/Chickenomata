"""
Ad-hoc templates to prevent myself from testing too much in main
"""
import random
from v1.grass import Square
from v1.wings import time_engine, test_engine, pygame_engine
from v1.raptor import Raptor
from v1.settings import Grass_cfg, Engine_cfg
from v1.chicken import Flock, Chicken
    

def chicken_test():

    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 50
    gcfg.cols = 15
    gcfg.ndims = 1
    in_sys = 2
    
    # rule = [0,1,0,1,1,1,1,0]
    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    print(rule110)
    
    rap = Raptor(rule110, in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    
    gra = Square(gcfg.shape)
    gra._set_random(2)

    time_engine(flock, gra, ecfg)
    
    

def Rule110():
    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 10000
    gcfg.cols = 300
    gcfg.ndims = 1
    in_sys = 2
    
    # rule = [0,1,0,1,1,1,1,0]
    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    print(rule110)
    
    rap = Raptor(rule110, in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    
    gra = Square(gcfg.shape)
    # gra._set_product(2, 3)

    time_engine(flock, gra, ecfg)


def gray():
    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 3000
    gcfg.cols = 300
    gcfg.ndims = 1
    in_sys = 5
    
    # rule = [0, 0, 3, 3, 4, 1, 2, 3, 3, 0, 0, 4, 1, 3, 0, 2, 3, 2, 3, 2, 2, 2, 0, 4, 0, 0, 3, 2, 4, 0, 3, 3, 2, 0, 3, 4, 1, 4, 3, 0, 3, 3, 4, 3, 1, 1, 1, 0, 0, 0, 2, 3, 2, 2, 4, 2, 1, 4, 3, 2, 0, 4, 4, 2, 0, 4, 0, 3, 3, 1, 3, 0, 3, 2, 0, 1, 1, 0, 2, 3, 2, 3, 4, 0, 0, 2, 3, 1, 1, 4, 4, 3, 0, 1, 4, 4, 4, 0, 4, 0, 4, 2, 0, 2, 0, 3, 2, 2, 0, 2, 2, 2, 4, 0, 1, 2, 4, 2, 1, 1, 1, 0, 1, 0, 4]
    # rule = [4, 0, 0, 1, 1, 2, 1, 2, 1, 1, 3, 2, 4, 4, 4, 3, 1, 2, 3, 4, 1, 0, 2, 1, 4, 2, 4, 3, 2, 4, 2, 3, 4, 2, 0, 4, 1, 3, 1, 2, 2, 0, 3, 4, 3, 2, 0, 0, 4, 2, 2, 4, 0, 2, 4, 2, 0, 4, 0, 0, 1, 3, 3, 2, 3, 3, 4, 0, 1, 1, 4, 0, 3, 4, 3, 3, 4, 4, 0, 4, 4, 2, 0, 4, 1, 4, 3, 0, 1, 0, 2, 2, 3, 4, 2, 3, 4, 2, 3, 2, 2, 2, 1, 4, 3, 3, 4, 2, 2, 2, 0, 0, 0, 4, 4, 4, 2, 3, 0, 2, 2, 2, 4, 1, 0]
    # rule = [0, 4, 4, 1, 4, 3, 3, 1, 3, 4, 3, 4, 4, 1, 0, 4, 1, 1, 3, 1, 3, 3, 4, 0, 4, 3, 0, 1, 3, 4, 0, 3, 0, 3, 3, 1, 4, 3, 1, 2, 0, 4, 4, 2, 4, 2, 4, 1, 1, 4, 4, 0, 0, 4, 1, 3, 3, 4, 0, 0, 4, 4, 3, 2, 0, 2, 1, 3, 3, 2, 1, 1, 1, 3, 4, 4, 2, 4, 3, 1, 3, 2, 0, 1, 1, 3, 0, 3, 0, 0, 0, 2, 2, 3, 2, 2, 1, 4, 2, 1, 1, 1, 1, 2, 1, 1, 0, 0, 4, 4, 4, 0, 1, 0, 0, 2, 1, 2, 2, 1, 4, 4, 1, 0, 3]
    # rule = [0, 4, 3, 2, 4, 2, 3, 1, 0, 4, 3, 4, 3, 1, 2, 4, 0, 0, 3, 1, 3, 1, 4, 0, 4, 3, 0, 1, 3, 4, 0, 3, 0, 1, 2, 1, 4, 3, 1, 2, 0, 4, 4, 2, 3, 2, 0, 1, 1, 4, 2, 0, 0, 4, 1, 3, 3, 4, 0, 2, 4, 4, 3, 2, 0, 1, 1, 3, 2, 2, 1, 3, 1, 3, 4, 4, 2, 4, 3, 1, 3, 2, 0, 1, 4, 3, 0, 3, 0, 3, 0, 2, 2, 3, 2, 2, 1, 4, 2, 1, 1, 1, 1, 2, 1, 1, 0, 0, 4, 2, 4, 0, 1, 0, 0, 2, 1, 3, 2, 1, 4, 4, 1, 0, 3]
    # rule = [0, 3, 2, 2, 3, 2, 1, 0, 1, 4, 1, 3, 3, 4, 3, 4, 2, 2, 2, 4, 4, 4, 1, 0, 0, 0, 0, 0, 4, 1, 3, 3, 3, 3, 4, 2, 1, 3, 2, 2, 3, 0, 0, 2, 3, 0, 2, 1, 1, 4, 0, 1, 0, 4, 1, 4, 2, 0, 4, 2, 2, 4, 2, 4, 1, 0, 2, 0, 2, 1, 1, 0, 0, 0, 4, 3, 3, 1, 3, 0, 2, 1, 4, 3, 3, 4, 4, 3, 4, 2, 0, 1, 2, 2, 4, 1, 1, 1, 0, 1, 4, 2, 3, 1, 4, 0, 3, 3, 3, 2, 1, 4, 0, 0, 3, 3, 0, 2, 4, 1, 4, 1, 3, 1, 2]
    # ruke = [3, 0, 4, 2, 4, 3, 2, 4, 3, 4, 0, 1, 1, 2, 1, 4, 0, 0, 4, 0, 4, 2, 3, 1, 3, 2, 3, 1, 4, 0, 4, 0, 2, 4, 2, 1, 3, 4, 4, 4, 1, 3, 0, 3, 0, 2, 1, 1, 1, 0, 3, 0, 2, 3, 0, 3, 0, 3, 2, 2, 1, 3, 0, 1, 1, 1, 4, 1, 0, 4, 3, 4, 2, 2, 4, 2, 4, 1, 2, 2, 4, 2, 1, 3, 1, 0, 3, 1, 1, 2, 2, 1, 0, 4, 3, 0, 3, 2, 4, 0, 3, 3, 0, 4, 2, 2, 3, 1, 1, 0, 0, 4, 0, 4, 0, 2, 4, 0, 3, 3, 3, 1, 2, 2, 1]
    rule = [3, 0, 4, 2, 4, 3, 2, 4, 3, 4, 0, 1, 1, 2, 1, 4, 0, 0, 4, 0, 4, 2, 3, 1, 3, 2, 3, 1, 4, 0, 4, 0, 2, 4, 2, 1, 3, 4, 4, 4, 1, 3, 0, 3, 0, 2, 1, 1, 1, 0, 3, 0, 2, 3, 0, 3, 0, 3, 2, 2, 1, 3, 0, 1, 1, 1, 4, 1, 0, 4, 3, 4, 2, 2, 4, 2, 4, 1, 2, 2, 4, 2, 1, 3, 1, 0, 3, 1, 1, 2, 2, 1, 0, 4, 3, 0, 3, 2, 4, 0, 3, 3, 0, 4, 2, 2, 3, 1, 1, 0, 0, 4, 0, 4, 0, 2, 4, 0, 3, 3, 3, 1, 2, 2, 1]
    # rand = [[random.randint(0,4) for _ in range(144)] for _ in range(5)]
    # print(len(rule))
    rap = Raptor(rule,in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    
    gra = Square(gcfg.shape)
    print(gra.shape)
    gra._set_random(5)

    time_engine(flock, gra, ecfg)
    
def colors():

    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 3000
    gcfg.cols = 300
    gcfg.ndims = 1
    in_sys = 12

# rand = [random.randint(0,10) for _ in range(121)]
    rand = [random.randint(0,11) for _ in range(1728)]
    # print(len(rule))
    rap = Raptor(rand,in_sys)
    print(rap.neighbor_count)
    chick = Chicken(rap)
    flock = Flock([chick], None)

    gra = Square(gcfg.shape)
    # gra._set_random(12)

    time_engine(flock, gra, ecfg)
    

def discrete_conway():

    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 3000
    gcfg.cols = 150
    gcfg.ndims = 2
    in_sys = 2
    
    conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    conwayrule = [*conwayrule]
    conwayrule = list(map(int, conwayrule))
    rap = Raptor(conwayrule,in_sys)
    print(rap.neighbor_count, rap.in_system)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    
    gra = Square(gcfg.shape)
    gra._set_random(2)

    # Bendis(rap, gra, ecfg, False)    
    time_engine(flock, gra, ecfg)
    
def color_conway():

    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 3000
    gcfg.cols = 150
    gcfg.ndims = 2
    in_sys = 12
    
    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0,11) for _ in range(12)]
    rap = Raptor(rand,in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    
    
    gra = Square(gcfg.shape)
    print(gra.shape)
    gra._set_random(11)

    time_engine(flock, gra, ecfg)
    
    

def test_high():

    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 300000
    gcfg.cols = 100
    gcfg.ndims = 1
    in_sys = 2048*2
    
    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0,(2048*2)-1) for _ in range((2048*2)**2)]
    rap = Raptor(rand,in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    
    
    gra = Square(gcfg.shape)
    print(gra.shape)
    gra._set_center(1)

    test_engine(flock, gra, ecfg)
    
    


def test_dim():

    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 10000
    gcfg.cols = 5
    gcfg.ndims = 5
    in_sys = 2
    
    # conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
    # conwayrule = [*conwayrule]
    # conwayrule = list(map(int, conwayrule))
    rand = [random.randint(0,1) for _ in range(1024)]
    # print(rand)
    rap = Raptor(rand,in_sys)
    # print(rap.neighbor_count)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    
    import numpy as np
    gra = Square(gcfg.shape, dtype='b')
    # print(gra.shape)
    gra._set_center(1)
    # gra._set_random(2)
    # print(gra.data)

    time_engine(flock, gra, ecfg)
    
    
def test_pygame():
    gcfg, ecfg = Grass_cfg(), Engine_cfg()
    ecfg.runs = 10000
    gcfg.cols = 300
    gcfg.ndims = 1
    in_sys = 2
    
    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    
    rap = Raptor(rule110, in_sys)
    chick = Chicken(rap)
    flock = Flock([chick], None)
    
    gra = Square(gcfg.shape)
    # gra._set_product(2, 3)

    pygame_engine(flock, gra, ecfg)