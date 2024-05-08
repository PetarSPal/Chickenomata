from itertools import product

# center = 1, rest of neighbors <2 -> 0
# center = 1, rest 2-3 -> 1
# center = 1, rest >3 -> 0
# center = 0, rest = 3 -> 1

#
# if neighbors == 3 or (center == 1 and neighbors == 2):
#     center = 1
# else:
#     center = 0
#

x = list(product(range(2), repeat=9))
y = product("01", repeat=9)

rule = ''
for i, v in enumerate(y):
    center = x[i][3]
    rest = sum(x[i][:3]) + sum(x[i][4:])
    print("".join(v), end=" -> ")
    if center == 1 and (rest < 2 or rest > 3):
        out = 0
    elif center == 1:
        out = 1
    elif rest == 3:
        out = 1
    else:
        out = 0
    print(out)
    rule += str(out)
print("Conway's Game of Life As Discrete Automata -> Wolfram Code:")
print(rule[::-1])

# Conway's Game of Life As Discrete Automata -> Wolfram Code:
# 00000000000000000000000000000001000000000000000000000000000000010000000000000001000000010001011100000000000000010000000100010110000000000000000100000001000101110000000000000001000000010001011000000001000101110001011101111110000000010001011000010110011010000000000000000001000000010001011100000000000000010000000100010110000000010001011100010111011111100000000100010110000101100110100000000001000101110001011101111110000000010001011000010110011010000001011101111110011111101110100000010110011010000110100010000000
