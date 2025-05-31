import pyxel
from config import BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED

class Bullet:
    def __init__(self, x, y, dy=-BULLET_SPEED):
        self.x = x
        self.y = y
        self.dy = dy  # 弾の進行方向（上：負、下：正）
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT

    def update(self):
        self.y += self.dy  # 上下どちらにも対応

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 7)
