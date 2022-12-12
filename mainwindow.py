import pygame as pg
import casinosocket

class mainwindow:
    def __init__(self, id, username, password, chips):
        self.id = id
        self.username = username
        self.password = password
        self.chips = chips
        pg.init()
        self.screen = pg.display.set_mode((384, 135))

    def render(self):
        pass
