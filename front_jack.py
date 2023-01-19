import pygame as pygame
from blago_black import *
from const import *
import sys
import time



###text object render

class Play:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()


    def blackjack(self):

        self.dealer.calc_hand()
        self.player.calc_hand()

        show_dealer_card = pygame.image.load('card/' + self.dealer.card_img[1] + '.png').convert()

        if self.player.value == 21 and self.dealer.value == 21:
            self.gameDisplay.blit(show_dealer_card, (550, 200))
            self.black_jack("Both BlackJack!", 500, 250, grey)
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value == 21:
            self.gameDisplay.blit(show_dealer_card, (550, 200))
            self.black_jack("You got BlackJack!", 500, 250, green)
            time.sleep(4)
            self.play_or_exit()
        elif self.dealer.value == 21:
            self.gameDisplay.blit(show_dealer_card, (550, 200))
            self.black_jack("Dealer has BlackJack!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()

        self.player.value = 0
        self.dealer.value = 0

    def text_objects(self, text, font):
        textSurface = pygame.font.SysFont("Arial", 20).render(text, True, black)
        print('r_t_o')
        return textSurface, textSurface.get_rect()

    def end_text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    # game text display
    def game_texts(self, text, x, y):
        TextSurf, TextRect = self.text_objects(text, pygame.font.SysFont('Comic Sans MS', 35))
        TextRect.center = (x, y)
        self.gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()

    def game_finish(self, text, x, y, color):
        TextSurf, TextRect = self.end_text_objects(text, pygame.font.SysFont('dejavusans', 100), color)
        TextRect.center = (x, y)
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()

    def black_jack(self, text, x, y, color):
        TextSurf, TextRect = self.end_text_objects(text, pygame.font.SysFont('roboto', 70), color)
        TextRect.center = (x, y)
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()

    # button display
    def button(self, msg, x, y, w, h, ic, ac, action=None):
        print(777)
        mouse = pygame.mouse.get_pos()
        print(888)
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))
            if click[0] == 1:
                print(action)
                action()
        else:
            print('2')
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))
        print(msg)
        TextSurf, TextRect = self.text_objects(msg, pygame.font.SysFont("Arial", 20))
        TextRect.center = ((x + (w / 2)), (y + (h / 2)))
        print(131313131313)
        self.gameDisplay.blit(TextSurf, TextRect)

    def deal(self):
        self.ismain = 1
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1
        dealer_card = pygame.image.load('card/' + self.dealer.card_img[0] + '.png').convert()
        dealer_card_2 = pygame.image.load('card/back.png').convert()

        player_card = pygame.image.load('card/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load('card/' + self.player.card_img[1] + '.png').convert()

        self.game_texts("Dealer's hand:", 500, 150)

        self.gameDisplay.blit(dealer_card, (400, 200))
        self.gameDisplay.blit(dealer_card_2, (600, 100))

        self.game_texts("Your hand:", 500, 400)

        self.gameDisplay.blit(player_card, (300, 450))
        self.gameDisplay.blit(player_card_2, (410, 450))
        self.blackjack()

    def hit(self):
        self.player.add_card(self.deck.deal())
        self.blackjack()
        self.player_card += 1

        if self.player_card == 2:
            self.player.calc_hand()
            self.player.display_cards()
            player_card_3 = pygame.image.load('card/' + self.player.card_img[2] + '.png').convert()
            self.gameDisplay.blit(player_card_3, (520, 450))

        if self.player_card == 3:
            self.player.calc_hand()
            self.player.display_cards()
            player_card_4 = pygame.image.load('card/' + self.player.card_img[3] + '.png').convert()
            self.gameDisplay.blit(player_card_4, (630, 450))

        if self.player.value > 21:
            show_dealer_card = pygame.image.load('card/' + self.dealer.card_img[1] + '.png').convert()
            self.gameDisplay.blit(show_dealer_card, (550, 200))
            self.game_finish("You LOOSE", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()

        self.player.value = 0

        if self.player_card > 4:
            sys.exit()

    def stand(self):
        show_dealer_card = pygame.image.load('card/' + self.dealer.card_img[1] + '.png').convert()
        self.gameDisplay.blit(show_dealer_card, (550, 200))
        self.blackjack()
        self.dealer.calc_hand()
        self.player.calc_hand()
        if self.player.value > self.dealer.value:
            self.game_finish("You Won!", 500, 250, green)
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value < self.dealer.value:
            self.game_finish("Dealer Wins!", 500, 250, red)
            time.sleep(4)
            self.play_or_exit()
        else:
            self.game_finish("It's a Tie!", 500, 250, grey)
            time.sleep(4)
            self.play_or_exit()

    def exit(self):
        sys.exit()

    def play_or_exit(self):
        self.game_texts("Play again press Deal!", 200, 80)
        time.sleep(3)
        self.player.value = 0
        self.dealer.value = 0
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.gameDisplay.fill(background_color)
        pygame.draw.rect(self.gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
        pygame.display.update()


    def render(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        print(1, self.gameDisplay)
        pygame.display.set_caption('BlackJack')

        self.run = True

        ismain = 0
        while self.run:
            print(self.gameDisplay)
            self.clock.tick(2)

            if ismain == 0:
                ismain = 1
                self.gameDisplay.fill(background_color)
            pygame.draw.rect(self.gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
            self.button("Deal", 30, 100, 150, 50, light_slat, dark_slat, self.deal)
            self.button("Hit", 30, 200, 150, 50, light_slat, dark_slat, self.hit)
            self.button("Stand", 30, 300, 150, 50, light_slat, dark_slat, self.stand)
            self.button("EXIT", 30, 500, 150, 50, light_slat, dark_red, self.exit)
            pygame.display.update()

            pygame.display.flip()
        pygame.display.quit()


