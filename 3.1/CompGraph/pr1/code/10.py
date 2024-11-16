import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Задача 10")

a = 50
b = 100
theta = 0

points = []
while theta <= 4 * math.pi:
    r = b + 2 * a * math.cos(theta)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    points.append((400 + x, 300 - y))
    theta += 0.01

screen.fill((255, 255, 255))
pygame.draw.lines(screen, (0, 0, 0), False, points, 2)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
