import pygame
import numpy as np
import math

class ReferenceFrame:
    def __init__(self, origin_x, origin_y, unit_x, unit_y):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.unit_x = unit_x
        self.unit_y = unit_y

class Drawer:
    def __init__(self, res_x, res_y, color_depth, rf):
        self.res_x = res_x
        self.res_y = res_y
        self.color_depth = color_depth
        self.rf = rf
        self.__color = (255, 255, 255)

    def initialize(self, caption):
        pygame.init()
        self.screen = pygame.display.set_mode((self.res_x, self.res_y))
        pygame.display.set_caption(caption)
        self.font = pygame.font.SysFont(None, 24)

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    def get_x(self, x):
        return int(self.rf.origin_x + x * self.rf.unit_x)

    def get_y(self, y):
        return int(self.rf.origin_y - y * self.rf.unit_y)

    def draw_polygon(self, points, width):
        pygame.draw.polygon(self.screen, self.__color,
                            [(self.get_x(x), self.get_y(y)) for x, y, _ in points], width)

    def draw_axes(self, x_min, x_max, y_min, y_max):
        old_color = self.__color
        self.__color = (0, 0, 0)
        pygame.draw.line(self.screen, self.__color,
                         (self.get_x(x_min), self.get_y(0)),
                         (self.get_x(x_max), self.get_y(0)), 1)
        pygame.draw.line(self.screen, self.__color,
                         (self.get_x(0), self.get_y(y_min)),
                         (self.get_x(0), self.get_y(y_max)), 1)
        self.__color = old_color

def translate(dx, dy):
    return np.array([
        [1, 0, 0],
        [0, 1, 0],
        [dx, dy, 1]
    ])

def scale(sx, sy):
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])

def rotate(angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return np.array([
        [cos_a, sin_a, 0],
        [-sin_a, cos_a, 0],
        [0, 0, 1]
    ])

rf = ReferenceFrame(400, 300, 50, 50)
drawer = Drawer(800, 600, 32, rf)
drawer.initialize("Задача 11")

L = np.array([
    [2, -2, 1],
    [-2, -2, 1],
    [-2, 2, 1],
    [2, 2, 1]
])

xc, yc = 0, 0
angle = math.pi / 32
m = 0.9
iterations = 20

drawer.color = (255, 255, 255)
drawer.draw_axes(-10, 10, -10, 10)

for i in range(iterations):
    T = translate(-xc, -yc) @ scale(m, m) @ rotate(angle) @ translate(xc, yc)
    L = L @ T
    drawer.color = (255 - i*12, 0, i*12)
    drawer.draw_polygon(L, 1)
    pygame.display.flip()
    pygame.time.wait(100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
