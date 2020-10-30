import pygame 
import math

# initialize
pygame.init()
pygame.font.init()
# sizes
window_width = 1000
window_height = 600
size_default = 5
# window
window = pygame.display.set_mode((window_width, window_height))
# colors
black = (0, 0, 0)
white = (255, 255, 255)
# set caption and icon
pygame.display.set_caption('Pong')
icon = pygame.image.load('pong.png')
pygame.display.set_icon(icon)
# scores
game_round = 0
score_left = 0
score_right = 0
scored_last = "left"
font = pygame.font.SysFont('Arial', 30, True, False)
# ball
ball_coordinates = (int(window_width / 2), int(window_height / 2))
ball_angel = (-1, 0)
speed = 0.5
ball_radius = 10
# bars
bar_indent = 50
bar_height = 100
bar_width = 15
bar_right = (window_width - bar_indent - bar_width, int((window_height - bar_height) / 2))
bar_left = (bar_indent, int((window_height - bar_height) / 2))
# game variables
running = True

def game_loop():
    while running:
        get_ball_angel()
        check_events()
        move_ball()
        draw()

def draw():
    window.fill(black)
    # drawing bars
    pygame.draw.rect(window, white, (bar_left[0], int(bar_left[1]), bar_width, bar_height))
    pygame.draw.rect(window, white, (bar_right[0], int(bar_right[1]), bar_width, bar_height))
    # draw ball
    pygame.draw.circle(window, white, ball_coordinates, ball_radius)
    pygame.display.update()

def move_ball():
    fill = "filled"

def get_ball_angel():
    fill = "filled"

def check_events():
    global running, bar_left, bar_right
    # checking for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # checking for movement
    keys = pygame.key.get_pressed()
    # left bar
    # up
    if keys[pygame.K_w]:
        if bar_left[1] >= speed:
            bar_left = (bar_indent, bar_left[1] - speed)
    # down
    if keys[pygame.K_s]:
        if bar_left[1] <= window_height - speed - bar_height:
            bar_left = (bar_indent, bar_left[1] + speed)
    # right bar
    # up
    if keys[pygame.K_UP]:
        if bar_right[1] >= speed:
            bar_right = (window_width - bar_indent - bar_width, bar_right[1] - speed)
    # down
    if keys[pygame.K_DOWN]:
        if bar_right[1] <= window_height - speed - bar_height:
            bar_right = (window_width - bar_indent - bar_width, bar_right[1] + speed)

game_loop()
pygame.font.quit()
pygame.quit()
exit()