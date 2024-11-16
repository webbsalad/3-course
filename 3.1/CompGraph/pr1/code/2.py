import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Primitives")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    pygame.draw.circle(screen, GREEN, (300, 300), 50) 
    pygame.draw.line(screen, BLUE, (100, 100), (500, 100), 5) 
    pygame.draw.rect(screen, RED, (200, 200, 100, 50))  

    pygame.display.flip()

pygame.quit()
