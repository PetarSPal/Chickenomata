"""
Execution / display module   
"""

import numpy as np

chars = tuple((*map(lambda x: x*2, "█ ▒▓░"), *"🟥🟦🟧🟨🟩🟪🟫"))
        
def unicode_print(data):
    i = 0
    for el in data.flat:
        print(chars[el]*2, end="")
        if i == data.shape[0]-1:
            print()
        i = (i+1) % data.shape[0]
        
def num_print(data):
    print(data)

def time_engine(flock, grass, settings):
    for _ in range(settings.runs):
        unicode_print(grass.data)
        grass.graze_all(flock)
        
def test_engine(flock, grass, settings):
    for _ in range(settings.runs):
        num_print(grass.data)
        grass.graze_all(flock)

# def __legacy_poc_to_reimplement_hybrid(raptors, grass, settings, oned=True):
#     for _ in range(settings.runs):
#         print_engine(grass.data, raptors[0].in_system)
#         grass._mutate_all_moore_raptors(raptors, settings.runs)
        
# def __legacy_test_rand_factory(ca, settings,step=1):
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

def pygame_engine(flock, grass, settings):
    import pygame
    pygame.init()
    width=80
    height=40
    cell_size=20
    speed=10
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("Chickenomata")
    paused = False
    clock = pygame.time.Clock()
    running = True
        
    def pygame_draw(data):
        screen.fill((255, 255, 255))
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, (0, 0, 0), (x * cell_size, y * cell_size, cell_size, cell_size))
        pygame.display.flip()
    
    for _ in range(settings.runs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            if not paused:
                pygame_draw(grass.data)
                grass.graze_all(flock)
                clock.tick(speed)        
    pygame.quit()

