import pyxel
from config import SCREEN_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullet = None
        self.direction = "neutral"  # "left", "right", "neutral"

    def update(self):
        speed = 2
        self.direction = "neutral"

        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(0, self.x - speed)
            self.direction = "left"

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(SCREEN_WIDTH - PLAYER_WIDTH, self.x + speed)
            self.direction = "right"

        if pyxel.btnp(pyxel.KEY_SPACE) and self.bullet is None:
            self.bullet = [self.x + PLAYER_WIDTH // 2, self.y]
            pyxel.play(0, 0)

        if self.bullet is not None:
            self.bullet[1] -= BULLET_SPEED
            if self.bullet[1] + BULLET_HEIGHT < 0:
                self.bullet = None

    def draw(self):
        if self.direction == "right":
            pyxel.blt(self.x, self.y, 0, 0, 16, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
        elif self.direction == "left":
            pyxel.blt(self.x, self.y, 0, 0, 32, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 0)

        if self.bullet is not None:
            pyxel.rect(self.bullet[0], self.bullet[1], BULLET_WIDTH, BULLET_HEIGHT, 7)
