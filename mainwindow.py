import pygame
from casinosocket import socketprocessor
from main import Game
import front_jack
import changecatalog
from field import fieldwindow

COLOR_INACTIVE = (255, 255, 255)
COLOR_ACTIVE = (50, 50, 250)

class labelbox:
    def __init__(self, x, y, w, h, text='Balance: ----р.'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
    def handle_event(self, chips):
        if chips.isnumeric():
            self.txt_surface = pygame.font.Font(None, 32).render('Balance: ' + str(chips) + 'р.', True, self.color)
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

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)



class Board:
    def __init__(self, width, height, screen, id, chips, socket):
        self.width = width
        self.chips = chips
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.screen = screen
        self.hide = False
        self.id = id
        self.socket = socket
        self.runninggame = None

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        wcolor = pygame.Color("white")
        for i in range(self.height):
            for j in range(self.width):
                gameicon = None
                if i == 0 and j == 0:
                    gameicon = pygame.image.load('slotsicon.jpg').convert()
                if i == 0 and j == 1:
                    gameicon = pygame.image.load('poker.png').convert()
                if i == 4 and j == 0:
                    gameicon = pygame.image.load('changelogin.png').convert()
                if i == 4 and j == 1:
                    gameicon = pygame.image.load('changepassword.png').convert()
                if i == 0 and j == 2:
                    gameicon = pygame.image.load('cash.jpg').convert()
                if i == 4 and j == 2:
                    gameicon = pygame.image.load('buychips.jpg').convert()
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
            self.runninggame = Game()
            self.hide = True
        elif coords == (1, 0):
            self.runninggame = front_jack.Play()
            self.hide = True
        elif coords == (2, 0):
            self.runninggame = fieldwindow(self.id, self.chips, self.socket)
            self.hide = True
        elif coords == (0, 4):
            self.runninggame = changecatalog.changecatalog('login', self.id, self.socket)
            self.hide = True

        elif coords == (1, 4):
            self.runninggame = changecatalog.changecatalog('password', self.id, self.socket)
            self.hide = True

        elif coords == (2, 4):
            self.runninggame = changecatalog.chips(self.id, self.socket)
            self.hide = True



class mainwindow:
    def __init__(self, id, username, password, chips, socket):
        self.socket = socket
        self.id = id
        self.username = username
        self.password = password
        self.chips = chips
        pygame.init()

    def render(self):
        pygame.init()
        #1800 800 if desktop
        #800 400 if laptop
        size = 1800, 800
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Queen of spades")
        logo = pygame.image.load('logopic.jpg').convert()
        pygame.display.set_icon(logo)
        board = Board(8, 5, screen, self.id, 0, self.socket)
        # 0, 0, 100 if desktop 0, 0, 20 if laptop
        board.set_view(0, 0, 100)
        running = True
        bgimage = pygame.image.load('mainbackground.png').convert()
        itt = 0
        input_box = InputBox(0, 700, 24, 60, 'chips count')
        label_box = labelbox(300, 700, 24, 60)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.socket.ext()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.on_click(event.pos)
                    if board.hide:
                        running = False
                        break
                input_box.handle_event(event)
            if not running:
                break
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
            print(2)
            board.render(screen)
            print(1)
            label_box.handle_event(self.socket.getchips(self.id))
            print(self.socket.getchips(self.id))
            label_box.update()
            input_box.update()
            label_box.draw(screen)
            input_box.draw(screen)
            board.chips = int(input_box.text) if input_box.text.isnumeric() else 0

            pygame.display.flip()
            clock.tick(120)


        if not running and board.hide:
            pygame.display.quit()
            board.runninggame.render()
            board.hide = False
            self.render()
        else:
            self.socket.ext()
            pygame.quit()
