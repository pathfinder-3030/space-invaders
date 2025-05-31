import pyxel
from entities.bullet import Bullet
from config import SCREEN_WIDTH, PLAYER_WIDTH, BULLET_WIDTH, BULLET_HEIGHT, PLAYER_HEIGHT, BULLET_SPEED

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []  # 自機の弾リスト
        self.direction = "neutral"
        self.last_shot_frame = -30  # 初期フレームで発射可能にする

    def update(self):
        speed = 2
        self.direction = "neutral"

        # 移動処理
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(0, self.x - speed)
            self.direction = "left"

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(SCREEN_WIDTH - PLAYER_WIDTH, self.x + speed)
            self.direction = "right"

        # 弾発射（毎秒1回）
        if pyxel.btn(pyxel.KEY_SPACE):
            current_frame = pyxel.frame_count
            if current_frame - self.last_shot_frame >= 30:
                bullet_x = self.x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2
                bullet_y = self.y
                self.bullets.append(Bullet(bullet_x, bullet_y, dy=-BULLET_SPEED))  # 上方向
                pyxel.play(0, 0)
                self.last_shot_frame = current_frame

        # 弾の更新と削除
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y + BULLET_HEIGHT < 0:
                self.bullets.remove(bullet)

    def draw(self):
        # 自機の描画（向きでスプライト切り替え）
        if self.direction == "right":
            pyxel.blt(self.x, self.y, 0, 0, 16, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
        elif self.direction == "left":
            pyxel.blt(self.x, self.y, 0, 0, 32, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 0)

        # 弾の描画
        for bullet in self.bullets:
            bullet.draw()

    def is_hit_by(self, bullet):
        return (
            self.x < bullet.x + bullet.w and
            self.x + PLAYER_WIDTH > bullet.x and
            self.y < bullet.y + bullet.h and
            self.y + PLAYER_HEIGHT > bullet.y
        )
