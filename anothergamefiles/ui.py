from player import Player
from settings import *
import pygame


class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()

    def display_info(self):
        player_data = self.player.get_data()

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()
