import pyxel
import random
from entities.bullet import Bullet
from config import SCREEN_WIDTH, BULLET_WIDTH

ENEMY_WIDTH = 12
ENEMY_HEIGHT = 11
ENEMY_SPEED = 0.5
DESCENT_AMOUNT = 30
ENEMY_SHOT_INTERVAL = 120  

class StrongEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = ENEMY_SPEED
        self.bullets = []
        self.last_shot_frame = pyxel.frame_count + random.randint(0, 60)

    def update(self):
        self.x += self.dx
        if self.x <= 0 or self.x + ENEMY_WIDTH >= SCREEN_WIDTH:
            self.dx *= -1
            self.y += DESCENT_AMOUNT

        # 弾の発射
        if pyxel.frame_count - self.last_shot_frame >= ENEMY_SHOT_INTERVAL:
            bullet_x = self.x + ENEMY_WIDTH // 2 - BULLET_WIDTH // 2
            bullet_y = self.y + ENEMY_HEIGHT
            self.bullets.append(Bullet(bullet_x, bullet_y, dy=2, color=3))  
            self.last_shot_frame = pyxel.frame_count

        # 弾の更新・削除
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y > pyxel.height:
                self.bullets.remove(bullet)

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

        for bullet in self.bullets:
            bullet.draw()
