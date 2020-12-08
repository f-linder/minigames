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
        self.color_i = (0, 191, 255)
        self.color_o = (255, 255, 0)
        self.color_t = (138, 43, 226)
        self.color_s = (0, 255, 0)
        self.color_z = (255, 0, 0)
        self.color_j = (65, 105, 225)
        self.color_l = (255, 165, 0)
        self.type_to_color = {
            0: self.color_i,
            1: self.color_o,
            2: self.color_t,
            3: self.color_s,
            4: self.color_z,
            5: self.color_j,
            6: self.color_l,
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
        self.font = pygame.font.SysFont("Arial", 35, True, False)
        self.next = None
        self.current = None
        self.projection = None
        self.array = []
        self.score = None
        self.score_lines = None
        self.combo = 0
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
                if self.time_last_move > 400:
                    self.time_last_move = 0
                    self.move()
            self.play_again = self.endscreen()
        self.close()

    def endscreen(self):
        # draw block from bottom to top
        for y in range(19, -1, -1):
            for x in range(10):
                self.draw_side(x + 1, y + 1)
                pygame.time.wait(10)
                pygame.display.update()
        # drawing end screen
        pygame.draw.rect(self.window, self.color_side, (self.pixel_per_casket, self.pixel_per_casket, self.columns * self.pixel_per_casket, self.rows * self.pixel_per_casket))
        # updating score 
        scores, highscore = self.read_scores()
        # score_surface = self.font.render()

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
        highscore = False
        # read scores
        with open('./resources/scores.csv', 'r') as file:
            lines = file.readlines()
            scores = [int(line.strip()) for line in lines]
        # set new highscore
        before = 0
        for i, num in enumerate(scores):
            if not highscore and num < self.score:
                scores[i] = self.score
                highscore = True
            elif highscore:
                scores[i] = before
            before = num
        # write new highscore to file
        if highscore:
            with open('.resources/scores.csv', 'w') as file:
                for num in scores:
                    file.write(f'{str(num)}\n')

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
            self.combo *= len(full_lines)
            self.score += self.combo * 1000 * len(full_lines)
            self.remove_lines(full_lines)
            pygame.display.update()
            pygame.time.wait(250)
            # making the rest fall down
            self.drop_down(full_lines)
            self.draw_score()
            pygame.display.update()
        else:
            self.combo = 0
      
    def draw_score(self):
        score_surface = self.font.render(f'Score: {self.score}', False, self.color_side)
        self.window.blit(score_surface, ((self.columns + 3) * self.pixel_per_casket, 7 * self.pixel_per_casket))
        score_surface = self.font.render(f"Lines: {self.score_lines}", False, self.color_side)
        self.window.blit(score_surface, ((self.columns + 3) * self.pixel_per_casket, 9 * self.pixel_per_casket))

    def remove_lines(self, lines):
        # removing blocks in line
        for y in lines:
            for x in range(10):
                self.array[x][y] = -1
            pygame.draw.rect(self.window, self.white, (self.pixel_per_casket, (y + 1) * self.pixel_per_casket, 10 * self.pixel_per_casket, self.pixel_per_casket))
            pygame.draw.rect(self.window, self.black, (self.pixel_per_casket + 2, (y + 1) * self.pixel_per_casket + 2, 10 * self.pixel_per_casket - 4, self.pixel_per_casket - 4), 2)

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
                self.array[pos[0]][pos[1]] = typ
                self.draw_tetronimo(pos[0], pos[1], self.type_to_color[typ])
            self.current = self.next
            # game ends if the spawning block is on top of an existing one
            for pos in self.current.block.pos:
                if pos[1] < 0:
                    continue
                if self.array[pos[0]][pos[1]] != -1:   
                    self.running = False
            self.full_line()
            self.projection = None
            self.update_projection()
            # overdrawing next
            self.overdraw_next(self.next.block.pos)
            self.next = Block(random.randint(0, 2))
            # draw next
            color = self.type_to_color[self.next.typ]
            for x, y in self.next.block.pos:
                self.draw_next(x, y, color)
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
        self.combo = 0
        self.scored_last_round = False
        self.score = 0
        self.score_lines = 0
        self.next = Block(random.randint(0, 2))
        self.current = Block(random.randint(0, 1))
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
        pygame.display.update()
        
    def draw_current(self):
        color = self.type_to_color[self.current.typ]
        for pos in self.current.block.pos:
            self.draw_tetronimo(pos[0], pos[1], color)
        pygame.display.update()
    
    def draw_next(self, x, y, color):
        pygame.draw.rect(self.window, color, ((x + self.columns) * self.pixel_per_casket, (y + 3) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
        pygame.draw.rect(self.window, self.white, ((x + self.columns) * self.pixel_per_casket + 2, (y + 3) * self.pixel_per_casket + 2, self.pixel_per_casket - 4, self.pixel_per_casket - 4), 2)

    def draw_tetronimo(self, x, y, color):
        if x < 0 or x >= 10 or y < 0 or y >= 20:
            return
        pygame.draw.rect(self.window, color, ((x + 1) * self.pixel_per_casket, (y + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
        pygame.draw.rect(self.window, self.white, ((x + 1) * self.pixel_per_casket + 2, (y + 1) * self.pixel_per_casket + 2, self.pixel_per_casket - 4, self.pixel_per_casket - 4), 2)
    
    def draw_projection(self, x, y):
        pygame.draw.rect(self.window, self.color_side, ((x + 1) * self.pixel_per_casket + 2, (y + 1) * self.pixel_per_casket + 2, self.pixel_per_casket - 4, self.pixel_per_casket - 4), 2)
    
    def draw_side(self, x, y):
        # side inside
        pygame.draw.rect(self.window, self.color_side, (x * self.pixel_per_casket, y * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
        # side border
        pygame.draw.rect(self.window, self.color_border, (x * self.pixel_per_casket + 6, y * self.pixel_per_casket + 6, self.pixel_per_casket - 12, self.pixel_per_casket - 12))
        
    def overdraw_next(self, pos):
        for p in pos:
            pygame.draw.rect(self.window, self.color_background, ((p[0] + self.columns) * self.pixel_per_casket, (p[1] + 3) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
    
    def overdraw(self, pos):
        for p in pos:
            if p[1] >= 0:
                pygame.draw.rect(self.window, self.color_background, ((p[0] + 1) * self.pixel_per_casket, (p[1] + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))