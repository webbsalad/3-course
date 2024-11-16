import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Задача 5")

L = np.array([[50, 100],
              [250, 200],
              [50, 200],
              [250, 300]])

T = np.array([[1, 2], [3, 1]])
transformed_L = L @ T.T

def to_pygame_coords(point):
    return int(point[0]), 600 - int(point[1])

def slope(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0:
        return None
    return dy / dx

segment1 = L[0:2]
segment2 = L[2:4]
transformed_segment1 = transformed_L[0:2]
transformed_segment2 = transformed_L[2:4]

slope1 = slope(segment1[0], segment1[1])
slope2 = slope(segment2[0], segment2[1])
transformed_slope1 = slope(transformed_segment1[0], transformed_segment1[1])
transformed_slope2 = slope(transformed_segment2[0], transformed_segment2[1])

print("Начальные наклоны:", slope1, slope2)
print("Преобразованные наклоны:", transformed_slope1, transformed_slope2)

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (255, 0, 0), to_pygame_coords(segment1[0]), to_pygame_coords(segment1[1]), 2)
    pygame.draw.line(screen, (255, 0, 0), to_pygame_coords(segment2[0]), to_pygame_coords(segment2[1]), 2)
    pygame.draw.line(screen, (0, 0, 255), to_pygame_coords(transformed_segment1[0]), to_pygame_coords(transformed_segment1[1]), 2)
    pygame.draw.line(screen, (0, 0, 255), to_pygame_coords(transformed_segment2[0]), to_pygame_coords(transformed_segment2[1]), 2)
    pygame.display.flip()
