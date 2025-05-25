import pyxel
from entities.player import Player
from entities.enemy import BasicEnemy
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT

# ----------------------------
# 効果音初期化
# ----------------------------
def init_sounds():
    pyxel.sound(0).set("c3", "p", "6", "n", 10)

# ----------------------------
# ゲーム全体の更新
# ----------------------------
def update():
    player.update()
    for enemy in basic_enemies:
        enemy.update()

# ----------------------------
# ゲーム全体の描画
# ----------------------------
def draw():
    pyxel.cls(0)
    player.draw()
    for enemy in basic_enemies:
        enemy.draw()

# ----------------------------
# 起動処理
# ----------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="インベーダーゲーム")
pyxel.load("invader_game.pyxres")
init_sounds()

player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 5)

# 複数の敵を横に並べて生成
basic_enemies = []
for i in range(5):
    x = i * 16
    y = 0
    basic_enemies.append(BasicEnemy(x, y))

pyxel.run(update, draw)
