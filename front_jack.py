import pygame as pygame
from blago_black import *
from const import *




#text object render



class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()

    def blackjack(self):
        pass

    def deal(self):
        pass

    def hit(self):
        pass



class Window:
    def __init__(self):
        pygame.init()

        clock = pygame.time.Clock()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))

        pygame.display.set_caption('BlackJack')
        self.gameDisplay.fill(background_color)
        pygame.draw.rect(self.gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
        self.play_blackjack = Play()
    def render(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.button("Deal", 30, 100, 150, 50, light_slat, dark_slat, self.play_blackjack.deal)
                self.button("Hit", 30, 200, 150, 50, light_slat, dark_slat, self.play_blackjack.hit)
                self.button("Stand", 30, 300, 150, 50, light_slat, dark_slat, self.play_blackjack)
                self.button("EXIT", 30, 500, 150, 50, light_slat, dark_red, self.play_blackjack)

            pygame.display.flip()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def end_text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    # game text display
    def game_texts(self, text, x, y):
        TextSurf, TextRect = self.text_objects(text, textfont)
        TextRect.center = (x, y)
        self.gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()

    def black_jack(self, text, x, y, color):
        TextSurf, TextRect = self.end_text_objects(text, blackjack, color)
        TextRect.center = (x, y)
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()

    # button display
    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))
            if click[0] == 1 != None:
                action()
        else:
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))

        TextSurf, TextRect = self.text_objects(msg, font)
        TextRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.gameDisplay.blit(TextSurf, TextRect)

