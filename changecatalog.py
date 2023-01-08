from casinosocket import socketprocessor
import pygame as pg
import time

COLOR_INACTIVE = (255, 255, 255)
COLOR_ACTIVE = (50, 50, 250)
FONT = pg.font.Font(None, 32)
BTNFONT = pg.font.Font(None, 24)



class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.downcount = 0
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
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
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, w, h, type, boxes, socket):
        self.rect = pg.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.boxes = boxes
        self.type = type
        self.txt_surface = BTNFONT.render(type, True, COLOR_ACTIVE)
        self.active = False
        self.done = False
        self.profile = ()
        self.socket = socket

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                    if self.type == 'login':
                        self.socket.setlogin(self.boxes.text)
                        self.done = True
                    elif self.type == 'password':
                        self.socket.setpassword(self.boxes.text)


    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


class changecatalog:
    def __init__(self, table, id, socket):
        pg.init()

        self.screen = pg.display.set_mode((384, 135))
        self.socket = socket
        self.id = id
        self.table = table

    def render(self):
        if self.table == 'login':
            pg.display.set_caption("Смена логина")
            input_box1 = InputBox(10, 10, 14, 32, 'login')
        else:
            pg.display.set_caption('Смена пароля')
            input_box1 = InputBox(10, 10, 14, 32, 'password')

        logo = pg.image.load('logopic.jpg').convert()
        pg.display.set_icon(logo)
        input_boxes = [input_box1]
        buttons = [Button(220, 10, 56, 56, self.table, input_box1, self.socket)]
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    break
                for box in input_boxes:
                    box.handle_event(event)
                for btn in buttons:
                    btn.handle_event(event)
                    if btn.done:
                        done = True

            if not done:
                for box in input_boxes:
                    box.update()

                self.screen.fill((10, 10, 30))
                for box in input_boxes:
                    box.draw(self.screen)
                for btn in buttons:
                    btn.draw(self.screen)

                pg.display.flip()
        pg.quit()
