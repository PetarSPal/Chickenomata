from v1.engines import pygame_engine, console_engine, moderngl_engine
from v1.templates import (
    adj_conway,
    discrete_conway,
    Rule110,
    colors,
    gray,
    color_conway,
    # chicken_test,
    mobile_neighbor_experiment_10,
    mobile_neighbor_experiment_11,
    mobile_neighbor_experiment_12,
    # mobile_neighbor_experiment_13,
    mobile_neighbor_experiment_6,
    mobile_neighbor_experiment_7,
    mobile_neighbor_experiment_8,
    mobile_neighbor_experiment_9,
    mobilen2_conway,
    mobilen3_conway,
    mobilen4_conway,
    mobilen5_conway,
    mobilen_conway,
    test_high,
    test_dim,
    test_neigbor_rule2,
    test_neigbor_rule3,
    test_neigbor_rule4,
    test_neigbor_rule5,
    test_neigbor_rule6,
    test_pygame,
    test_pygame_nd,
    test_pygdim,
    test_pygdim2,
    discrete_conwayvar,
    test_c0d,
    test_neigbor_rule,
    test_pygdim2d,
    test_pygdim3,
    test_pygdimn,
)
from pstats import SortKey, Stats
from cProfile import Profile

pyg = pygame_engine
tig = console_engine
mgl = moderngl_engine
eng = mgl

if __name__ == "__main__":
    # chicken_test(eng)
    # Rule110(eng)
    # gray(eng)
    # colors(eng)
    # discrete_conway(eng)
    # color_conway(eng)
    # test_high(eng)
    # test_dim(eng)
    # test_pygame(eng)
    # test_pygame_nd(eng)
    # test_pygdim(eng)
    # test_pygdimn(eng)
    # test_pygdim2(eng)
    # discrete_conwayvar(eng)
    # test_c0d(eng)
    # test_neigbor_rule(tig) #Bug?
    # test_pygdim3(eng)
    # test_pygdim2d(eng)
    # test_neigbor_rule2(eng) ##BUg
    # test_neigbor_rule3(eng) #BUG
    # test_neigbor_rule4(tig)
    # test_neigbor_rule5(tig)
    # test_neigbor_rule6(tig)
    # adj_conway(eng)
    # mobilen_conway(eng)
    # mobilen2_conway(eng)
    # mobilen3_conway(eng)
    # mobilen4_conway(eng)
    # mobilen5_conway(eng)
    # mobile_neighbor_experiment_6(eng)
    # mobile_neighbor_experiment_7(eng)
    # mobile_neighbor_experiment_8(eng)
    mobile_neighbor_experiment_9(eng)
    # mobile_neighbor_experiment_10(eng)
    # mobile_neighbor_experiment_11(eng)
    # mobile_neighbor_experiment_12(eng)
    # mobile_neighbor_experiment_13(eng)

    # from v1.raptor import Raptor
    # rule = [0,1,0,1,1,1,1,0]
    # a = Raptor(rule, 2)
    # print(a.neighbor_count)
    # print(a.io([1,1,1]))
    # print(a.io([1,1,1]))

    # with Profile() as profile:
    #     adj_conway(pyg)
    #     (
    #         Stats(profile)
    #         .strip_dirs()
    #         .sort_stats(SortKey.CALLS)
    #         .print_stats()
    #     )
