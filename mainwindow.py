import pygame
import casinosocket
from main import Game

class Board:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.screen = screen
        self.hide = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        wcolor = pygame.Color("white")
        for i in range(self.height):
            for j in range(self.width):
                if i == 0 and j == 0:
                    gameicon = pygame.image.load('slotsicon.jpg').convert()
                    gameicon.set_colorkey((255, 255, 255))
                    obj_rect = gameicon.get_rect(
                        center=(self.left + self.cell_size * j + self.cell_size // 2, self.top + self.cell_size * i + self.cell_size // 2))
                    pygame.display.update()
                    scale = pygame.transform.scale(
                        gameicon, (self.cell_size, self.cell_size))

                    scale_rect = scale.get_rect(
                        center=(self.left + self.cell_size * j + self.cell_size // 2, self.top + self.cell_size * i + self.cell_size // 2))

                    self.screen.blit(scale, scale_rect)
                else:
                    pygame.draw.rect(surface, wcolor,
                                 (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                  self.cell_size, self.cell_size), 1 if self.board[i][j] == 0 else 0)

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords is None:
            return

        self.on_click(cell_coords)

    def get_cell(self, mouse_pos):
        return (
            (mouse_pos[1] - self.left) // self.cell_size,
            (mouse_pos[0] - self.top) // self.cell_size) if self.left < \
                                                            mouse_pos[
                                                                0] < self.left + self.width * \
                                                            self.cell_size and self.top < \
                                                            mouse_pos[
                                                                1] < self.top + self.height * self.cell_size else None

    def on_click(self, cords):
        coords = (cords[0] // self.cell_size - self.top // self.cell_size,
        cords[1] // self.cell_size - self.top // self.cell_size if 0 <= cords[
        0] // self.cell_size - self.top // self.cell_size < self.width and 0 <= cords[
                                                                               1] // self.cell_size - self.top // \
                                                                           self.cell_size < \
                                                                     self.height else None)
        if coords == (0, 0):
            slotwindow = Game()
            slotwindow.run()
            self.hide = True



class mainwindow:
    def __init__(self, id, username, password, chips):
        self.id = id
        self.username = username
        self.password = password
        self.chips = chips
        pygame.init()

    def render(self):
        pygame.init()
        size = 1800, 800
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Queen of spades")
        logo = pygame.image.load('logopic.jpg').convert()
        pygame.display.set_icon(logo)
        board = Board(8, 3, screen)
        board.set_view(0, 0, 100)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.on_click(event.pos)
                    if board.hide:
                        pygame.display.quit()
                        running = False
                        break

                bgimage = pygame.image.load('mainbackground.png').convert()
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
            pygame.quit()
