import pyxel
from config import SCREEN_WIDTH

ENEMY_WIDTH = 12
ENEMY_HEIGHT = 11
ENEMY_SPEED = 0.2
DESCENT_AMOUNT = 30

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
            u=50,  
            v=2,   
            w=ENEMY_WIDTH,
            h=ENEMY_HEIGHT,
            colkey=0
        )
