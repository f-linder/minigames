import pygame
import os

# initialize pygame
pygame.init()
# set dimensions
window = pygame.display.set_mode((800, 800))
# set caption and icon
pygame.display.set_caption("Snake")
icon = pygame.image.load(os.path.dirname(snake.py))
pygame.display.set_icon(icon)

running = True

# game loop
while running:

    # checking for input
    for event in pygame.event().get():
        # X pressed
        if event == pygame.QUIT:
            running = False


    # update whats shown
    pygame.display.update()
