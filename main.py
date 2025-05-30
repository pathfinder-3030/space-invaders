import pyxel
from entities.player import Player
from entities.basic_enemy import BasicEnemy
from entities.strong_enemy import StrongEnemy
from entities.boss_enemy import BossEnemy
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

    # 通常敵の更新と衝突処理
    for enemy in basic_enemies[:]:
        enemy.update()
        for bullet in player.bullets[:]:
            if enemy.is_hit_by(bullet):
                basic_enemies.remove(enemy)
                player.bullets.remove(bullet)
                break

    # 強敵の更新と衝突処理
    for enemy in strong_enemies[:]:
        enemy.update()
        for bullet in player.bullets[:]:
            if enemy.is_hit_by(bullet):
                strong_enemies.remove(enemy)
                player.bullets.remove(bullet)
                break

    # 強敵の更新と衝突処理
    for enemy in boss_enemies[:]:
        enemy.update()
        for bullet in player.bullets[:]:
            if enemy.is_hit_by(bullet):
                boss_enemies.remove(enemy)
                player.bullets.remove(bullet)
                

# ----------------------------
# ゲーム全体の描画
# ----------------------------
def draw():
    pyxel.cls(0)
    player.draw()

    for enemy in basic_enemies:
        enemy.draw()

    for enemy in strong_enemies:
        enemy.draw()

    for enemy in boss_enemies:
        enemy.draw()
# ----------------------------
# 起動処理
# ----------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="インベーダーゲーム")
pyxel.load("invader_game.pyxres")
init_sounds()

# プレイヤー初期化
player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 5)


basic_enemies = []
strong_enemies = []
boss_enemies = []

for i in range(10):
    x = i * 20
    y = 0
    boss_enemies.append(BossEnemy(x, y))

for i in range(10):
    x = i * 20
    y = 20
    strong_enemies.append(StrongEnemy(x, y))

for i in range(10):
    x = i * 20
    y = 40
    basic_enemies.append(BasicEnemy(x, y))

# ゲーム開始
pyxel.run(update, draw)
