import pyxel
from entities.player import Player
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT


# ----------------------------
# 効果音初期化
# ----------------------------
def init_sounds():
    pyxel.sound(0).set("c3", "p", "6", "n", 10)

# ----------------------------
# ゲーム全体の初期化
# ----------------------------
def update():
    player.update()

def draw():
    pyxel.cls(0)
    player.draw()

# ----------------------------
# 起動処理
# ----------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Invader with Class")
pyxel.load("invader_game.pyxres")
init_sounds()
player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 5)
pyxel.run(update, draw)
