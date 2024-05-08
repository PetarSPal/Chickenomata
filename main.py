from v1.engines import moderngl_engine, pygame_engine, console_engine
import random
import numpy as np
from v1.grass import numpyGrass
from v1.resolver import Resolver
from v1.settings import Cfg
from v1.automata import Automata, Pre, Post
from v1.utils.prepost import (
    conway_test_preset,
    sum_treshold_tst,
    test_preset4,
    outer_sum_filt,
)
from v1.utils.resolvers import test_resolver4

pyg = pygame_engine
tig = console_engine
mgl = moderngl_engine
engine = mgl

if __name__ == "__main__":
    run_sequence = []
    cfg = Cfg()
    cfg.runs = 150
    cfg.cols = 150
    cfg.ndim = 1

    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))

    res = Resolver(rule110, cfg)
    chick = Automata(res)

    gra = numpyGrass(cfg, dtype="b")
    gra._set_random(2)
    gra._history = 149

    cfg2 = Cfg()
    cfg2.runs = 10
    cfg2.cols = 150
    cfg2.ndim = 2

    conway = conway_test_preset()
    pre = Pre(conway)

    adj2 = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    ngra2 = numpyGrass(cfg, dtype="b")
    ngra2.data = np.asarray(adj2)

    rap2 = Resolver([1, 0], cfg2)
    chick2 = Automata(rap2, pre=pre, adjacency=ngra2)
    #
    gra2 = numpyGrass(cfg2, dtype="b")

    def get_gra2():
        # gra2 = numpyGrass(cfg2)
        new_data = np.asarray(gra._hist_data + [gra.data]).T

        gra2.data[:, : gra._history + 1] = new_data
        return gra2

    cfg3 = Cfg()
    cfg3.runs = 10
    cfg3.cols = 150
    cfg3.ndim = 2

    adj3 = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ]
    ngra3 = numpyGrass(cfg, dtype="b")
    ngra3.data = np.asarray(adj3)

    rap3 = Resolver([1, 0], cfg3)
    chick3 = Automata(rap3, pre=pre, adjacency=ngra3)

    gra3 = numpyGrass(cfg3, dtype="b")

    def get_gra3():
        gra3.data[:] = gra2.data
        return gra3

    n4cfg = Cfg()
    n4cfg.runs = 3
    n4cfg.cols = 9
    adj4 = ngra = numpyGrass(n4cfg, dtype="b")

    cfg4 = Cfg()
    cfg4.runs = 150
    cfg4.cols = 150
    cfg4.ndim = 1
    cfg4.in_system = 2

    rule110 = "01101110"
    rule110 = [*rule110]
    rule110 = list(map(int, rule110))
    # mrule = [random.randint(0, 1) for _ in range(8)]
    rule4 = [0, 0, 1, 0, 1, 1, 1, 0]

    pre4 = Pre(sum_treshold_tst)

    n4rap = Resolver(rule110, n4cfg)
    rap4 = Resolver(rule4, cfg4)

    n4chick = Automata(n4rap, wrap="wrap")
    for i in range(n4cfg.runs):
        adj4.graze_all(n4chick)
    # nchick.period = 5

    # print(adj.data)

    chick4 = Automata(rap4, pre=pre4, adjacency=adj4, adjacency_auto=n4chick)

    gra4 = numpyGrass(cfg4, dtype="b")
    gra4._history = 149

    def get_gra4():
        gra4.data[:] = gra3.data[0]
        return gra4

    n5gra, n5chick = test_resolver4(2, 2)

    adj5 = n5gra

    cfg5 = Cfg()
    cfg5.runs = 100
    cfg5.cols = 150
    cfg5.ndim = 2
    rule_id = [1, 0]
    conway5 = test_preset4()
    pre5 = Pre(conway5)
    rap5 = Resolver(rule_id, cfg5)
    chick5 = Automata(rap5, pre=pre5, adjacency=adj5, adjacency_auto=n5chick)

    gra5 = numpyGrass(cfg5, dtype="b")
    gra5._history = 10

    def get_gra5():
        new_data = np.asarray(gra4._hist_data + [gra4.data]).T

        gra5.data[:, : gra4._history + 1] = new_data
        return gra5

    # cfg6 = Cfg()
    # cfg6.runs = 150
    # cfg6.cols = 30
    # cfg6.ndim = 3
    # cfg6.in_system = 2
    #
    # rand6 = [1, 0, 1, 0]
    # print(rand6)
    #
    # otot6 = outer_sum_filt(rand6)
    #
    # rul6 = [1, 1, 1, 0]
    #
    # pre6 = Pre(otot6)
    # rap6 = Resolver(rul6, cfg=cfg6)
    # chick6 = Automata(rap6, (1, 1), pre6)
    #
    # gra6 = numpyGrass(cfg6, dtype="b")
    #
    # def get_gra6():
    #     # gra6.data = np.insert(gra6.data, 1, gra5.data, axis=0)
    #     gra6.data[:] = gra5.data.flatten()[: gra6.data.size].reshape(gra6.data.shape)
    #     return gra6

    run_sequence.append([chick2, get_gra2, cfg2])
    run_sequence.append([chick3, get_gra3, cfg3])
    run_sequence.append([chick4, get_gra4, cfg4])
    run_sequence.append([chick5, get_gra5, cfg5])
    # run_sequence.append([chick6, get_gra6, cfg6])

    engine(chick, gra, cfg, rest=run_sequence)
