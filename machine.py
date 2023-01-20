from player import Player
from reel import *
from settings import *
from ui import UI


class SlotMachine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.reels = {}
        self.spin_result = {0: None, 1: None, 2: None}
        self.index = 0
        self.can_toggle = True
        self.spinning = False
        self.flag_win = False
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)
        self.spawn()

    def reel_spin(self):
        for reel in self.reels:
            if self.reels[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reels[reel].reel_is_spinning for reel in self.reels].count(False) == 3:
            self.can_toggle = True
            self.spin_result = self.get_result()
            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)

    def scroll(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:  # если пользовател нажал пробел то начинается анимация
            self.spin()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):  # анимация вращения
        for reel in self.reels:
            self.reels[reel].animate(delta_time)

    def spawn(self):  # изначальное положение символов
        if not self.reels:
            x_topl, y_topl = 10, -300  # начальные координаты
        while self.index < 3:
            if self.index > -1:
                x_topl, y_topl = (x_topl + 300 + X_OFFSET), y_topl  # расположение последующих символов

            self.reels[self.index] = Reel((x_topl, y_topl))  # прокрутка
            self.index += 1

    def spin(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.can_toggle = False

            for reel in self.reels:  # прокрутка
                self.reels[reel].scroll_on(int(reel) * 200)

    def get_result(self):  # результат вращения
        for reel in self.reels:
            self.spin_result[reel] = self.reels[reel].spin_result()
        return self.spin_result

    def check_wins(self, result):  # проверка выигрышных комбинаций
        lines = flip_horizontal(result)
        if lines[1][0] == lines[1][1] == lines[1][2]:
            self.flag_win = True
        elif lines[0][0] == lines[0][1] == lines[0][2]:
            self.flag_win = True
        elif lines[2][0] == lines[2][1] == lines[2][2]:
            self.flag_win = True
        else:
            self.flag_win = False

    def win(self):
        pass

    def update(self, delta_time):
        self.reel_spin()
        self.scroll()
        self.draw_reels(delta_time)
        for reel in self.reels:
            self.reels[reel].symbol_list.draw(self.display_surface)
            self.reels[reel].symbol_list.update()
        self.win()
        self.ui.update()
