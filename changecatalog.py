from casinosocket import socketprocessor
import pygame as pg
import time
pg.init()
COLOR_INACTIVE = (255, 255, 255)
COLOR_ACTIVE = (50, 50, 250)

class labelbox:
    def __init__(self, x, y, w, h, text='----р.'):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pg.font.Font(None, 32).render(text, True, self.color)
    def handle_event(self, chips):
        if chips.isnumeric():
            self.txt_surface = pg.font.Font(None, 32).render(str(int(chips) * 10) + 'р.', True, self.color)
        else:
            self.txt_surface = pg.font.Font(None, 32).render(self.text, True, self.color)


    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.downcount = 0
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = pg.font.Font(None, 32).render(text, True, self.color)
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
                self.txt_surface = pg.font.Font(None, 32).render(self.text, True, self.color)

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
    def __init__(self, x, y, w, h, type, boxes, id, socket):
        self.rect = pg.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.boxes = boxes
        self.type = type
        self.txt_surface = pg.font.Font(None, 24).render(type, True, COLOR_ACTIVE)
        self.active = False
        self.done = False
        self.profile = ()
        self.socket = socket
        self.id = id

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                    if self.type == 'login':
                        self.socket.setlogin(self.id, self.boxes.text)
                        self.done = True
                    elif self.type == 'password':
                        self.socket.setpassword(self.id, self.boxes.text)
                        self.done = True
                    elif self.type == 'add chips':
                        self.socket.addchips(self.id, self.boxes[0].text)
                        self.done = True
                    elif self.type == 'calculate':
                        self.boxes[2].handle_event(self.boxes[0].text)


    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


class chips:
    def __init__(self, id, socket):
        pg.init()

        self.socket = socket
        self.id = id


    def render(self):
        pg.init()
        self.screen = pg.display.set_mode((384, 135))
        pg.display.set_caption("Купить фишки")
        self.input_box1 = InputBox(10, 10, 14, 32, 'chips count')
        self.input_box2 = InputBox(10, 50, 14, 32, 'card number')
        self.input_box3 = labelbox(10, 90, 14, 32)
        logo = pg.image.load('logopic.jpg').convert()
        input_boxes = [self.input_box1, self.input_box2, self.input_box3]
        buttons = [Button(220, 10, 56, 56, 'add chips', input_boxes, self.id, self.socket), Button(220, 66, 56, 56, 'calculate', input_boxes, self.id, self.socket)]
        self.run = True

        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                    break
                for box in input_boxes[:-1]:
                    box.handle_event(event)
                for btn in buttons:
                    btn.handle_event(event)
                    if btn.done:
                        self.run = False

            if self.run:
                for box in input_boxes:
                    box.update()

                self.screen.fill((10, 10, 30))
                for box in input_boxes:
                    box.draw(self.screen)
                for btn in buttons:
                    btn.draw(self.screen)

                pg.display.flip()
        pg.display.quit()

class changecatalog:
    def __init__(self, table, id, socket):
        pg.init()

        self.socket = socket
        self.id = id
        self.table = table


    def render(self):
        print(1)
        pg.init()
        print(2)
        self.screen = pg.display.set_mode((384, 135))
        print(3)
        if self.table == 'login':
            pg.display.set_caption("Смена логина")
            self.input_box1 = InputBox(10, 10, 14, 32, 'login')
        else:
            pg.display.set_caption('Смена пароля')
            self.input_box1 = InputBox(10, 10, 14, 32, 'password')
        print(4)
        logo = pg.image.load('logopic.jpg').convert()
        input_boxes = [self.input_box1]
        buttons = [Button(220, 10, 56, 56, self.table, self.input_box1, self.id, self.socket)]
        self.run = True

        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                    break
                for box in input_boxes:
                    box.handle_event(event)
                for btn in buttons:
                    btn.handle_event(event)
                    if btn.done:
                        self.run = False

            if self.run:
                for box in input_boxes:
                    box.update()

                self.screen.fill((10, 10, 30))
                for box in input_boxes:
                    box.draw(self.screen)
                for btn in buttons:
                    btn.draw(self.screen)

                pg.display.flip()
        pg.display.quit()


