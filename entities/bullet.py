import pyxel
from config import BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED

class Bullet:
    def __init__(self, x, y, dy=-BULLET_SPEED, color=7):
        self.x = x
        self.y = y
        self.dy = dy
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.color = color  # 弾の色を保持

    def update(self):
        self.y += self.dy

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)
