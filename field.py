import pygame
import random

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.downcount = 0
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                if self.downcount == 0:
                    self.text = ''
                    self.downcount += 1
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

class labelbox:
    def __init__(self, x, y, w, h, text='Balance: ----р.'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
    def handle_event(self, chips):
        if chips.isnumeric():
            self.txt_surface = pygame.font.Font(None, 32).render('Balance: ' + str(int(chips) * 10) + 'р.', True, self.color)
        else:
            self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)


    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

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
        size = 600, 900
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



