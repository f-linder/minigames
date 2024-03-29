import pygame
import random
import copy
from .block import Block

class Tetris:
    def __init__(self):
        # setup for pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Tetris") 
        image = pygame.image.load("resources/tetris.png")

        pygame.display.set_icon(image)
        self.clock = pygame.time.Clock()
        self.time_last_event = 0
        self.time_last_move = 0
        # colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.color_background = (255, 250, 240)
        self.color_border = (169, 169, 169)
        self.color_side = (105, 105, 105)
        self.color_i = (0, 255, 255)
        self.color_o = (255, 255, 0)
        self.color_t = (255, 0, 255)
        self.color_s = (0, 255, 0)
        self.color_z = (255, 0, 0)
        self.color_j = (0, 0, 255)
        self.color_l = (255, 130, 0)
        self.type_to_color = {
            0: self.color_i,
            1: self.color_o,
            2: self.color_t,
            3: self.color_j,
            4: self.color_l,
            5: self.color_s,
            6: self.color_z,
        }
        # attributes
        # sizes
        self.rows = 20
        self.columns = 10
        self.bar_columns = 6
        self.width = self.columns + self.bar_columns + 2
        self.pixel_per_casket = 30
        self.game_height = (self.rows + 2) * self.pixel_per_casket
        self.game_width = (self.columns + 2) * self.pixel_per_casket
        self.bar_width = self.pixel_per_casket * self.bar_columns
        # game variabels
        self.window = pygame.display.set_mode((self.game_width + self.bar_width, self.game_height))
        self.play_again = True
        self.running = True
        self.font = pygame.font.SysFont("Arial", 30, True, True)
        self.font_num = pygame.font.SysFont("Arial", 20, True, False)
        self.next = None
        self.current = None
        self.projection = None
        self.array = []
        self.score = 0
        self.score_lines = 0
        self.combo = 1
        self.scored_last_round = False

        self.game_loop()
    
    def game_loop(self):
        while self.play_again:
            self.setup()
            while self.running:
                self.draw_current()
                self.check_events()
                dt = self.clock.tick()
                self.time_last_move += dt
                if self.time_last_move > 750 - (self.score_lines * 3):
                    self.time_last_move = 0
                    self.move()
            self.play_again = self.endscreen()
        self.close()

    def endscreen(self):
        # draw block from bottom to top
        for y in range(19, -1, -1):
            for x in range(self.width):
                self.draw_side(x + 1, y + 1)
            pygame.time.wait(50)
            pygame.display.update()
        # drawing end screen
        pygame.draw.rect(self.window, self.color_border, (self.pixel_per_casket, self.pixel_per_casket, (self.width - 2) * self.pixel_per_casket, self.rows * self.pixel_per_casket))
        # updating score 
        scores, highscore = self.read_scores()
        # drawing fonts
        font = pygame.font.SysFont("Arial", 50, True, False)
        score_surface = font.render("Your Score", False, self.color_z, self.window)
        self.window.blit(score_surface, (self.pixel_per_casket * 5, self.pixel_per_casket * 1.5))

        score_surface = font.render(f"{self.score}", False, self.color_s, self.window)
        self.window.blit(score_surface, (self.pixel_per_casket * 2, self.pixel_per_casket * 3 + self.pixel_per_casket / 3))

        score_surface = font.render("Highscores", False, self.color_z, self.window)
        self.window.blit(score_surface, (self.pixel_per_casket * 5, self.pixel_per_casket * 5.5))

        for i, num in enumerate(scores):
            if num == self.score:
                score_surface = font.render(f"{i + 1}. Place: {num}", False, self.color_s)
            else:
                score_surface = font.render(f"{i + 1}. Place: {num}", False, self.color_z)
            self.window.blit(score_surface, (self.pixel_per_casket * 1.5, self.pixel_per_casket * (7.5 + i * 2)))

        score_surface = self.font.render("Press Spacebar to play again", False, self.color_z)
        self.window.blit(score_surface, (self.pixel_per_casket * 2, self.pixel_per_casket * 19))

        
        pygame.display.update()

        # checking for event
        while True:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    return False
                # play again
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return True

    def read_scores(self):
        scores = []
        # read scores
        with open('resources/scores.csv', 'r') as file:
            lines = file.readlines()
            scores = [int(line.strip()) for line in lines]
        # set new highscore
        scores.append(self.score)
        scores.sort()
        scores = scores[::-1]
        scores = scores[:5]
        # write new highscore to file
        with open('resources/scores.csv', 'w') as file:
            for num in scores:
                file.write(f'{str(num)}\n')

        highscore = False
        if self.score in scores:
            highscore = True

        return (scores, highscore)

    def full_line(self):
        # lines to remove
        full_lines = []
        # checking which lines are full and appending them to list
        for y in range(self.rows):
            for x in range(10):
                if self.array[x][y] == -1:
                    break
                elif x == 9:
                    self.score_lines += 1
                    full_lines.append(y)
        
        if len(full_lines) > 0:
            # removing lines
            self.score += self.combo * 1000 * len(full_lines)
            self.combo += len(full_lines)
            self.remove_lines(full_lines)
            pygame.display.update()
            pygame.time.wait(250)
            # making the rest fall down
            self.drop_down(full_lines)
        else:
            self.combo = 1
        
      
    def draw_score(self):
        # overdraw old score
        for x in range(2, 7):
            self.overdraw_next([(x, 4)])
            self.overdraw_next([(x, 5)])
            self.overdraw_next([(x, 8)])
            self.overdraw_next([(x, 9)])
            self.overdraw_next([(x, 12)])
            self.overdraw_next([(x, 13)])
        # combo text
        score_surface = self.font_num.render(f"x {self.combo}", False, self.color_z)
        self.window.blit(score_surface, ((self.columns + 4) * self.pixel_per_casket, 8.5 * self.pixel_per_casket))
        # score text
        score_surface = self.font_num.render(f"{self.score}", False, self.color_z)
        self.window.blit(score_surface, ((self.columns + 3) * self.pixel_per_casket + 10, 12.5 * self.pixel_per_casket))
        # lines text
        score_surface = self.font_num.render(f"{self.score_lines}", False, self.color_z)
        self.window.blit(score_surface, ((self.columns + 3.5) * self.pixel_per_casket + 10, 16.5 * self.pixel_per_casket))


    def remove_lines(self, lines):
        # removing blocks in line
        for y in lines:
            for x in range(10):
                self.array[x][y] = -1
            pygame.draw.rect(self.window, self.white, (self.pixel_per_casket, (y + 1) * self.pixel_per_casket, 10 * self.pixel_per_casket, self.pixel_per_casket))

    def drop_down(self, lines):
        # for each to be removed... (starting from top)
        for row in lines:
            # drop every row...
            for y in range(row - 1, -1, -1):
                # one down
                for x in range(self.columns):
                    self.array[x][y + 1] = self.array[x][y]
            # -1 on top
            for x in range(10):
                self.array[x][0] = -1
        # draw new gamestate
        # background
        pygame.draw.rect(self.window, self.color_background, (self.pixel_per_casket, self.pixel_per_casket, self.columns * self.pixel_per_casket, self.rows * self.pixel_per_casket))
        # board
        for x in range(self.columns):
            for y in range(self.rows):
                if self.array[x][y] != -1:
                    self.draw_tetronimo(x, y, self.type_to_color[self.array[x][y]])   

    def update_projection(self):
        # drawing over old projection
        if self.projection:
            self.overdraw(self.projection.block.pos)
        # getting new projection
        self.projection = copy.deepcopy(self.current)
        while not self.projection.fixed:
            self.projection.move(self.array, 0, 1)
        # drawing the new projection
        for pos in self.projection.block.pos:
            self.draw_projection(pos[0], pos[1])

    def move(self):
        # drawing over current position before move and redrawing
        self.overdraw(self.current.block.pos)
        self.current.move(self.array, 0, 1)
        # current is now placed
        if self.current.fixed:
            # add current to game state
            typ = self.current.typ
            for pos in self.current.block.pos:
                # if block whos now fixed reaches out of the top
                if pos[1] < 0:
                    self.running = False
                    break
                else:
                    self.array[pos[0]][pos[1]] = typ
                    self.draw_tetronimo(pos[0], pos[1], self.type_to_color[typ])
            
            if self.running:
                self.current = self.next
                self.full_line()
                self.projection = None
                self.update_projection()
                # overdrawing next
                self.overdraw_next(self.next.block.pos)
                self.next = Block(random.randint(0, 6))
                # draw next
                color = self.type_to_color[self.next.typ]
                for x, y in self.next.block.pos:
                    self.draw_next(x, y, color)
        self.draw_score()
        pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            # checking for quit
            if event.type == pygame.QUIT:
                self.running = False
            # checking for key strokes
            elif event.type == pygame.KEYDOWN:
                # checking for 
                # move left
                if event.key == pygame.K_LEFT:
                    self.overdraw(self.current.block.pos)
                    self.current.move(self.array, -1, 0)
                    self.update_projection()
                    self.draw_current()
                # move right
                elif event.key == pygame.K_RIGHT:
                    self.overdraw(self.current.block.pos)
                    self.current.move(self.array, 1, 0)
                    self.update_projection()
                    self.draw_current()
                # move down
                elif event.key == pygame.K_DOWN:
                    self.overdraw(self.current.block.pos)
                    self.current.move(self.array, 0, 1)
                    self.draw_current()
                # rotate
                elif event.key == pygame.K_x:
                    self.overdraw(self.current.block.pos)
                    self.current.change_state(self.array)
                    self.draw_current()
                    self.update_projection()
                # move to bottom
                elif event.key == pygame.K_SPACE:
                    self.overdraw(self.current.block.pos)
                    self.current = self.projection
                    self.move()
        
    def setup(self):
        self.running = True
        self.combo = 1
        self.scored_last_round = False
        self.score = 0
        self.score_lines = 0
        self.next = Block(random.randint(0, 6))
        self.current = Block(random.randint(0, 6))
        self.array = [[-1 for i in range(self.rows)] for j in range(self.columns)]
        self.draw_start()
        self.update_projection()

    def close(self):
        pygame.font.quit()
        pygame.quit()
        exit()

    def draw_start(self):
        self.draw_score()
        self.window.fill(self.color_background)
        # next text
        score_surface = self.font.render("Next", False, self.color_side)
        self.window.blit(score_surface, ((self.columns + 3) * self.pixel_per_casket + 10, 1 * self.pixel_per_casket + 5))
        # combo text
        score_surface = self.font.render("Multiplier", False, self.color_side)
        self.window.blit(score_surface, ((self.columns + 2) * self.pixel_per_casket + 10, 7 * self.pixel_per_casket + 5))
        # score text
        score_surface = self.font.render("Score", False, self.color_side)
        self.window.blit(score_surface, ((self.columns + 3) * self.pixel_per_casket + 5, 11 * self.pixel_per_casket + 5))
        # lines text
        score_surface = self.font.render("Lines", False, self.color_side)
        self.window.blit(score_surface, ((self.columns + 3) * self.pixel_per_casket + 5, 15 * self.pixel_per_casket + 5))
        # draw next
        color = self.type_to_color[self.next.typ]
        for x, y in self.next.block.pos:
            self.draw_next(x, y, color)
        # drawing border
        for x in range(self.width):
            # top
            self.draw_side(x, 0)
            # bottom
            self.draw_side(x, self.rows + 1)
        for y in range(1, self.rows + 1):
            # left
            self.draw_side(0, y)
            # right middle
            self.draw_side(self.columns + 1, y)
            # right
            self.draw_side(self.width - 1, y)
        # horizontal lines at right
        for x in range(self.bar_columns + 1):
            self.draw_side(x + self.columns + 2, 6)
            self.draw_side(x + self.columns + 2, 10)
            self.draw_side(x + self.columns + 2, 14)
            for y in range(18,21):
                self.draw_side(x + self.columns + 2, y)
            
        pygame.display.update()
        
    def draw_current(self):
        color = self.type_to_color[self.current.typ]
        for pos in self.current.block.pos:
            self.draw_tetronimo(pos[0], pos[1], color)
        pygame.display.update()
    
    def draw_next(self, x, y, color):
        pygame.draw.rect(self.window, color, ((x + self.columns) * self.pixel_per_casket, (y + 4) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
        pygame.draw.rect(self.window, self.white, ((x + self.columns) * self.pixel_per_casket + 2, (y + 4) * self.pixel_per_casket + 2, self.pixel_per_casket - 4, self.pixel_per_casket - 4), 2)

    def draw_tetronimo(self, x, y, color):
        if x < 0 or x >= 10 or y < 0 or y >= 20:
            return
        pygame.draw.rect(self.window, color, ((x + 1) * self.pixel_per_casket, (y + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
        pygame.draw.rect(self.window, self.white, ((x + 1) * self.pixel_per_casket + 2, (y + 1) * self.pixel_per_casket + 2, self.pixel_per_casket - 4, self.pixel_per_casket - 4), 2)
    
    def draw_projection(self, x, y):
        if y >= 0:
            pygame.draw.rect(self.window, self.white, ((x + 1) * self.pixel_per_casket, (y + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
            pygame.draw.rect(self.window, self.color_side, ((x + 1) * self.pixel_per_casket + 2, (y + 1) * self.pixel_per_casket + 2, self.pixel_per_casket - 4, self.pixel_per_casket - 4), 2)
    
    def draw_side(self, x, y):
        # side inside
        pygame.draw.rect(self.window, self.color_side, (x * self.pixel_per_casket, y * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
        # side border
        pygame.draw.rect(self.window, self.color_border, (x * self.pixel_per_casket + 6, y * self.pixel_per_casket + 6, self.pixel_per_casket - 12, self.pixel_per_casket - 12))
        
    def overdraw_next(self, pos):
        for p in pos:
            pygame.draw.rect(self.window, self.color_background, ((p[0] + self.columns) * self.pixel_per_casket, (p[1] + 4) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
    
    def overdraw(self, pos):
        for p in pos:
            if p[1] >= 0:
                pygame.draw.rect(self.window, self.color_background, ((p[0] + 1) * self.pixel_per_casket, (p[1] + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))