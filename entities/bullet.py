import pyxel
from config import BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED

class Bullet:
    def __init__(self, x, y, dx=0, dy=-BULLET_SPEED, color=7):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.color = color  

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)
