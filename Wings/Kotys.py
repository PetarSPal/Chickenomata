
def print_chars(row, in_system, oned):
    chars = {}
    chars[5] = ["█", "▓", "▒", "░", " "]
    chars[4] = chars[5][:2] + chars[5][3:]
    chars[3] = [chars[5][0], chars[5][2], chars[5][-1]]
    chars[2] = [chars[5][0], chars[5][-1]]
    act_chars = chars[in_system]
    if oned:
        print("".join([act_chars[c]*2 for c in row])) 
    else:
        #2d, fix nd later
        for c in row:
            print("".join([act_chars[z]*2 for z in c])) 

def Bendis(raptor, grass, settings, oned=True):
    for _ in range(settings.rows):
        print_chars(grass.data, raptor.in_system, oned)
        grass.mutate_all_moore(raptor)
        
# def rand_factory(ca, settings,step=1):
#     row = set_initial_condition(settings.cols, settings.initial_condition)
#     f = open("randrules.txt", "a")
#     f.write("==BEGIN==")
#     f.write(str(ca.rule))
#     f.write("==END==")
#     f.close()
#     for _ in range(settings.rows):
#         print_chars(row)
#         row = ca.process_row(row, settings)
#         if _ % step == 0:
#             rules = [random.randrange(0, 255) for i in range(len(ca.rule))]
#             ca.rule=rules
#             f = open("randrules.txt", "a")
#             f.write("==BEGIN==")
#             f.write(str(ca.dec_rule))
#             f.write("==END==")
#             f.close()