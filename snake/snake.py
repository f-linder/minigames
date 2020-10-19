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
play_again = True
running = True
# list for snake
snake = []
# set head in the middle of the screen
snake.append((size_window - math.floor(columns / 2 - 2) * size_default, size_window - int(columns / 2) * size_default))
# food + timer
food = []
ate = False
# direction of motion
motion = (1, 0)
# score
score = 0
font = pygame.font.SysFont('Arial', 30, True, True)

def game_loop():
    global running, play_again
    while play_again:
        running = True
        setup()
        while running:
            pygame.time.delay(100)
            check_events()
            spawn_food()
            move()
            eating_food()
            draw()
        play_again = end_screen()

def setup():
    global snake, food, score, ate, motion
    score = 0
    snake = []
    snake.append((size_window - math.floor(columns / 2 - 2) * size_default, size_window - int(columns / 2) * size_default))
    food = []
    ate = False
    motion = (1, 0)

def end_screen():
    global running, play_again
    # draw end screen
    window.fill(color_background)
    # read scores from .csv file and update
    scores, highscore = read_scores()
    # display scores
    score_font = pygame.font.SysFont('Arial', 50, True, False)
    score_surface = score_font.render(f'Your Score is: {score}', False, color_snake_body)
    window.blit(score_surface, (int(size_window * 0.15), int(size_window * 0.1)))
    score_surface = score_font.render('Highscores:', False, color_food)
    window.blit(score_surface, (int(size_window * 0.15), int(size_window * 0.25)))
    once = True
    for i, num in enumerate(scores):
        if once and highscore and num == score:
            score_surface = font.render(f'{i+1}.: {num}', False, color_snake_head)
            once = False
        else:
            score_surface = font.render(f'{i+1}.: {num}', False, color_food)
        window.blit(score_surface, (int(size_window * 0.6), int(size_window * 0.27) + (i * size_default * 3)))
    score_surface = score_font.render('Press spacebar to', False, color_snake_head)
    window.blit(score_surface, (int(size_window * 0.15), int(size_window * 0.8)))
    score_surface = score_font.render('start a new round!', False, color_snake_head)
    window.blit(score_surface, (int(size_window * 0.15), int(size_window * 0.88)))
    pygame.display.update()
    # check if user want to play again
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

def read_scores():
    scores = []
    highscore = False
    # read scores
    with open('scores.csv', 'r') as file:
        lines = file.readlines()
        scores = [int(line.strip()) for line in lines]
    # set new highscore
    before = 0
    for i, num in enumerate(scores):
        if not highscore and num < score:
            scores[i] = score
            highscore = True
        elif highscore:
            scores[i] = before
        before = num
    # write new highscore to file
    if highscore:
        with open('scores.csv', 'w') as file:
            for num in scores:
                file.write(f'{str(num)}\n')

    return (scores, highscore)

def check_events():
    global running, motion, play_again
    for event in pygame.event.get():
        # checking for quit
        if event.type == pygame.QUIT:
            running = False  
            play_again = False
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
    textsurface = font.render(f'Score: {score}', False, color_food)
    window.blit(textsurface, (0, 0))
    # update whats shown
    pygame.display.update()

game_loop()
pygame.quit()
exit()
