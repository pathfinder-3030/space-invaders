import pyxel
import random
from entities.player import Player
from entities.basic_enemy import BasicEnemy
from entities.strong_enemy import StrongEnemy
from entities.boss_enemy import BossEnemy
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT

# ----------------------------
# 星の初期化（50個、ランダムサイズ＆速度）
# ----------------------------
stars = []
NUM_STARS = 50

for _ in range(NUM_STARS):
    stars.append({
        "x": random.randint(0, SCREEN_WIDTH - 1),
        "y": random.randint(0, SCREEN_HEIGHT - 1),
        "speed": random.choice([0.3, 0.5, 1]),
        "size": random.choice([1, 2])  # サイズ: 1px または 2px角
    })

# ----------------------------
# 効果音初期化
# ----------------------------
def init_sounds():
    pyxel.sound(0).set("c3", "p", "6", "n", 10)

# ----------------------------
# ゲーム全体の更新
# ----------------------------
def update():
    # 星の位置更新
    for star in stars:
        star["y"] += star["speed"]
        if star["y"] >= SCREEN_HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, SCREEN_WIDTH - 1)

    player.update()

    for enemy in basic_enemies[:]:
        enemy.update()
        for bullet in player.bullets[:]:
            if enemy.is_hit_by(bullet):
                basic_enemies.remove(enemy)
                player.bullets.remove(bullet)
                break

    for enemy in strong_enemies[:]:
        enemy.update()
        for bullet in player.bullets[:]:
            if enemy.is_hit_by(bullet):
                strong_enemies.remove(enemy)
                player.bullets.remove(bullet)
                break

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

    # 星をサイズに応じて描画
    for star in stars:
        x = int(star["x"])
        y = int(star["y"])
        if star["size"] == 1:
            pyxel.pset(x, y, 7)  # 小さな白点
        else:
            pyxel.rect(x, y, 2, 2, 7)  # 大きめの白点（正方形）

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

player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 5)

basic_enemies = []
strong_enemies = []
boss_enemies = []

enemy_rows = [
    {"type": BossEnemy, "row_count": 1},
    {"type": StrongEnemy, "row_count": 1},
    {"type": BasicEnemy, "row_count": 1},
]

enemies_per_group = 5
group_count = 3
enemy_spacing_x = 30
enemy_spacing_y = 20
group_margin_x = 40

for row_index, row in enumerate(enemy_rows):
    for group_index in range(group_count):
        for i in range(enemies_per_group):
            x = (group_index * (enemies_per_group * enemy_spacing_x + group_margin_x)) + (i * enemy_spacing_x) + 20
            y = row_index * enemy_spacing_y + 20
            enemy_instance = row["type"](x, y)
            if row["type"] == BossEnemy:
                boss_enemies.append(enemy_instance)
            elif row["type"] == StrongEnemy:
                strong_enemies.append(enemy_instance)
            elif row["type"] == BasicEnemy:
                basic_enemies.append(enemy_instance)

pyxel.run(update, draw)
