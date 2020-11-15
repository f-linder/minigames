import pygame
import random
from .block import Block

class Tetris:
    def __init__(self):
        # setup for pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Tetris") 
        image = pygame.image.load("tetris.png")
        pygame.display.set_icon(image)
        self.clock = pygame.time.Clock()
        self.time_last_draw = 0
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
        self.font = pygame.font.SysFont("Arial", 30, True, False)
        self.next = None
        self.current = None
        self.current_last_pos = None
        self.array = []
        self.score = None
        self.score_lines = None

        self.game_loop()
    
    def game_loop(self):
        self.setup()
        while self.running:
            self.check_events()
            self.draw_current()
            dt = self.clock.tick()
            self.time_last_move += dt
            if self.time_last_move > 333:
                self.time_last_move = 0
                self.move()
        self.close()
    
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
            self.next = Block(0)
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
                    self.draw_current()
                # move right
                elif event.key == pygame.K_RIGHT:
                    self.overdraw(self.current.block.pos)
                    self.current.move(self.array, 1, 0)
                    self.draw_current()
                # move down
                elif event.key == pygame.K_DOWN:
                    self.overdraw(self.current.block.pos)
                    self.current.move(self.array, 0, 1)
                    self.draw_current()
                # rotate
                elif event.key == pygame.K_x:
                    self.overdraw(self.current.block.pos)
                    self.current.block.change_state(self.array)
                    self.draw_current()
        

    def setup(self):
        self.running = True
        self.score = 0
        self.score_lines = 0
        self.next = Block(0)
        self.current = Block(0)
        self.current_last_pos = self.current.block.pos.copy()
        self.array = [[-1 for i in range(self.rows)] for j in range(self.columns)]
        self.draw_start()

    def close(self):
        pygame.font.quit()
        pygame.quit()
        exit()

    def draw_start(self):
        self.window.fill(self.color_background)
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

    def draw_tetronimo(self, x, y, color):
        if x < 0 or x >= 10 or y < 0 or y >= 20:
            return
        # normal inside
        pygame.draw.rect(self.window, color, ((x + 1) * self.pixel_per_casket, (y + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
        pygame.draw.rect(self.window, self.white, ((x + 1) * self.pixel_per_casket + 2, (y + 1) * self.pixel_per_casket + 2, self.pixel_per_casket - 4, self.pixel_per_casket - 4), 2)
        
    def draw_side(self, x, y):
        # side border
        pygame.draw.rect(self.window, self.color_side, (x * self.pixel_per_casket, y * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
        # side inside
        pygame.draw.rect(self.window, self.color_border, (x * self.pixel_per_casket + 6, y * self.pixel_per_casket + 6, self.pixel_per_casket - 12, self.pixel_per_casket - 12))
        
    def overdraw(self, pos):
        for p in pos:
            if p[1] >= 0:
                pygame.draw.rect(self.window, self.color_background, ((p[0] + 1) * self.pixel_per_casket, (p[1] + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))