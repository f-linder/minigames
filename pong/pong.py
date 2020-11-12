import pygame 
import math
import random

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
speed = 5
ball_x_speed = 0
ball_y_speed = 0
ball_radius = 10
# bars
bar_indent = 50
bar_height = 100
bar_width = 15
bar_right = (window_width - bar_indent - bar_width, int((window_height - bar_height) / 2))
bar_left = (bar_indent, int((window_height - bar_height) / 2))
# game variables
running = True
new_round = True
# clock
clock = pygame.time.Clock()

def game_loop():
    while running:
        clock.tick(60)
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
    pygame.draw.circle(window, white, (int(ball_coordinates[0]), int(ball_coordinates[1])), ball_radius)
    pygame.display.update()

def get_plus_or_minus():
    if random.randint(0, 2) >= 1:
        return -1
    else:
        return 1

def move_ball():
    global ball_coordinates, new_round, ball_x_speed, ball_y_speed, score_left, score_right, scored_last
    # neue runde -> ball in Richtung des Gewinners des letzten Punkts und repositionieren in Mitte
    if new_round:
        #
        # TO IMPLEMENT
        # ANGEL WITH X AND Y
        #

        ball_coordinates = (int(window_width / 2), int(window_height / 2))
        new_round = False
    else: 
        # links raus -> rechts gewinnt Runde
        if ball_coordinates[0] - ball_radius <= 0:
            new_round = True
            scored_last = "right"
            score_right += 1
        # rechts raus -> links gewinnt Runde
        elif ball_coordinates[0] + ball_radius >= window_width:
            new_round = True
            scored_last = "left"
            score_left += 1
        # normal
        else:
            ball_coordinates = (ball_coordinates[0] + math.cos(ball_angel[0]) * speed, ball_coordinates[1] + math.sin(ball_angel[1]) * speed)


def get_ball_angel():
    fill = "filler"

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