import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Segment Transformation")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

segment = np.array([[50, 100], [200, 300]])

T = np.array([[1, 3], [4, 1]])

transformed_segment = np.dot(segment, T.T)

def draw_line(surface, segment, color, width=2):
    pygame.draw.line(surface, color, tuple(segment[0]), tuple(segment[1]), width)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    draw_line(screen, segment, GREEN)
    draw_line(screen, transformed_segment, BLUE)

    pygame.display.flip()

pygame.quit()
