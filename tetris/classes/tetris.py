from .object import Object
import pygame
import random

class Tetris:
    def __init__(self):
        # setup for pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Tetris") 
        image = pygame.image.load("tetris.png")
        pygame.display.set_icon(image)
        # colors
        self.black = (0, 0, 0)
        self.color_background = (244, 228, 215)
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
        self.array = []
        self.score = None
        self.score_lines = None

        self.game_loop()
    
    def game_loop(self):
        self.setup()
        while self.running:
            self.draw()
            self.check_events()
        self.close()

    def check_events(self):
        for event in pygame.event.get():
            # checking for quit
            if event.type == pygame.QUIT:
                self.running = False

    def setup(self):
        self.running = True
        self.score = 0
        self.score_lines = 0
        self.next = Object(random.randint(0, 7))
        self.current = Object(random.randint(0, 7))
        self.array = [[-1 for i in range(self.rows)] for j in range(self.columns)]
    
    def close(self):
        pygame.font.quit()
        pygame.quit()
        exit()

    def draw(self):
        self.window.fill(self.color_background)

        # drawing border
        for x in range(self.columns + self.bar_columns + 2):
            # top
            self.draw_block(x - 1, -1, self.color_side)
            # bottom
            self.draw_block(x - 1, self.rows, self.color_side)
        for y in range(1, self.rows + 1):
            # left
            self.draw_block(-1, y - 1, self.color_side)
            # right middle
            self.draw_block(self.columns, y - 1, self.color_side)
            # right
            self.draw_block(self.columns + self.bar_columns, y - 1, self.color_side)

        # horizontal lines at right
        for x in range(self.columns + 2, self.bar_width + self.columns + 1):
            self.draw_block(x - 1, 6, self.color_side)
        
        # drawing tetrominos
        for x, row in enumerate(self.array):
            for y, typ in enumerate(row):
                if typ != -1:
                    self.draw_block(x, y, self.type_to_color[typ])

        pygame.display.update()

    def draw_block(self, x, y, color):
        if color == self.color_side:
            # side inside
            pygame.draw.rect(self.window, self.color_border, ((x + 1) * self.pixel_per_casket, (y + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
            # side border
            pygame.draw.rect(self.window, color, ((x + 1) * self.pixel_per_casket, (y + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket), 8)
        else:
            # normal inside
            pygame.draw.rect(self.window, color, ((x + 1) * self.pixel_per_casket, (y + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket))
            # normal border
            pygame.draw.rect(self.window, self.black, ((x + 1) * self.pixel_per_casket, (y + 1) * self.pixel_per_casket, self.pixel_per_casket, self.pixel_per_casket), 3)