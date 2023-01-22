import pygame
import random
import os

# координаты
HEIGHT = 1000
WIDTH = 1700
x = 0
y = -300
x1 = 30
y1 = 0
fps = 60
bg = "pic/pictures/bg.png"  # задний фон
# символы
symbols = {
    'diamond': f"pic/pictures/symbols/5.png",
    'floppy': f"pic/pictures/symbols/1.png",
    'hourglass': f"pic/pictures/symbols/3.png",
    'hourglass2': f"pic/pictures/symbols/2.png",
    'telephone': f"pic/pictures/symbols/4.png"}
GAME_INDICES = [1, 2, 3]  # индексы символов
caption = "Слоты"


# класс для анимации прокрутки
class Reels:
    def __init__(self, pos):
        self.slot_spin = False  # флаг для вращения
        self.symbol_slots = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)  # случайный выбор символов

        for i, k in enumerate(self.shuffled_keys):
            position = pos
            el = symbols[k]
            index = i
            self.symbol_slots.add(Symbol(el, position, index))  # добавление символа, его позиции и индекса
            pos = list(pos)
            pos[1] += 300  # последующее положение по координате у
            pos = tuple(pos)

    # звук прокрутки
    def sound(self):
        reel_sound = pygame.mixer.Sound('sounds/reel.wav')
        reel_sound.set_volume(0.2)
        reel_sound.play()

    def animation(self, delta_time):  # анимация
        if self.slot_spin:
            self.delay_time -= (delta_time * 1000)  # задержка
            self.spin_time -= (delta_time * 900)  # время вращения
            reel_stop = False  # флаг для остановки вращения

            if self.spin_time < 0:
                reel_stop = True
            if self.delay_time <= 0:
                # положения символов
                bottom = 100
                top = 1200
                for symbol in self.symbol_slots:
                    symbol.rect.bottom += bottom
                    if symbol.rect.top == top:
                        if reel_stop:
                            self.slot_spin = False
                        symbol_index = symbol.idx
                        symbol.kill()  # удаление старого символа
                        choice = random.choice(self.shuffled_keys)
                        position = symbol.x_val, -300
                        # положение символа после вращения
                        self.symbol_slots.add(Symbol(symbols[choice], position, symbol_index))

    def start_spin(self, delay_time):  # информация для начала вращения
        self.sound()
        self.delay_time = delay_time  # задержка вращения
        self.spin_time = delay_time + 1000  # общее время вращения
        self.slot_spin = True

    def reel_spin_result(self):
        # результат вращения
        spin_symbols = [self.symbol_slots.sprites()[i].slot_symbol for i in GAME_INDICES]
        return spin_symbols[::-1]


# основной класс, где появляются символы, считаются выигрыши и тп
class SlotMachine:
    def __init__(self, id, chips, socket):
        self.id = id
        self.chips = chips
        self.socket = socket
        self.surface = pygame.display.get_surface()
        self.reel_index = 0
        self.reel_list = {}
        self.switch = True  # флаг для изменения символов
        self.spinning = False  # флаг для анимации вращения
        self.animation = False  # флаг для проверки анимации выигрышей
        self.spin = {0: None, 1: None, 2: None, 3: None, 4: None}  # результат вращения

        self.spawn_reels()  # появление символов
        self.player = Player(self.id, self.chips, self.socket)
        self.ui = PlayerPanel(self.player)

    def spin_down(self):  # проверка после вращения
        for i in self.reel_list:
            if self.reel_list[i].slot_spin:
                self.switch = False
                self.spinning = True

        # проверка возможности вращения и количества символов в ряду
        if not self.switch and [self.reel_list[i].slot_spin for i in self.reel_list].count(False) == 5:
            self.switch = True
            self.spin = self.get_result()

            if self.check_wins(self.spin):  # если есть победные комбинации
                self.win_data = self.check_wins(self.spin)
                self.pay(self.win_data, self.player)
                self.animation = True

    def scroll(self):
        keys = pygame.key.get_pressed()
        # проверка нажал ли пользователь пробел, проверка возможности анимации вращения
        # и проверка меньше ли ставка баланса
        if (keys[pygame.K_SPACE]) and self.switch and int(self.player.balance) >= int(self.player.bet):
            self.spinning_reels()  # вращение символов
            self.spin_time = pygame.time.get_ticks()
            self.player.place_bet()
            self.player.payout = None

    def draw_reels(self, delta_time):  # перебор символов для анимации
        for reel in self.reel_list:
            self.reel_list[reel].animation(delta_time)

    def spawn_reels(self):  # появление символов
        if not self.reel_list:
            x_top_left = 10
            y_top_left = -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_top_left += (300 + x1)
            position = x_top_left, y_top_left
            self.reel_list[self.reel_index] = Reels(position)
            self.reel_index += 1

    def spinning_reels(self):  # вращение символов
        if self.switch:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.switch = False

            for i in self.reel_list:
                n = int(i)
                self.reel_list[i].start_spin(n * 200)
                self.animation = False

    def get_result(self):  # результат вращения
        for el in self.reel_list:
            self.spin[el] = self.reel_list[el].reel_spin_result()
        return self.spin

    def check_wins(self, result):  # проверка выигрыша
        win_symbols = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) >= 3:
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]
                    if len(longest_seq(possible_win)) >= 3:
                        # добавление символа в словарь и информации о нем
                        win_symbols[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]

        if win_symbols:
            return win_symbols

    def pay(self, win_data, player):  # функция для подсчета выигрышей
        n = 0
        for i in win_data.values():
            n += len(i[1])  # количество выигрышных символов
        # выигрыш равень ставке умноженной на общее количество выигрышных символов
        prize = (n * player.bet)  # выигрыш
        self.socket.addchips(self.id, prize)
        player.balance = int(player.balance)
        player.balance += int(prize)  # добавляем выигрыш к балансу
        player.balance = str(player.balance)
        player.payout = int(prize)  # выигрыш

    def win(self):  # информация для анимации выигрышных символов
        if self.animation and self.win_data:
            for i, k in list(self.win_data.items()):
                # проверка строки, в которой произошел выигрыш
                if i == 3:
                    animationRow = 1
                elif i == 1:
                    animationRow = 3
                else:
                    animationRow = 2
                animationCols = k[1]
                for i in self.reel_list:
                    # установка флагов на символы для анимации выигрышей
                    if i in animationCols:
                        self.reel_list[i].symbol_slots.sprites()[animationRow].fade_in = True
                    for symbol in self.reel_list[i].symbol_slots:
                        if not symbol.fade_in:
                            symbol.fade_out = True

    def update(self, delta_time):
        # отрисовка информации и вызов функций для дальнейшей работы
        self.spin_down()
        self.scroll()
        self.draw_reels(delta_time)
        for i in self.reel_list:
            self.reel_list[i].symbol_slots.draw(self.surface)
            self.reel_list[i].symbol_slots.update()
        self.ui.update()
        self.win()


# функция для вычисления выигрышей
def flip_horizontal(result):
    horizontal_values = []
    for value in result.values():
        horizontal_values.append(value)
    rows = len(horizontal_values)
    cols = len(horizontal_values[0])
    values1 = [[""] * rows for i in range(cols)]
    for i in range(rows):
        for k in range(cols):
            values1[k][rows - i - 1] = horizontal_values[i][k]
    values2 = [item[::-1] for item in values1]
    return values2


# функция для вычисления выигрышей
def longest_seq(hit):
    subSeqLength = 1
    longest = 1
    start = 0
    end = 0
    for i in range(len(hit) - 1):
        if hit[i] == hit[i + 1] - 1:
            subSeqLength += 1
            if subSeqLength > longest:
                longest = subSeqLength
                start = i + 2 - subSeqLength
                end = i + 2
        else:
            subSeqLength = 1
    return hit[start:end]


# класс информации пользователя
class PlayerPanel:
    def __init__(self, player):
        self.surface = pygame.display.get_surface()  # экран
        self.player = player
        # шрифты для баланса, ставки и выигрыша
        self.font = pygame.font.SysFont("Arial", 40)
        self.bet = pygame.font.SysFont("Arial", 40)
        self.win = pygame.font.SysFont("Arial", 65)

    def information(self):
        player_data = self.player.get_data()  # информация о балансе, ставке и тд
        text_color = (255, 255, 255)  # цвет текста
        # координаты
        n = self.surface.get_size()[0]
        x_1 = n - 20
        y_1 = self.surface.get_size()[1] - 30
        x_2 = 800
        n1 = self.surface.get_size()[1]
        y_2 = n1 - 60

        bet = self.bet.render(f'Ставка: ${player_data["bet"]}', True, text_color, None)  # текст ставки
        # положение текста
        position = x_1, y_1
        bet_rect = bet.get_rect(bottomright=position)

        balance = self.font.render(f"Баланс: ${player_data['balance']}", True, text_color, None)  # баланс
        # положение баланса
        x_1 = 20
        position = x_1, y_1
        balance_rect = balance.get_rect(bottomleft=position)
        # отображение текста
        pygame.draw.rect(self.surface, False, balance_rect)
        pygame.draw.rect(self.surface, False, bet_rect)
        self.surface.blit(balance, balance_rect)
        self.surface.blit(bet, bet_rect)
        if self.player.payout:  # проверка есть ли выигрыш
            payout = player_data["payout"]  # выигрыш
            win = self.win.render(f"ВЫ ВЫИГРАЛИ ${payout}!", True, text_color, None)  # текст выигрыша
            # положение выигрыша
            position = x_2, y_2
            win_rect = win.get_rect(center=position)
            self.surface.blit(win, win_rect)

    def update(self):
        color = (0, 0, 0)  # цвет панели отображения
        size = 0, 900, 1700, 100  # размер панели
        pygame.draw.rect(self.surface, color, pygame.Rect(size))  # рисовка панели
        self.information()  # отрисовка информации


# класс информации пользователя
class Player:
    def __init__(self, id, chips, socket):
        self.id = id
        self.chips = chips
        self.socket = socket
        self.balance = self.socket.getchips(self.id)
        self.bet = self.chips
        self.payout = 0

    def get_data(self):  # собирание информации о балансе, ставке и тп
        player_data = {"balance": str(self.balance), "bet": str(self.bet)}
        if self.payout:
            player_data["payout"] = str(self.payout)
        else:
            player_data["payout"] = "0"
        return player_data

    def place_bet(self):
        self.socket.addchips(self.id, -self.chips)  # уменьшение баланса в базе данных после ставки
        self.balance = int(self.balance)
        self.balance -= int(self.chips)  # уменьшение баланса на экране
        self.balance = str(self.balance)


# анимация символов
class Symbol(pygame.sprite.Sprite):
    def __init__(self, image, pos, idx):
        super().__init__()
        self.slot_symbol = image.split("/")[3].split(".")[0]  # получение символа
        self.image = pygame.image.load(image).convert_alpha()

        # координаты, индексы и тп
        self.pos = pos
        self.idx = idx
        self.rect = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left

        self.transparency = 255  # прозрачность по умолчанию
        self.fade_out = False  # флаг, если прозрачность символа 255
        self.fade_in = False  # флаг, если прозрачность символа не 255

    def update(self):
        if not self.fade_in and self.fade_out:
            if self.transparency > 155:
                self.transparency -= 10
                self.image.set_alpha(self.transparency)  # не выигрышные символы становятся прозрачными


# класс иницилизации игры
class SlotGame2:
    def __init__(self, id, chips, socket):
        os.environ["SDL_VIDEO_CENTERED"] = "1"  # положение в центре экрана по умолчанию
        # информация о балансе и тп
        self.id = id
        self.chips = chips
        self.socket = socket

        self.bg_image = pygame.image.load(bg)  # загрузка заднего фона
        self.clock = pygame.time.Clock()
        self.delta_time = 0

    def sound(self):
        # музыка
        start_sound = pygame.mixer.Sound('sounds/start_sound.mp3')
        start_sound.play()

    def render(self):
        pygame.init()
        size = (WIDTH, HEIGHT)  # размеры экрана
        screen = pygame.display.set_mode(size)  # установка размера экрана
        pygame.display.set_caption(caption)  # название окна
        logo = pygame.image.load('pic/pictures/logopic.jpg').convert()  # логотип
        pygame.display.set_icon(logo)  # установка логотипа
        machine_slot = SlotMachine(self.id, self.chips, self.socket)  # вызов класса
        self.start = pygame.time.get_ticks()  # начальное время
        self.run = True
        self.sound()  # стартовый звук
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
            # отображение картинок, время и тд
            n = pygame.time.get_ticks() - self.start
            self.delta_time = n / 1000
            self.start = pygame.time.get_ticks()
            pygame.display.flip()
            position = 0, 0
            screen.blit(self.bg_image, position)
            machine_slot.update(self.delta_time)
            self.clock.tick(fps)