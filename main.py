from Raptor.Raptor import Raptor
from Grass.Grass import Grass
from Wings.Kotys import Bendis
from Wings.Bendis import Settings

# in_sys=2
# in_sys=3
# in_sys=5
# rule = [0,1,1,0,1,1,1,0]
# rule = [0,1,1,1,0,1,1,0]
# rule = [0,1,1,2,0,1,1,0,2]

# rule = [0,2,1,2,0,1,2,0,0]
# rule = [0,1,1,2,2,1,4,0,2,0,1,4,3,2,1,3,1,0,2,1,1,0,4,2,1][::-1]


setting = Settings()
# setting.cols = 53
setting.cols = 300
setting.rows = 1000
in_sys = 2


rule = [0,1,1,0,1,1,1,0]
# rule = [0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1]
# rule = [0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,1,0,1,1,1,0]
rap = Raptor(rule,in_sys)
print(rap.neighbor_count)
oned = setting.cols
gra = Grass(oned)
gra._set_center(1)
# gra._set_random(2)
# gra._set_product(in_sys, rap.neighbor_count)
Bendis(rap, gra, setting)

# conwayrule = "00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000"
# conwayrule = [*conwayrule]
# conwayrule = list(map(int, conwayrule))
# # conwayrule = conwayrule*512
# # print(len(conwayrule))
# rap = Raptor(conwayrule,in_sys)
# # print(rap.neighbor_count)
# twod = [setting.cols, setting.cols]
# gra = Grass(twod)
# # gra._set_center(1)
# gra._set_random(2)
# # gra._set_product(in_sys, rap.neighbor_count)
# Bendis(rap, gra, setting, False)

# print(gra.data.ndim)











# print(rap.neighbor_count)
# print(rap.io([0,1,0]))
# gra = Grass(100,1)
# gra.set_center(1)
# print(gra.data)
# gra.mutate_all(rap)


# for i in range(100):
#     gra.mutate_all_moore(rap)
#     print(gra.data)

# data = np.zeros(tuple(35 for _ in range(1)), dtype=int)
# Logic.data.set_center(1, data)
# print(data)

# for i in range(100):
#     data = Logic.data.mutate_all_moore(rap, data, 1, rap.neighbor_count, True)
#     print(data)
# # Logic.data.mutate_all_moore(rap, data, 2, rap.neighbor_count, True)