from machine import SlotMachine
from settings import *
import pygame


class Game:
    def __init__(self, id, bet, socket):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # размер окна
        pygame.display.set_caption("Слоты")  # название
        bg_image = "pic/pictures/bg.jpg"
        self.bg_image = pygame.image.load(bg_image).convert_alpha()  # установка заднего фона
        self.m = SlotMachine()
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.time = pygame.time.get_ticks()
        self.id = id
        self.bet = bet
        self.socket = socket
        self.sound()  # начальная мелодия при открытии игры

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.delta_time = (pygame.time.get_ticks() - self.time) / 1000
            self.time = pygame.time.get_ticks()
            pygame.display.flip()
            self.screen.blit(self.bg_image, (0, 0))
            self.m.update(self.delta_time)
            self.clock.tick(FPS)

    def sound(self):
        # музыка
        start_sound = pygame.mixer.Sound('sounds/start_sound.mp3')
        start_sound.play()


if __name__ == '__main__':
    game = Game()
    game.run()
