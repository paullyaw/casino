from settings import *
import pygame
import random


class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group()
        self.reel_is_spinning = False
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5]
        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True
            if self.delay_time <= 0:
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 50
                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                        symbol_idx = symbol.idx
                        symbol.kill()
                        self.symbol_list.add(
                            Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -300), symbol_idx))

    # звук прокрутки
    def sound(self):
        reel_sound = pygame.mixer.Sound('sounds/reel.wav')
        reel_sound.set_volume(0.2)
        reel_sound.play()

    def scroll_on(self, delay_time):
        self.sound()
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    # результат вращения по индексам символов
    def spin_result(self):
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)
        return spin_symbols[::-1]


class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()
        self.sym_type = pathToFile.split('/')[3].split('.')[0]
        self.pos, self.idx = pos, idx
        self.image = pygame.image.load(pathToFile).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left


def flip_horizontal(result):
    horizontal_values = []
    l3 = []
    for value in result.values():
        horizontal_values.append(value)
    row, col = len(horizontal_values), len(horizontal_values[0])
    l2 = [[""] * row for k in range(col)]
    for x in range(row):
        for y in range(col):
            l2[y][row - x - 1] = horizontal_values[x][y]
    for i in l2:
        l3.append(i[::-1])
    print(l3)
    return l3
