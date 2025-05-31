import pyxel
from config import SCREEN_WIDTH

# スプライト情報（必要に応じて config.py に移してもOK）
ENEMY_WIDTH = 12
ENEMY_HEIGHT = 11
SPRITE_ENEMY_U = 34
SPRITE_ENEMY_V = 3
ENEMY_SPEED = 0.5
DESCENT_AMOUNT = 30

class BasicEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = ENEMY_SPEED  # x方向の速度

    def update(self):
        self.x += self.dx

        # 端にあたったら方向を反転し、y方向に進める
        if self.x <= 0 or self.x + ENEMY_WIDTH >= SCREEN_WIDTH:
            self.dx *= -1
            self.y += DESCENT_AMOUNT

    def draw(self):
        pyxel.blt(
            self.x, self.y,
            img=0,
            u=SPRITE_ENEMY_U, 
            v=SPRITE_ENEMY_V,
            w=ENEMY_WIDTH, 
            h=ENEMY_HEIGHT,
            colkey=0
        )

    def is_hit_by(self, bullet):
        return (
        self.x < bullet.x + bullet.w and
        self.x + ENEMY_WIDTH > bullet.x and
        self.y < bullet.y + bullet.h and
        self.y + ENEMY_HEIGHT > bullet.y
    )
