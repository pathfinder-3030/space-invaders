import pyxel
from config import SCREEN_WIDTH

ENEMY_WIDTH = 16
ENEMY_HEIGHT = 12
ENEMY_SPEED = 0.5
DESCENT_AMOUNT = 11

class StrongEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = ENEMY_SPEED

    def update(self):
        self.x += self.dx
        if self.x <= 0 or self.x + ENEMY_WIDTH >= SCREEN_WIDTH:
            self.dx *= -1
            self.y += DESCENT_AMOUNT

    def is_hit_by(self, bullet):
        return (
            self.x < bullet.x + bullet.w and
            self.x + ENEMY_WIDTH > bullet.x and
            self.y < bullet.y + bullet.h and
            self.y + ENEMY_HEIGHT > bullet.y
        )

    def draw(self):
        pyxel.blt(
            self.x, self.y,
            img=0,
            u=48,  # スプライトX座標（見た目だけ変更）
            v=1,   # スプライトY座標
            w=ENEMY_WIDTH,
            h=ENEMY_HEIGHT,
            colkey=0
        )
