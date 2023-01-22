import pygame
import random

COLOR_INACTIVE = (255, 255, 255)
COLOR_ACTIVE = (50, 50, 250)



class Button:
    def __init__(self, x, y, w, h, type, boxes, id, socket):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.boxes = boxes
        self.type = type
        self.txt_surface = pygame.font.Font(None, 24).render(type, True, COLOR_ACTIVE)
        self.active = False
        self.done = False
        self.profile = ()
        self.socket = socket
        self.id = id

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                    if self.type == 'regenerate':
                        self.socket.addchips(self.id, self.boxes[0].text[12:])
                        self.done = True



    def draw(self, screen):
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class labelbox:
    def __init__(self, x, y, w, h, text='Ваш выигрыш: 0'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)

    def handle_event(self, chips):
        self.txt_surface = pygame.font.Font(None, 32).render('Ваш выигрыш: ' + str(int(chips)), True, self.color)
        self.text = 'Ваш выигрыш: ' + str(int(chips))


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
    def __init__(self, width, height, board, screen, bet, id, label, socket):
        self.width = width
        self.bet = bet // 2
        self.label = label
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
        self.cashcells = 0

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
                    gameicon = pygame.image.load('pic/pictures/cash.jpg').convert()
                if self.board[i][j] == 4:
                    gameicon = pygame.image.load('pic/pictures/bomb.jpg').convert()
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
            self.board[cell[1]][cell[0]] = 4 if self.board[cell[1]][cell[0]] == 0 else 3 if self.board[cell[1]][cell[0]] == 1 else self.board[cell[1]][cell[0]]
            if self.board[cell[1]][cell[0]] == 4:
                self.done = True
                self.bet = 0
                self.label.handle_event(0)
                pygame.mixer.music.load("sounds/death.mp3")
                pygame.mixer.music.play(0)



            else:
                self.cashcells += 1
                pygame.mixer.music.load("sounds/congrats.mp3")
                pygame.mixer.music.play(0)

                self.label.handle_event(int(self.label.text[12:]) + self.bet)
                self.bet *= 2
                if self.cashcells == 5:
                    self.done = True
                    pygame.mixer.music.load("sounds/winfield.mp3")
                    pygame.mixer.music.play(0)


class fieldwindow:
    def __init__(self, id, bet, socket):
        self.socket = socket
        self.socket.addchips(id, -bet)
        self.id = id
        self.bet = bet
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
        running = True
        itt = 0
        self.run = True
        self.input_box = labelbox(0, 805, 450, 50)
        input_boxes = [self.input_box]
        buttons = [Button(500, 805, 100, 100, 'regenerate', input_boxes, self.id, self.socket)]
        board = Board(3, 4, generated, screen, self.bet, self.id, self.input_box, self.socket)
        board.set_view(0, 0, 200)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.socket.addchips(self.id, int(self.input_box.text[12:]))
                    running = False
                    break
                if itt == 0:
                    itt = 1
                    screen.fill((0, 0, 0))
                    board.render(screen)
                    for btn in buttons:
                        btn.handle_event(event)
                        if btn.done:
                            self.run = False
                            running = False
                            break
                    if self.run:
                        for box in input_boxes:
                            box.update()

                        for box in input_boxes:
                            box.draw(screen)
                        for btn in buttons:
                            btn.draw(screen)

                    pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.on_click(event.pos)
                    itt = 0
                for btn in buttons:
                    btn.handle_event(event)
                    if btn.done:
                        self.run = False


        if not self.run:
            pygame.quit()
            self.render()

        pygame.quit()



