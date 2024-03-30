from Raptor.Raptor import Raptor
# from Grass.Grass import Grass
import Logic.data

import numpy as np

rule = [0,1,1,0,1,0,1,0]
rap = Raptor(rule,2,1)
print(rap.neighbor_count)
print(rap.io([0,1,1]))
# gra = Grass(100,1)
# gra.set_center(1)
# print(gra.data)
# gra.mutate_all(rap)


data = np.zeros(tuple(7 for _ in range(1)))

Logic.data.set_center(1, data)
print(data)

Logic.data.mutate_all_moore(rap, data, 1, rap.neighbor_count, True)
# Logic.data.mutate_all_moore(rap, data, 2, rap.neighbor_count, True)