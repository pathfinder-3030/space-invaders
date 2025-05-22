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
# グローバル変数
# ----------------------------
playerX = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
playerY = SCREEN_HEIGHT - PLAYER_HEIGHT - 5
bullet = None

# ----------------------------
# 効果音（必要に応じて）
# ----------------------------
def init_sounds():
    pyxel.sound(0).set("c3", "p", "6", "n", 10)

# ----------------------------
# 更新処理
# ----------------------------
def update():
    global playerX, bullet

    speed = 2
    if pyxel.btn(pyxel.KEY_LEFT):
        playerX = max(0, playerX - speed)
    if pyxel.btn(pyxel.KEY_RIGHT):
        playerX = min(SCREEN_WIDTH - PLAYER_WIDTH, playerX + speed)

    if pyxel.btnp(pyxel.KEY_SPACE) and bullet is None:
        bullet = [playerX + PLAYER_WIDTH // 2, playerY]
        pyxel.play(0, 0)

    if bullet is not None:
        bullet[1] -= BULLET_SPEED
        if bullet[1] + BULLET_HEIGHT < 0:
            bullet = None

# ----------------------------
# 描画処理
# ----------------------------
def draw():
    pyxel.cls(0)
    pyxel.blt(playerX, playerY, 0, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
    if bullet is not None:
        pyxel.rect(bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT, 7)

# ----------------------------
# 起動
# ----------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Invader Core")
pyxel.load("invader_game.pyxres")
init_sounds()
pyxel.run(update, draw)
