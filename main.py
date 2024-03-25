from Raptor.Raptor import Raptor
from Grass.Grass import Grass

rule = [0,1,1,0,1,0,1,0]
rap = Raptor(rule,2)
# print(rap.neighbor_count)
print(rap.io([0,0,0]))
gra = Grass(100,1)
gra.set_center(1)
print(gra.data)
gra.mutate_all(rap)
    