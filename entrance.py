import pygame as pg
import casinosocket
from mainwindow import mainwindow

pg.init()
screen = pg.display.set_mode((384, 135))
COLOR_INACTIVE = (255, 255, 255)
COLOR_ACTIVE = (50, 50, 250)
FONT = pg.font.Font(None, 32)
BTNFONT = pg.font.Font(None, 24)

class Button:
    def __init__(self, x, y, w, h, type, boxes):
        self.rect = pg.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.boxes = boxes
        self.type = type
        self.txt_surface = BTNFONT.render(type, True, COLOR_ACTIVE)
        self.active = False
        self.done = False
        self.profile = ()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if all(list(map(lambda x: 1 if len(x.text) > 0 and x.text != 'login' and x.text != 'password' and x.text != 'server ip' else 0, self.boxes))):
                    socket = casinosocket.socketprocessor(self.boxes[2].text)
                    if self.type == 'reg':
                        socket.registration(self.boxes[0], self.boxes[1])
                        self.profile = (socket.getid(self.boxes[0].text, self.boxes[1].text).decode('utf-8'), socket.getprofile(socket.getid(self.boxes[0].text, self.boxes[1].text).decode('utf-8')))
                        self.done = True
                    elif self.type == 'log in':
                        self.profile = (socket.getid(self.boxes[0].text, self.boxes[1].text).decode('utf-8'), socket.getprofile(socket.getid(self.boxes[0].text, self.boxes[1].text).decode('utf-8')))
                        print(self.profile)
                        self.done = True

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class InputBox:
    def __init__(self, x, y, w, h, text=''):
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

class entrance:
    def render(self):
        pg.display.set_caption("Вход/Регистрация")
        clock = pg.time.Clock()
        input_box1 = InputBox(10, 10, 14, 32, 'login')
        input_box2 = InputBox(10, 50, 14, 32, 'password')
        input_box3 = InputBox(10, 90, 14, 32, 'server ip')
        input_boxes = [input_box1, input_box2, input_box3]
        buttons = [Button(220, 10, 56, 56, 'log in', input_boxes), Button(220, 66, 56, 56, 'reg', input_boxes)]
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                for box in input_boxes:
                    box.handle_event(event)
                for btn in buttons:
                    btn.handle_event(event)
                    if btn.done:
                        pg.quit()
                        window = mainwindow(btn.profile[0], btn.profile[1].decode('utf-8').split('|')[1], btn.profile[1].decode('utf-8').split('|')[2], btn.profile[1].decode('utf-8').split('|')[1])
                        done = True



            if not done:
                for box in input_boxes:
                    box.update()

                screen.fill((10, 10, 30))
                for box in input_boxes:
                    box.draw(screen)
                for btn in buttons:
                    btn.draw(screen)

                pg.display.flip()
                clock.tick(30)




ex = entrance()
ex.render()