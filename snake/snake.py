import pygame
import pygame.freetype
import random
import math

# initialize pygame
pygame.init()
pygame.font.init()
# sizes
size_window = 700
size_default = 20
# columns, rows
columns = rows = int(size_window / size_default) 
print(f"columns: {columns}, rows: {rows}")
# set dimensions
window = pygame.display.set_mode((size_window, size_window))
# set caption and icon
pygame.display.set_caption('Snake')
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)
# colors
color_background = (255, 255, 205)
color_food = (255, 112, 77)
color_snake_body = (102, 255, 102)
color_snake_head = (26, 255, 26)
# boolean var for game loop
running = True
# list for snake
snake = []
# set head in the middle of the screen
snake.append((size_window - math.floor(columns / 2 - 2) * size_default, size_window - int(columns / 2) * size_default))
# food + timer
food = []
missing_food = 0 
ate = False
# direction of motion
motion = (1, 0)
# score
score = 0
font = pygame.font.SysFont('Arial', 30, True, True)


def game_loop():
    while running:
        pygame.time.delay(100)
        check_events()
        spawn_food()
        move()
        eating_food()
        draw()
    
def check_events():
    global running, motion
    for event in pygame.event.get():
        # checking for quit
        if event.type == pygame.QUIT:
            running == False  
        # checking for movement
        elif event.type == pygame.KEYDOWN:
            # left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # turning left depending on the current direction
                # moving up
                if motion == (0, -1):
                    motion = (-1, 0)
                # moving down
                elif motion == (0, 1):
                    motion = (1, 0)
                # moving right
                elif motion == (1, 0):
                    motion = (0, -1)
                # moving left
                elif motion == (-1, 0):
                    motion = (0, 1)
            # right
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # turning right depending on the current direction
                # moving up
                if motion == (0, -1):
                    motion = (1, 0)
                # moving down
                elif motion == (0, 1):
                    motion = (-1, 0)
                # moving right
                elif motion == (1, 0):
                    motion = (0, 1)
                # moving left
                elif motion == (-1, 0):
                    motion = (0, -1)

def move():
    global ate
    if not ate:
        move_snake()
    else:
        pos_last = snake[-1]
        move_snake()
        snake.append(pos_last)
        ate = False
        

def move_snake():
    global snake, running
    pos = 0
    for i, s in enumerate(snake):
        if i > 0:
            snake[i] = pos
            pos = s
        else:
            pos = s
            pos_head = ((s[0] + motion[0] * size_default) % size_window, (s[1] + motion[1] * size_default) % size_window)
            for s in snake[1:]:
                if pos_head == s:
                    running = False
                    break
            else:
                snake[i] = pos_head

def spawn_food():
    missing_food = 3 - len(food)
    if missing_food > 0 and random.randrange(100) < (missing_food ** 3) / 2:
        food.append((random.randrange(rows) * size_default, random.randrange(columns) * size_default))

def eating_food():
    global ate, score
    for f in food:
        if snake[0] == f:
            food.remove(f)
            ate = True
            score += 1

def draw():
    window.fill(color_background)
    # drawing snake
    for i, s in enumerate(snake):
        if i > 0:
            pygame.draw.rect(window, color_snake_body, (s[0], s[1], size_default, size_default))
        elif i == 0:
            pygame.draw.rect(window, color_snake_head, (s[0], s[1], size_default, size_default))
    # drawing food
    for f in food:
        pygame.draw.rect(window, color_food, (f[0], f[1], size_default, size_default))
    # drawing font
    textsurface = font.render(f'Score: {score}', False, (240, 0, 0))
    window.blit(textsurface, (0, 0))
    # update whats shown
    pygame.display.update()

game_loop()
pygame.quit()

