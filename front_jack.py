import pygame as pygame
from blago_black import *
from const import *
import sys
import time
pygame.init()

font = pygame.font.SysFont("Arial", 20)
textfont = pygame.font.SysFont('Comic Sans MS', 35)
game_end = pygame.font.SysFont('dejavusans', 100)
blackjack = pygame.font.SysFont('roboto', 70)
id = None
socket = None
chips = 0
gameDisplay = None
clickcount = 0

###text object render
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def end_text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# game text display
def game_texts(text, x, y):
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def game_finish(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, game_end, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


def black_jack(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, blackjack, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


# button display
def button(msg, x, y, w, h, ic, ac, action=None):
    global clickcount
    global id
    global socket
    global chips
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 != None:
            if clickcount == 0:
                socket.addchips(id, -chips)
                clickcount += 1
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    TextSurf, TextRect = text_objects(msg, font)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(TextSurf, TextRect)


class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()

    def blackjack(self):
        self.dealer.calc_hand()
        self.player.calc_hand()
        show_dealer_card = pygame.image.load('card/' + self.dealer.card_img[1] + '.png').convert()
        if self.player.value == 21 and self.dealer.value == 21:
            gameDisplay.blit(show_dealer_card, (550, 200))
            black_jack("Both BlackJack!", 500, 250, grey)
            socket.addchips(id, chips)
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value == 21:
            gameDisplay.blit(show_dealer_card, (550, 200))
            black_jack("You got BlackJack!", 500, 250, green)
            socket.addchips(id, chips * 2)
            time.sleep(4)
            self.play_or_exit()
        elif self.dealer.value == 21:
            gameDisplay.blit(show_dealer_card, (550, 200))
            black_jack("Dealer has BlackJack!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()

        self.player.value = 0
        self.dealer.value = 0

    def deal(self):
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1
        dealer_card = pygame.image.load('card/' + self.dealer.card_img[0] + '.png').convert()
        dealer_card_2 = pygame.image.load('card/back.png')
        dealer_card_2 = pygame.transform.scale(dealer_card_2, (int(100), int(150))).convert()

        player_card = pygame.image.load('card/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load('card/' + self.player.card_img[1] + '.png').convert()

        game_texts("Dealer's hand:", 500, 150)

        gameDisplay.blit(dealer_card, (400, 200))
        gameDisplay.blit(dealer_card_2, (550, 200))

        game_texts("Your hand:", 500, 400)

        gameDisplay.blit(player_card, (300, 450))
        gameDisplay.blit(player_card_2, (410, 450))
        self.blackjack()

    def hit(self):
        self.player.add_card(self.deck.deal())
        self.blackjack()
        self.player_card += 1

        if self.player_card == 2:
            self.player.calc_hand()
            self.player.display_cards()
            player_card_3 = pygame.image.load('card/' + self.player.card_img[2] + '.png').convert()
            gameDisplay.blit(player_card_3, (520, 450))

        if self.player_card == 3:
            self.player.calc_hand()
            self.player.display_cards()
            player_card_4 = pygame.image.load('card/' + self.player.card_img[3] + '.png').convert()
            gameDisplay.blit(player_card_4, (630, 450))

        if self.player.value > 21:
            show_dealer_card = pygame.image.load('card/' + self.dealer.card_img[1] + '.png').convert()
            gameDisplay.blit(show_dealer_card, (550, 200))
            game_finish("You LOOSE", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()

        self.player.value = 0

        if self.player_card > 4:
            sys.exit()

    def stand(self):
        show_dealer_card = pygame.image.load('card/' + self.dealer.card_img[1] + '.png').convert()
        gameDisplay.blit(show_dealer_card, (550, 200))
        self.blackjack()
        self.dealer.calc_hand()
        self.player.calc_hand()
        if self.player.value > self.dealer.value:
            game_finish("You Won!", 500, 250, green)
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value < self.dealer.value:
            game_finish("Dealer Wins!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()
        else:
            game_finish("It's a Tie!", 500, 250, grey)
            time.sleep(4)
            self.play_or_exit()

    def play_or_exit(self):
        game_texts("Play again press Deal!", 200, 80)
        time.sleep(3)
        self.player.value = 0
        self.dealer.value = 0
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        gameDisplay.fill(background_color)
        pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
        pygame.display.update()


def render(id1, chips1, socket1):
    global gameDisplay
    global id
    global chips
    global socket
    global clickcount
    id = id1
    chips = int(chips1)
    socket = socket1
    clock = pygame.time.Clock()
    clickcount = 0

    gameDisplay = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption('BlackJack')
    gameDisplay.fill(background_color)
    pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
    play_blackjack = Play()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            button("Deal", 30, 100, 150, 50, light_slat, dark_slat, play_blackjack.deal)
            button("Hit", 30, 200, 150, 50, light_slat, dark_slat, play_blackjack.hit)
            button("Stand", 30, 300, 150, 50, light_slat, dark_slat, play_blackjack.stand)

        pygame.display.flip()
