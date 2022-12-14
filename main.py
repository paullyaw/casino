from machine import SlotMachine
from settings import *
import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Слоты')
        self.bg_image = pygame.image.load(bg_image).convert_alpha()
        self.m = SlotMachine()
        self.clock = pygame.time.Clock()
        self.delta_time = 0

    def run(self):

        self.start_time = pygame.time.get_ticks()
        run = True
        while run:
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()
            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.m.update(self.delta_time)
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break




if __name__ == '__main__':
    game = Game()
    game.run()
