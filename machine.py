import pygame
from player import Player
from reel import *
from settings import *
from ui import UI


class SlotMachine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.spawn()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

    def cooldown(self):
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True

    def scroll(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.spin()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn(self):
        if not self.reel_list:
            x_topl, y_topl = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topl, y_topl = (x_topl + (300 + X_OFFSET)), y_topl

            self.reel_list[self.reel_index] = Reel((x_topl, y_topl))
            self.reel_index += 1

    def spin(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in self.reel_list:
                self.reel_list[reel].scroll_on(int(reel) * 200)
                self.win_animation_ongoing = False

    def get_result(self):
        pass

    def update(self, delta_time):
        self.cooldown()
        self.scroll()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
