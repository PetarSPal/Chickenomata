"""
Execution / display module
"""

import numpy as np
from scipy.interpolate import interp1d
import pygame

chars = tuple((*map(lambda x: x*2, "█ ▒▓░"), *"🟥🟦🟧🟨🟩🟪🟫"))


def unicode_print(data):

    if len(data.shape) > 1:
        pancake = (np.prod(data.shape[len(data.shape)//2:]),
                   (np.prod(data.shape[:len(data.shape)//2])))
        data = data.reshape(pancake)
        for row in data:
            print("".join([chars[el]*2 for el in row]))
    else:
        print("".join([chars[el]*2 for el in data]))


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


def pygame_draw(grass, screen, color, cell_size, running, hoffset, reorder=True):
    screen.fill((255, 255, 255))
    pancake = (np.prod(grass.data.shape[len(grass.data.shape)//2:]),
               (np.prod(grass.data.shape[:len(grass.data.shape)//2])))

    new_data = grass.data
    if reorder and grass.ndim > 2:
        for i in range(sum(divmod(grass.data.ndim-2, 2))):
            new_data = grass.data.swapaxes(-2-i, -3-i)
            new_data = new_data.reshape(pancake)
    if grass.ndim == 1:
        new_data = np.asarray(grass._hist_data + [grass.data]).T
    if grass.ndim == 2:
        new_data = np.asarray(grass.data)
    for index, x in np.ndenumerate(new_data):
        # TODO: Fix paralax rerendering
        if running and x > 0:
            pygame.draw.rect(
                screen,
                color[x-1],
                (hoffset + (index[0] * cell_size), index[1] * cell_size, cell_size, cell_size))
    # pygame.display.flip()
    screen.blit(screen, (0, 0))
    pygame.display.update()


def pygame_engine(flock, grass, cfg):
    pygame.init()
    speed = 60
    paused, running = False, True
    screen = pygame.display.set_mode((cfg.width, cfg.height))
    pygame.display.set_caption("Chickenomata")
    clock = pygame.time.Clock()

    cell_cols = cfg.cols**((grass.ndim+1)//2)
    print(cfg.cols, cfg.ndim)
    if cfg.ndim % 2:
        cell_size = cfg.width // cell_cols
    else:
        cell_size = cfg.height // cell_cols
    hoffset = (cfg.width - (cell_size * cell_cols)) // 2
    if cfg.ndim == 1 and not grass._history:
        grass._history = cfg.height//(cfg.width//cfg.cols)

    if cfg.in_sys == 2:
        color = [(0, 0, 0)]
    elif cfg.in_sys == 3:
        color = [(0, 0, 0), (128, 128, 128)]
    elif cfg.in_sys == 5:
        color = [(0, 0, 0), (64, 64, 64), (128, 128, 128), (192, 192, 192)]
    elif cfg.grayscale:
        colors = interp1d([0, cfg.in_sys-1], [1, 0])
        color = [[int(colors(x)*255)]*3 for x in range(1, cfg.in_sys)]
    else:
        colors = interp1d([0, cfg.in_sys-1], [1, 0])
        color = [((y >> 16) & 255, (y >> 8) & 255, y & 255)
                 for y in [int(colors(x)*16777215)
                           for x in range(1, cfg.in_sys)]]
    current_runs = cfg.runs
    while current_runs >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if not running:
            break
        if not paused:
            pygame_draw(grass, screen, color, cell_size, running, hoffset)
            grass.graze_all(flock)
            clock.tick(speed)
            current_runs -= 1
    pygame.quit()


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
#

#
# def pygame_1dengine(flock, grass, settings, width, height, cell_size, hoffset):
#     pygame.init()
#     # cell_size = 20
#     speed = 60
#     paused, running = False, True
#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption("Chickenomata")
#     clock = pygame.time.Clock()
#     colors = interp1d([1, 512], [5, 10])
#
#     def pygame_draw(data, old, running):
#         color = (0, 0, 0)
#         line = 0
#         screen.fill((255, 255, 255))
#         for odata in old + [data]:
#             for index, x in np.ndenumerate(odata):
#                 if running:
#                     if x:
#                         pygame.draw.rect(
#                             screen, color, (hoffset + (index[0] * cell_size), line * cell_size, cell_size, cell_size))
#             line += 1
#         # pygame.display.flip()
#         screen.blit(screen, (0, 0))
#         pygame.display.update()
#     current_runs = settings.runs
#     while current_runs >= 0:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     paused = not paused
#         #     if not paused:
#         if not running:
#             break
#         if not paused:
#             pygame_draw(grass.data, grass._hist_data, running)
#             grass.graze_all(flock)
#             clock.tick(speed)
#             current_runs -= 1
#     pygame.quit()
#
