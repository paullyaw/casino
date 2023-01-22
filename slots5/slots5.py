import pygame
import random
import os
import casinosocket

HEIGHT = 1000
WIDTH = 1700
font = 'pic/muller.ttf'
x = 0
y = -300
x1 = 30
y1 = 0
fps = 120
bg = "pic/pictures/bg.png"
# символы
symbols = {
    'diamond': f"pic/pictures/symbols/5.png",
    'floppy': f"pic/pictures/symbols/1.png",
    'hourglass': f"pic/pictures/symbols/3.png",
    'hourglass2': f"pic/pictures/symbols/2.png",
    'telephone': f"pic/pictures/symbols/4.png"}
GAME_INDICES = [1, 2, 3]
caption = "Слоты"


class Reels:
    def __init__(self, pos):
        self.slot_spin = False
        self.symbol_slots = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5]

        for i, k in enumerate(self.shuffled_keys):
            self.symbol_slots.add(Symbol(symbols[k], pos, i))
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    # звук прокрутки
    def sound(self):
        reel_sound = pygame.mixer.Sound('sounds/reel.wav')
        reel_sound.set_volume(0.2)
        reel_sound.play()

    def animation(self, delta_time):
        if self.slot_spin:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_stop = False

            if self.spin_time < 0:
                reel_stop = True
            if self.delay_time <= 0:
                for symbol in self.symbol_slots:
                    symbol.rect.bottom += 100
                    if symbol.rect.top == 1200:
                        if reel_stop:
                            self.slot_spin = False
                        symbol_idx = symbol.idx
                        symbol.kill()
                        choice = random.choice(self.shuffled_keys)
                        self.symbol_slots.add(
                            Symbol(symbols[choice], ((symbol.x_val), -300), symbol_idx))

    def start_spin(self, delay_time):
        self.sound()
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.slot_spin = True

    def reel_spin_result(self):
        spin_symbols = [self.symbol_slots.sprites()[i].slot_symbol for i in GAME_INDICES]
        return spin_symbols[::-1]


class SlotMachine:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.balance = 1000000000
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False

        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

    def cooldowns(self):
        for reel in self.reel_list:
            if self.reel_list[reel].slot_spin:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reel_list[reel].slot_spin for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()

            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-1, 1)

    def scroll(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]) and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.balance += self.currPlayer.bet
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animation(delta_time)

    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + x1), y_topleft

            self.reel_list[self.reel_index] = Reels((x_topleft, y_topleft))
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                self.win_animation_ongoing = False

    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result

    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) == 3:
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]
                    if len(longest_seq(possible_win)) == 3:
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits

    def pay_player(self, win_data, curr_player):
        multiplier = 0
        for v in win_data.values():
            multiplier += len(v[1])
        spin_payout = (multiplier * curr_player.bet)
        curr_player.balance += spin_payout
        self.balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    def win(self):
        if self.win_animation_ongoing and self.win_data:
            for i, k in list(self.win_data.items()):
                if i == 3:
                    animationRow = 1
                elif i == 1:
                    animationRow = 3
                else:
                    animationRow = 2
                animationCols = k[1]
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_slots.sprites()[animationRow].fade_in = True
                    for symbol in self.reel_list[reel].symbol_slots:
                        if not symbol.fade_in:
                            symbol.fade_out = True

    def update(self, delta_time):
        self.cooldowns()
        self.scroll()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_slots.draw(self.surface)
            self.reel_list[reel].symbol_slots.update()
        self.ui.update()
        self.win()


def flip_horizontal(result):
    horizontal_values = []
    for value in result.values():
        horizontal_values.append(value)
    rows, cols = len(horizontal_values), len(horizontal_values[0])
    hvals2 = [[""] * rows for _ in range(cols)]
    for x in range(rows):
        for y in range(cols):
            hvals2[y][rows - x - 1] = horizontal_values[x][y]
    hvals3 = [item[::-1] for item in hvals2]
    return hvals3


def longest_seq(hit):
    subSeqLength, longest = 1, 1
    start, end = 0, 0
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


class UI:
    def __init__(self, id):
        self.player = id
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(font, 30)
        self.bet_font = pygame.font.Font(font, 30)
        self.win_font = pygame.font.Font(font, 70)
        self.win_text_angle = random.randint(-4, 4)

    def display_info(self):
        player_data = self.player.get_data()
        balance_surf = self.font.render("Баланс: $" + player_data["balance"], True, (255, 255, 255), None)
        x, y = 20, self.display_surface.get_size()[1] - 30
        balance_rect = balance_surf.get_rect(bottomleft=(x, y))

        bet_surf = self.bet_font.render("Ставка: $" + player_data['bet'], True, (255, 255, 255), None)
        x = self.display_surface.get_size()[0] - 20
        bet_rect = bet_surf.get_rect(bottomright=(x, y))

        # Draw player data
        pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render("ВЫ ВЫИГРАЛИ $" + last_payout + "!", True, (255, 255, 255), None)
            x1 = 800
            y1 = self.display_surface.get_size()[1] - 60
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center=(x1, y1))
            self.display_surface.blit(win_surf, win_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1700, 100))
        self.display_info()


class Player:
    def __init__(self):
        self.balance = 9999
        self.bet = 15.00
        self.last_payout = 0.00
        self.total_won = 0.00
        self.total_wager = 0.00

    def get_data(self):
        player_data = {'balance': "{:.2f}".format(self.balance), 'bet': "{:.2f}".format(self.bet)}
        if self.last_payout:
            player_data['last_payout'] = "{:.2f}".format(self.last_payout)
        else:
            player_data['last_payout'] = "N/A"

        player_data['total_won'] = "{:.2f}".format(self.total_won)
        player_data['total_wager'] = "{:.2f}".format(self.total_wager)
        return player_data

    def place_bet(self):
        bet = self.bet
        self.balance -= bet
        self.total_wager += bet


class Symbol(pygame.sprite.Sprite):
    def __init__(self, image, pos, idx):
        super().__init__()

        self.slot_symbol = image.split("/")[3].split(".")[0]
        self.image = pygame.image.load(image).convert_alpha()

        self.pos = pos
        self.idx = idx
        self.rect = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left

        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        if not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 10
                self.image.set_alpha(self.alpha)


class SlotGame_2:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.bg_image = pygame.image.load(bg)
        self.clock = pygame.time.Clock()
        self.delta_time = 0

    def sound(self):
        # музыка
        start_sound = pygame.mixer.Sound('sounds/start_sound.mp3')
        start_sound.play()

    def render(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Слоты')
        self.m = SlotMachine()
        self.start = pygame.time.get_ticks()
        self.run = True
        self.sound()
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
            n = pygame.time.get_ticks() - self.start
            self.delta_time = n / 1000
            self.start = pygame.time.get_ticks()
            pygame.display.flip()
            self.screen.blit(self.bg_image, (0, 0))
            self.m.update(self.delta_time)
            self.clock.tick(fps)


if __name__ == '__main__':
    slot_game = SlotGame_2()
    slot_game.render()
