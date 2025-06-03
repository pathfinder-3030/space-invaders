import pyxel
import random
from entities.bullet import Bullet
from config import SCREEN_WIDTH, BULLET_WIDTH, BULLET_HEIGHT

ENEMY_WIDTH = 12
ENEMY_HEIGHT = 11
ENEMY_SPEED = 0.5
DESCENT_AMOUNT = 30
ENEMY_SHOT_INTERVAL = 300 

class BossEnemy:
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

        # 特殊攻撃（3方向弾）
        if pyxel.frame_count - self.last_shot_frame >= ENEMY_SHOT_INTERVAL:
            center_x = self.x + ENEMY_WIDTH // 2 - BULLET_WIDTH // 2
            bullet_y = self.y + ENEMY_HEIGHT

            # 左・中央・右方向に弾を撃つ（dx, dyの組み合わせ）
            directions = [(-1, 2), (0, 2), (1, 2)]
            for dx, dy in directions:
                self.bullets.append(Bullet(center_x, bullet_y, dx=dx, dy=dy, color=8))

            self.last_shot_frame = pyxel.frame_count

        # 弾の更新・削除
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y > pyxel.height or bullet.x < 0 or bullet.x > pyxel.width:
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
            u=18,
            v=2,
            w=ENEMY_WIDTH,
            h=ENEMY_HEIGHT,
            colkey=0
        )

        for bullet in self.bullets:
            bullet.draw()
