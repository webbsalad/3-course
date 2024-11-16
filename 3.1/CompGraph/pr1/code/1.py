import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Transformation")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

point = np.array([50, 100])

T = np.array([[1, 3], [4, 1]])

transformed_point = np.dot(T, point)

def draw_point(surface, point, color, radius=5):
    pygame.draw.circle(surface, color, (int(point[0]), int(point[1])), radius)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)

    draw_point(screen, point, RED)
    draw_point(screen, transformed_point, BLUE)

    pygame.display.flip()

pygame.quit()
