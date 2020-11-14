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
        # attributes
        self.rows = 20
        self.columns = 10
        self.pixel_per_casket = 30
        self.game_height = (self.rows + 1) * self.pixel_per_casket
        self.game_width = (self.columns + 2) * self.pixel_per_casket
        self.bar_width = int(self.game_width / 3)
        self.window = pygame.display.set_mode((self.game_width + self.bar_width, self.game_height))
        self.play_again = True
        self.running
        self.font = pygame.font.SysFont("Arial", 30, True, False)
        self.next
        self.array = []
        self.score
        self.score_lines


        self.setup()
        
    def setup(self):
        self.running = True
        self.score = 0
        self.score_lines = 0
        self.next = Object()
        self.array = [[True for i in range(self.columns)] for j in range(self.rows)]

    def draw(self):


