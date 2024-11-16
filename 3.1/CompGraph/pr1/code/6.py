import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Задача 6")

L = np.array([[-0.5, 1.5],
              [3, -2],
              [-1, -1],
              [3, 5/3]])

L = L * 100

T = np.array([[1, 2],
              [1, -3]])

transformed_L = L @ T.T

shift = np.array([400, 300])
L_shifted = L + shift
transformed_L_shifted = transformed_L + shift

def to_pygame_coords(point):
    return int(point[0]), 600 - int(point[1])

segment1 = L_shifted[0:2]
segment2 = L_shifted[2:4]
transformed_segment1 = transformed_L_shifted[0:2]
transformed_segment2 = transformed_L_shifted[2:4]

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
