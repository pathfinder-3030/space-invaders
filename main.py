import pyxel

# ----------------------------
# 各種設定
# ----------------------------
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16

BULLET_WIDTH = 1
BULLET_HEIGHT = 4
BULLET_SPEED = 4

# ----------------------------
# プレイヤークラス
# ----------------------------
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullet = None
        self.direction = "neutral"  # "left", "right", "neutral"

    def player_update(self):
        speed = 2
        self.direction = "neutral"  # 毎フレーム初期化

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

    def player_draw(self):
        if self.direction == "right":
            pyxel.blt(self.x, self.y, 0, 0, 16, PLAYER_WIDTH, PLAYER_HEIGHT, 0)

        if self.direction == "left":
            pyxel.blt(self.x, self.y, 0, 0, 32, PLAYER_WIDTH, PLAYER_HEIGHT, 0)

        if self.direction == "neutral":
            pyxel.blt(self.x, self.y, 0, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 0)

        if self.bullet is not None:
            pyxel.rect(self.bullet[0], self.bullet[1], BULLET_WIDTH, BULLET_HEIGHT, 7)

# ----------------------------
# 効果音初期化
# ----------------------------
def init_sounds():
    pyxel.sound(0).set("c3", "p", "6", "n", 10)

# ----------------------------
# ゲーム全体の初期化
# ----------------------------
def update():
    player.player_update()

def draw():
    pyxel.cls(0)
    player.player_draw()

# ----------------------------
# 起動処理
# ----------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Invader with Class")
pyxel.load("invader_game.pyxres")
init_sounds()
player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 5)
pyxel.run(update, draw)
