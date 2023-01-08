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
        self.done = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        wcolor = pygame.Color("white")
        for i in range(self.height):
            for j in range(self.width):
                gameicon = None
                if self.board[i][j] == 3:
                    gameicon = pygame.image.load('cash.jpg').convert()
                if self.board[i][j] == 4:
                    gameicon = pygame.image.load('bomb.jpg').convert()
                if gameicon != None:
                    gameicon.set_colorkey((255, 255, 255))
                    pygame.draw.rect(surface, wcolor, (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                       self.cell_size, self.cell_size),
                                     1)

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
                pygame.draw.rect(surface, wcolor, (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                   self.cell_size, self.cell_size),
                                 1)

        # wcolor = pygame.Color("white")
        # for i in range(self.height):
        #     for j in range(self.width):
        #         gameicon = None
        #
        #         if gameicon != None:
        #             gameicon.set_colorkey((255, 255, 255))
        #             obj_rect = gameicon.get_rect(
        #                 center=(self.left + self.cell_size * j + self.cell_size // 2,
        #                         self.top + self.cell_size * i + self.cell_size // 2))
        #             pygame.display.update()
        #             scale = pygame.transform.scale(
        #                 gameicon, (self.cell_size, self.cell_size))
        #
        #             scale_rect = scale.get_rect(
        #                 center=(self.left + self.cell_size * j + self.cell_size // 2,
        #                         self.top + self.cell_size * i + self.cell_size // 2))
        #
        #             self.screen.blit(scale, scale_rect)

#        self.board = [[0] * width for _ in range(height)]
    def on_click(self, cords):
        cell = (cords[0] // self.cell_size - self.top // self.cell_size,
               cords[1] // self.cell_size - self.top // self.cell_size) if 0 <= cords[
            0] // self.cell_size - self.top // self.cell_size < self.width and 0 <= cords[
                                                                               1] // self.cell_size - self.top // \
                                                                           self.cell_size < \
                                                                           self.height else None
        if cell != None and self.done == False:
            self.board[cell[1]][cell[0]] = 3 if self.board[cell[1]][cell[0]] == 0 else 4 if self.board[cell[1]][cell[0]] == 1 else self.board[cell[1]][cell[0]]
            if self.board[cell[1]][cell[0]] == 4:
                self.done = True


class fieldwindow:
    def __init__(self, id, bet, totalchips, socket):
        self.socket = socket
        self.id = id
        self.bet = bet
        self.totalchips = totalchips
        pygame.init()

    def render(self):
        pygame.init()
        size = 600, 800
        h = 3
        w = 4
        screen = pygame.display.set_mode(size)
        generated = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        random.shuffle(generated)
        generated = [[generated[h * i + j] for j in range(h)] for i in range(w)]
        print(generated)
        board = Board(3, 4, generated, screen, 1, 1)
        board.set_view(0, 0, 200)
        running = True
        itt = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if itt == 0:
                    itt = 1
                    screen.fill((0, 0, 0))
                    board.render(screen)
                    pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.on_click(event.pos)
                    itt = 0
        pygame.quit()



