from player import Player
from settings import *
import pygame


class UI:
    def __init__(self, player):
        self.font = None
        self.player = player
        self.display_surface = pygame.display.get_surface()

    def display_info(self):
        pass

    def update(self):
        pygame.draw.rect(self.display_surface, "Black", pygame.Rect(0, 900, 1700, 100))  # панель с балансом,
        # ставкой и тп
        self.display_info()
