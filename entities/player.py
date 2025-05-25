import pyxel
from entities.bullet import Bullet  
from config import SCREEN_WIDTH, PLAYER_WIDTH, BULLET_WIDTH, BULLET_HEIGHT, PLAYER_HEIGHT

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []  # 弾をリストで管理
        self.direction = "neutral"

    def update(self):
        speed = 2
        self.direction = "neutral"

        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(0, self.x - speed)
            self.direction = "left"

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(SCREEN_WIDTH - PLAYER_WIDTH, self.x + speed)
            self.direction = "right"

        if pyxel.btnp(pyxel.KEY_SPACE):
            bullet_x = self.x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2
            bullet_y = self.y
            self.bullets.append(Bullet(bullet_x, bullet_y))
            pyxel.play(0, 0)

        # 弾の更新と削除
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y + BULLET_HEIGHT < 0:
                self.bullets.remove(bullet)

    def draw(self):
        if self.direction == "right":
            pyxel.blt(self.x, self.y, 0, 0, 16, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
        elif self.direction == "left":
            pyxel.blt(self.x, self.y, 0, 0, 32, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 0)

        # 弾の描画
        for bullet in self.bullets:
            bullet.draw()
