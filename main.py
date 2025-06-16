import pyxel
import random
from entities.player import Player
from entities.basic_enemy import BasicEnemy
from entities.strong_enemy import StrongEnemy
from entities.boss_enemy import BossEnemy
from entities.barrier import Barrier
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT

# ----------------------------
# ゲーム状態の定義
# ----------------------------
STATE_MENU = 0
STATE_PLAY = 1
STATE_CLEAR = 2
STATE_GAME_OVER = 3
game_state = STATE_MENU

# ----------------------------
# 敵生成用設定
# ----------------------------
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

# ----------------------------
# 効果音初期化
# ----------------------------
def init_sounds():
    pyxel.sound(0).set("c3", "p", "6", "n", 10)

# ----------------------------
# 敵・プレイヤーの初期化（再利用可能）
# ----------------------------
def reset_game():
    global player, basic_enemies, strong_enemies, boss_enemies, barriers, game_state

    player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 5)

    basic_enemies = []
    strong_enemies = []
    boss_enemies = []

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

    # ▼ バリア3つを設置
    barriers = [
        Barrier(100, SCREEN_HEIGHT - 60),
        Barrier(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT - 60),
        Barrier(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 60)
    ]

    game_state = STATE_MENU

# ----------------------------
# ゲーム全体の更新
# ----------------------------
def update():
    global game_state

    if game_state == STATE_MENU:
        if pyxel.btnp(pyxel.KEY_SPACE):
            game_state = STATE_PLAY
        return

    if game_state == STATE_CLEAR or game_state == STATE_GAME_OVER:
        if pyxel.btnp(pyxel.KEY_R):
            reset_game()
        return

    player.update()

    # バリアと弾の衝突チェック
    for barrier in barriers:
        barrier.update(player.bullets)
        for enemy in basic_enemies + strong_enemies + boss_enemies:
            barrier.update(enemy.bullets)

    # BasicEnemy の更新と弾の衝突判定
    for enemy in basic_enemies[:]:
        enemy.update()
        for bullet in player.bullets[:]:
            if enemy.is_hit_by(bullet):
                basic_enemies.remove(enemy)
                player.bullets.remove(bullet)
                break
        for enemy_bullet in enemy.bullets[:]:
            if player.is_hit_by(enemy_bullet):
                game_state = STATE_GAME_OVER
                return

    # StrongEnemy の更新と弾の衝突判定
    for enemy in strong_enemies[:]:
        enemy.update()
        for bullet in player.bullets[:]:
            if enemy.is_hit_by(bullet):
                strong_enemies.remove(enemy)
                player.bullets.remove(bullet)
                break
        for enemy_bullet in enemy.bullets[:]:
            if player.is_hit_by(enemy_bullet):
                game_state = STATE_GAME_OVER
                return

    # BossEnemy の更新と弾の衝突判定（特殊攻撃含む）
    for enemy in boss_enemies[:]:
        enemy.update()
        for bullet in player.bullets[:]:
            if enemy.is_hit_by(bullet):
                boss_enemies.remove(enemy)
                player.bullets.remove(bullet)
                break
        for enemy_bullet in enemy.bullets[:]:
            if player.is_hit_by(enemy_bullet):
                game_state = STATE_GAME_OVER
                return

    # 敵が全滅したらゲームクリアへ
    if not basic_enemies and not strong_enemies and not boss_enemies:
        game_state = STATE_CLEAR

# ----------------------------
# ゲーム全体の描画
# ----------------------------
def draw():
    pyxel.cls(0)

    if game_state == STATE_MENU:
        title = "INVADER GAME"
        prompt = "PRESS SPACE TO START"

        title_x = (SCREEN_WIDTH - len(title) * 4) // 2
        title_y = SCREEN_HEIGHT // 2 - 10
        prompt_x = (SCREEN_WIDTH - len(prompt) * 4) // 2
        prompt_y = SCREEN_HEIGHT // 2 + 10

        pyxel.text(title_x, title_y, title, 7)
        if (pyxel.frame_count // 30) % 2 == 0:
            pyxel.text(prompt_x, prompt_y, prompt, 6)
        return

    elif game_state == STATE_CLEAR:
        clear_text = "!!! GAME CLEAR !!!"
        restart_text = "PRESS R TO RESTART"

        clear_x = (SCREEN_WIDTH - len(clear_text) * 4) // 2
        restart_x = (SCREEN_WIDTH - len(restart_text) * 4) // 2

        pyxel.text(clear_x, SCREEN_HEIGHT // 2 - 10, clear_text, 10)
        if (pyxel.frame_count // 30) % 2 == 0:
            pyxel.text(restart_x, SCREEN_HEIGHT // 2 + 10, restart_text, 7)
        return

    elif game_state == STATE_GAME_OVER:
        over_text = "GAME OVER"
        restart_text = "PRESS R TO RETRY"

        over_x = (SCREEN_WIDTH - len(over_text) * 4) // 2
        restart_x = (SCREEN_WIDTH - len(restart_text) * 4) // 2

        pyxel.text(over_x, SCREEN_HEIGHT // 2 - 10, over_text, 8)
        if (pyxel.frame_count // 30) % 2 == 0:
            pyxel.text(restart_x, SCREEN_HEIGHT // 2 + 10, restart_text, 7)
        return

    # プレイ中の描画
    player.draw()

    for enemy in basic_enemies:
        enemy.draw()
    for enemy in strong_enemies:
        enemy.draw()
    for enemy in boss_enemies:
        enemy.draw()

    for barrier in barriers:
        barrier.draw()

# ----------------------------
# 起動処理
# ----------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="インベーダーゲーム")
pyxel.load("invader_game.pyxres")
init_sounds()
reset_game()

pyxel.run(update, draw)
