import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Задача 4")

segment = np.array([[0, 100], [200, 300]])
T = np.array([[1, 2], [3, 1]])
transformed_segment = segment @ T.T

def to_pygame_coords(point):
    return int(point[0]), 600 - int(point[1])

def midpoint(p1, p2):
    return (p1 + p2) / 2

mid_orig = midpoint(segment[0], segment[1])
mid_trans = midpoint(transformed_segment[0], transformed_segment[1])

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (255, 0, 0), to_pygame_coords(segment[0]), to_pygame_coords(segment[1]), 2)
    pygame.draw.line(screen, (0, 0, 255), to_pygame_coords(transformed_segment[0]), to_pygame_coords(transformed_segment[1]), 2)
    pygame.draw.circle(screen, (255, 0, 0), to_pygame_coords(mid_orig), 5)
    pygame.draw.circle(screen, (0, 0, 255), to_pygame_coords(mid_trans), 5)
    pygame.draw.line(screen, (0, 255, 0), to_pygame_coords(mid_orig), to_pygame_coords(mid_trans), 1)
    pygame.display.flip()
