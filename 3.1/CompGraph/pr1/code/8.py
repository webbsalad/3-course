import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Задача 8")

L = np.array([[8, 1],
              [7, 3],
              [6, 2]])

L = L * 50
shift = np.array([200, 100])
L_shifted = L + shift

T = np.array([[0, 1],
              [1, 0]])

transformed_L = L @ T.T
transformed_L_shifted = transformed_L + shift

def to_pygame_coords(point):
    return int(point[0]), 600 - int(point[1])

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255, 255, 255))
    pygame.draw.polygon(screen, (255, 0, 0), [to_pygame_coords(p) for p in L_shifted])
    pygame.draw.polygon(screen, (0, 0, 255), [to_pygame_coords(p) for p in transformed_L_shifted])
    pygame.display.flip()
