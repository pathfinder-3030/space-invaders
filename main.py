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

    # ボス敵の更新と衝突処理
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

# 敵リスト初期化
basic_enemies = []
strong_enemies = []
boss_enemies = []

# 敵の行構成：上から順にBoss→Strong→Basic
enemy_rows = [
    {"type": BossEnemy, "row_count": 1},
    {"type": StrongEnemy, "row_count": 1},
    {"type": BasicEnemy, "row_count": 1},
]

# 各グループの設定
enemies_per_group = 5     # 各グループの敵数
group_count = 3           # 横方向に配置するグループ数
enemy_spacing_x = 30      # 敵同士の横間隔
enemy_spacing_y = 20      # 敵段の縦間隔
group_margin_x = 40       # グループ間のスペース

# 敵の配置処理
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

# ゲーム開始
pyxel.run(update, draw)
