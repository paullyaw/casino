import pygame
import random

class Board:
    def __init__(self, width, height, board, screen, id, socket):
        self.width = width
        self.height = height
        self.board = board
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.screen = screen
        self.hide = False
        self.id = id
        self.socket = socket

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        wcolor = pygame.Color("white")
        for i in range(self.height):
            for j in range(self.width):
                gameicon = None

                if gameicon != None:
                    gameicon.set_colorkey((255, 255, 255))
                    obj_rect = gameicon.get_rect(
                        center=(self.left + self.cell_size * j + self.cell_size // 2,
                                self.top + self.cell_size * i + self.cell_size // 2))
                    pygame.display.update()
                    scale = pygame.transform.scale(
                        gameicon, (self.cell_size, self.cell_size))

                    scale_rect = scale.get_rect(
                        center=(self.left + self.cell_size * j + self.cell_size // 2,
                                self.top + self.cell_size * i + self.cell_size // 2))

                    self.screen.blit(scale, scale_rect)

#        self.board = [[0] * width for _ in range(height)]

class fieldwindow:
    def __init__(self, id, bet, totalchips, socket):
        self.socket = socket
        self.id = id
        self.bet = bet
        self.totalchips = totalchips
        pygame.init()

    def render(self):
        pygame.init()
        #1800 800 if desktop
        #800 400 if laptop
        size = 1800, 800
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Queen of spades")
        logo = pygame.image.load('logopic.jpg').convert()
        pygame.display.set_icon(logo)
        board = Board(8, 5, screen, self.id, self.socket)
        # 0, 0, 100 if desktop 0, 0, 20 if laptop
        board.set_view(0, 0, 100)
        running = True
        bgimage = pygame.image.load('mainbackground.png').convert()
        itt = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.on_click(event.pos)
                    if board.hide:
                        running = False
                        pygame.quit()
                        break
                if itt == 0:
                    itt += 1
                    sprite = bgimage
                    sprite.set_colorkey((255, 255, 255))
                    obj_rect = sprite.get_rect()
                    pygame.display.update()
                    scale = pygame.transform.scale(
                        sprite, (sprite.get_width(),
                                 sprite.get_height()))

                    scale_rect = scale.get_rect()

                    screen.blit(scale, scale_rect)

                    pygame.display.update(obj_rect)
                    board.render(screen)



                pygame.display.flip()
        if running == False and board.hide == True:
            board.hide = False
            self.render()
        else:
            self.socket.ext()
            pygame.quit()
