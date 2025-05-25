import pyxel
from config import BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT

    def update(self):
        self.y -= BULLET_SPEED

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 7)
