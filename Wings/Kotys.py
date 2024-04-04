chars = {}
chars[5] = ["█", "▓", "▒", "░", " "]
chars[4] = chars[5][:2] + chars[5][3:]
chars[3] = [chars[5][0], chars[5][2], chars[5][-1]]
chars[2] = [chars[5][0], chars[5][-1]]

def print_oned_chars(row, in_system):
    act_chars = chars[in_system]
    print("".join([act_chars[c]*4 for c in row])) 
            
def print_twod_chars(row, in_system):
    #2d, fix nd later
    act_chars = chars[in_system]
    for c in row:
        print("".join([act_chars[z]*4 for z in c])) 

def Bendis(raptor, grass, settings, oned=True):
    print_chars = print_oned_chars if oned else print_twod_chars
    for _ in range(settings.rows):
        # print(_)
        print_chars(grass.data, raptor.in_system)
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