"""
Display module
"""

import numpy as np
from scipy.interpolate import interp1d
import pygame
import moderngl
import moderngl_window
from moderngl_window import geometry
from pathlib import Path
from pyrr import Matrix44

import moderngl_window as mglw
from moderngl_window.scene.camera import KeyboardCamera


def pygame_engine(flock, grass, cfg):
    # INIT
    pygame.init()
    speed = 60
    paused, running = False, True
    screen = pygame.display.set_mode((cfg.width, cfg.height))
    pygame.display.set_caption("Chickenomata")
    clock = pygame.time.Clock()
    # Determine cell size, attempt to determine offset
    cell_cols = cfg.cols ** ((grass.ndim + 1) // 2)
    if cfg.ndim % 2:
        cell_size = cfg.width // cell_cols
    else:
        cell_size = cfg.height // cell_cols
    hoffset = (cfg.width - (cell_size * cell_cols)) // 2
    # Histogram for 0D, 1D
    if cfg.ndim == 1 and not grass._history:
        grass._history = cfg.height // (cfg.width // cfg.cols)
    if cell_size == cfg.width:
        cell_size = cfg.height // 5
        grass._history = 5
    color = __pygame_colors(cfg)
    # Main loop
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
            __pygame_draw(grass, screen, color, cell_size, running, hoffset)
            grass.graze_all(flock)
            clock.tick(speed)
            current_runs -= 1
    pygame.quit()


def __pygame_colors(cfg):
    # Ad-hoc color interpolation
    if cfg.in_system == 2:
        color = [(0, 0, 0)]
    elif cfg.in_system == 3:
        color = [(0, 0, 0), (128, 128, 128)]
    elif cfg.in_system == 5:
        color = [(0, 0, 0), (64, 64, 64), (128, 128, 128), (192, 192, 192)]
    elif cfg.grayscale:
        colors = interp1d([0, cfg.in_system - 1], [1, 0])
        color = [[int(colors(x) * 255)] * 3 for x in range(1, cfg.in_system)]
    else:
        colors = interp1d([0, cfg.in_system - 1], [1, 0])
        color = [
            ((y >> 16) & 255, (y >> 8) & 255, y & 255)
            for y in [int(colors(x) * 16777215) for x in range(1, cfg.in_system)]
        ]
    return color


def __pygame_draw(grass, screen, color, cell_size, running, hoffset, reorder=False):
    screen.fill((255, 255, 255))
    # Historgram for 1D, pancake for 3D+
    if grass.ndim == 1:
        new_data = np.asarray(grass._hist_data + [grass.data]).T
    elif grass.ndim == 2:
        new_data = np.asarray(grass.data)
    else:  # if grass.ndim > 2:
        pancake = (
            np.prod(grass.data.shape[len(grass.data.shape) // 2 :]),
            (np.prod(grass.data.shape[: len(grass.data.shape) // 2])),
        )
        new_data = np.asarray(grass.data).reshape(pancake)
        # Arbitrary reorder
        if reorder:
            for i in range(sum(divmod(new_data.ndim - 2, 2))):
                new_data = new_data.swapaxes(-2 - i, -3 - i)

    # Main drawing loop
    for index, x in np.ndenumerate(new_data):
        if running and x > 0:
            pygame.draw.rect(
                screen,
                color[x - 1],
                (
                    hoffset + (index[0] * cell_size),
                    index[1] * cell_size,
                    cell_size,
                    cell_size,
                ),
            )
    # pygame.display.flip()
    screen.blit(screen, (0, 0))
    pygame.display.update()


def console_engine(flock, grass, settings):
    chars = tuple((*map(lambda x: x * 2, "█ ▒▓░"), *"🟥🟦🟧🟨🟩🟪🟫"))
    for _ in range(settings.runs):
        __unicode_print(grass.data, chars)
        grass.graze_all(flock)


def test_engine(flock, grass, settings):
    for _ in range(settings.runs):
        print(grass.data)
        grass.graze_all(flock)


def __unicode_print(data, chars):
    if len(data.shape) > 1:
        pancake = (
            np.prod(data.shape[len(data.shape) // 2 :]),
            (np.prod(data.shape[: len(data.shape) // 2])),
        )
        data = data.reshape(pancake)
        for row in data:
            print("".join([chars[el] * 2 for el in row]))
    else:
        print("".join([chars[el] * 2 for el in data]))


def moderngl_engine(automata, grass, cfg, rest=[]):
    pygame.init()

    class MGLgame(mglw.WindowConfig):
        resource_dir = (Path(__file__) / "../shaders").absolute()

        def data_reinit(self, automata, grass, cfg):
            self.runs = cfg.runs
            self.automata = automata
            self.grass = grass
            self.cfg = cfg
            self.wnd.size = (self.cfg.width, self.cfg.height)
            self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

            # Determine cell size, attempt to determine offset
            self.cell_cols = self.cfg.cols ** ((self.grass.ndim + 1) // 2)
            if self.cfg.ndim % 2:
                self.cell_size = self.cfg.width // self.cell_cols
            else:
                self.cell_size = self.cfg.height // self.cell_cols
            self.hoffset = (cfg.width - (self.cell_size * self.cell_cols)) // 2
            # Histogram for 0D, 1D
            if self.cfg.ndim == 1 and not self.grass._history:
                self.grass._history = self.cfg.height // (
                    self.cfg.width // self.cfg.cols
                )
            if self.cell_size == self.cfg.width:
                self.cell_size = self.cfg.height // 5
                self.grass._history = 5

            # self.ctx.clear(1.0, 1.0, 1.0)

        def data_init(self, automata, grass, cfg):
            self.runs = cfg.runs
            self.automata = automata
            self.grass = grass
            self.cfg = cfg
            self.wnd.title = "Chickenomata"
            self.wnd.size = (self.cfg.width, self.cfg.height)
            # self.camera.projection.update(aspect_ratio=16/9)
            self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

            # Determine cell size, attempt to determine offset
            self.cell_cols = self.cfg.cols ** ((self.grass.ndim + 1) // 2)
            if self.cfg.ndim % 2:
                self.cell_size = self.cfg.width // self.cell_cols
            else:
                self.cell_size = self.cfg.height // self.cell_cols
            self.hoffset = (cfg.width - (self.cell_size * self.cell_cols)) // 2
            # Histogram for 0D, 1D
            if self.cfg.ndim == 1 and not self.grass._history:
                self.grass._history = self.cfg.height // (
                    self.cfg.width // self.cfg.cols
                )
            if self.cell_size == self.cfg.width:
                self.cell_size = self.cfg.height // 5
                self.grass._history = 5

            if self.wnd.name != "pygame2":
                raise RuntimeError(
                    "This example only works with --window pygame2 option"
                )
            self.wnd.mouse_exclusivity = True
            self.camera.projection.update(fov=90, aspect_ratio=None, near=1, far=1000)
            self.camera.set_rotation(yaw=-90, pitch=0)
            self.camera.set_position(75, -75, 80)
            self.cube = geometry.cube(size=(1, 1, 1))
            self.prog = self.load_program("cube.glsl")
            self.fps = 30
            self.ctx.clear(1.0, 1.0, 1.0)

            reversed_id_mat = np.array(
                [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
            ).astype("f4")

            self.prog["m_model"].write(reversed_id_mat)
            self.time = 0
            reserved = grass.data.size * 48
            # 48 for 3d else 32?
            reserved = reserved * grass._history if grass._history else reserved
            self.instance_data = self.ctx.buffer(reserve=reserved, dynamic=True)
            vertices, self.instances = self.obtain_vertices(self.obtain_data())
            self.cube.buffer(self.instance_data, "3u/i", ["in_offset"])
            self.instance_data.write(vertices.astype("u4"))
            self.cube.render(self.prog, instances=self.instances)
            self.instance_data.clear()

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.camera = KeyboardCamera(
                self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio
            )
            self.camera_enabled = True
            self.data_init(automata, grass, cfg)

        def key_event(self, key, action, modifiers):
            keys = self.wnd.keys

            if self.camera_enabled:
                self.camera.key_input(key, action, modifiers)

            if action == keys.ACTION_PRESS:
                if key == keys.C:
                    self.camera_enabled = not self.camera_enabled
                    self.wnd.mouse_exclusivity = self.camera_enabled
                    self.wnd.cursor = not self.camera_enabled
                if key == keys.SPACE:
                    self.timer.toggle_pause()

        def mouse_position_event(self, x: int, y: int, dx, dy):
            if self.camera_enabled:
                self.camera.rot_state(-dx, -dy)

        def resize(self, width: int, height: int):
            self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

        def obtain_data(self):
            if self.grass.ndim == 1 or self.grass._history:
                new_data = np.asarray(self.grass._hist_data + [self.grass.data]).T
            elif self.grass.ndim <= 3:
                new_data = np.asarray(self.grass.data)
            else:  # if grass.ndim > 2:
                pndim = self.grass.ndim // 3
                pancake = (
                    np.prod(self.grass.data.shape[pndim * 2 :]),
                    np.prod(self.grass.data.shape[pndim : pndim * 2]),
                    np.prod(self.grass.data.shape[:pndim]),
                )
                new_data = np.asarray(self.grass.data).reshape(pancake)
            return new_data

        def obtain_vertices(self, data):
            if self.grass.ndim == 1 or (
                self.grass.ndim == 2 and not self.grass._history
            ):
                x, y = np.where(data != 0)
                instances = len(x)
                z = np.zeros(instances)
            else:
                x, y, z = np.where(data != 0)
                instances = len(x)
            vertices = np.dstack([x, y, z])
            return vertices, instances

        def render(self, time, frametime):
            self.ctx.clear(1.0, 1.0, 1.0)
            self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)
            self.prog["m_proj"].write(self.camera.projection.matrix)
            self.prog["m_camera"].write(self.camera.matrix)
            self.prog["time"].value = time
            if 1 / self.fps < (time - self.time):
                vertices, self.instances = self.obtain_vertices(self.obtain_data())
                self.instance_data.write(vertices.astype("u4"))
                # self.cube.render(self.prog, instances=self.instances)
                # self.instance_data.clear()
                # if self.time == 0:
                #     self.time = time
                self.time = time

                if self.runs <= 0 and rest:
                    # self.instance_data.release()
                    automata, grass, cfg = rest.pop(0)
                    grass = grass()
                    self.automata = automata
                    self.grass = grass
                    self.cfg = cfg
                    self.runs = self.cfg.runs
                    # self.data_reinit(automata, grass, cfg)

                if self.runs > 0:
                    self.runs -= 1
                    self.grass.graze_all(self.automata)

            self.cube.render(self.prog, instances=self.instances)

    moderngl_window.run_window_config(MGLgame, args=("--window", "pygame2"))
