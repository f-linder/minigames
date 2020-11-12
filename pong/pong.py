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
score_height = 100
# window
window = pygame.display.set_mode((window_width, window_height + score_height))
font = pygame.font.SysFont('Arial', 50, True, False)
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
hit_last = "left"
font = pygame.font.SysFont('Arial', 50, True, False)
# ball
ball_coordinates = (int(window_width / 2), int(window_height / 2))
speed = 7
ball_radius = 10
ball_direction_rad = 0
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
        clock.tick(45)
        detect_ball_colision()
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
    # draw lines
    pygame.draw.line(window, white, (0, window_height), (window_width, window_height), 5)
    pygame.draw.line(window, white, (int(window_width / 2), 0), (int(window_width / 2), window_height + score_height), 5)
    # font
    score_surface = font.render(str(score_left), False, white)
    window.blit(score_surface, (int(window_width * 0.25), int((window_height + score_height * 0.25))))
    score_surface = font.render(str(score_right), False, white)
    window.blit(score_surface, (int(window_width * 0.75), int((window_height + score_height * 0.25))))

    pygame.display.update()

def move_ball():
    global ball_coordinates, new_round, score_left, score_right, scored_last, ball_direction_rad, hit_last
    # neue runde -> ball in Richtung des Gewinners des letzten Punkts und repositionieren in Mitte
    if new_round:
        # ball fliegt am beginn nach links
        if scored_last == "right":
            hit_last = "left"
            ball_direction_rad = 0# random.uniform(math.pi * -0.33, math.pi * 0.33)
        # ball fliegt am beginn nach rechts
        elif scored_last == "left":
            hit_last = "right"
            ball_direction_rad =math.pi# random.uniform(math.pi * 0.66, math.pi * 1.33)
        else:
            print("ERROR")

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
            ball_coordinates = (ball_coordinates[0] + math.cos(ball_direction_rad) * speed, ball_coordinates[1] + math.sin(ball_direction_rad) * speed)


def detect_ball_colision():
    global ball_direction_rad, hit_last
    # top or bottom hit
    if ball_coordinates[1] - ball_radius <= 0 or ball_coordinates[1] + ball_radius >= window_height:
        ball_direction_rad = -ball_direction_rad
    # right bar hit
    elif hit_last == "left" and math.ceil(ball_coordinates[0] + ball_radius) <= window_width - bar_indent - bar_width and math.ceil(ball_coordinates[0] + ball_radius) >= window_width - bar_indent - bar_width - 5 and math.ceil(ball_coordinates[1]) >= bar_right[1] and math.ceil(ball_coordinates[1]) <= bar_right[1] + bar_height:
        if get_pressed("right", "up"):
            ball_direction_rad = math.pi - ball_direction_rad + 0.2
        elif get_pressed("right", "down"):
            ball_direction_rad = math.pi - ball_direction_rad - 0.2
        else: 
            ball_direction_rad = math.pi - ball_direction_rad
        hit_last = "right"
    # left bar hit
    elif hit_last == "right" and math.ceil(ball_coordinates[0] - ball_radius) >= bar_indent + bar_width and math.ceil(ball_coordinates[0] - ball_radius) <= bar_indent + bar_width + 5 and math.ceil(ball_coordinates[1]) >= bar_left[1] and math.ceil(ball_coordinates[1]) <= bar_left[1] + bar_height:
        if get_pressed("left", "up"):
            ball_direction_rad = math.pi - ball_direction_rad - 0.2
        elif get_pressed("left", "down"):
            ball_direction_rad = math.pi - ball_direction_rad + 0.2
        else: 
            ball_direction_rad = math.pi - ball_direction_rad
        hit_last = "left"

def get_pressed(leftright, updown):
    keys = pygame.key.get_pressed()

    if leftright == "right" and updown == "up" and keys[pygame.K_UP]:
        return True
    elif leftright == "right" and updown == "down" and keys[pygame.K_DOWN]:
        return True
    elif leftright == "left" and updown == "up" and keys[pygame.K_w]:
        return True
    elif leftright == "left" and updown == "down" and keys[pygame.K_s]:
        return True

    return False

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