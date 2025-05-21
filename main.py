import pyxel

# ----------------------------
# ウィンドウサイズと各種設定
# ----------------------------
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 8

ENEMY_SIZE = 8
ENEMY_COLS = 10
ENEMY_ROWS = 5
ENEMY_SPACING = 2
ENEMY_START_X = 10
ENEMY_START_Y = 10
ENEMY_SPEED = 1
ENEMY_MOVE_INTERVAL = 1
ENEMY_DESCEND_STEP = 4

BULLET_WIDTH = 1
BULLET_HEIGHT = 4
BULLET_SPEED = 4

# ----------------------------
# グローバル変数
# ----------------------------
playerX = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
playerY = SCREEN_HEIGHT - PLAYER_HEIGHT - 5
bullet = None
enemy_dx = ENEMY_SPEED
enemy_move_timer = 0
game_state = "title"  # title / playing / gameover / gameclear

# ----------------------------
# 敵初期化
# ----------------------------
def init_enemies():
    global enemies, enemy_positions
    enemies = [[True for _ in range(ENEMY_COLS)] for _ in range(ENEMY_ROWS)]
    enemy_positions = [
        [
            [
                ENEMY_START_X + col * (ENEMY_SIZE + ENEMY_SPACING),
                ENEMY_START_Y + row * (ENEMY_SIZE + ENEMY_SPACING)
            ]
            for col in range(ENEMY_COLS)
        ]
        for row in range(ENEMY_ROWS)
    ]

init_enemies()

# ----------------------------
# 効果音初期化
# ----------------------------
def init_sounds():
    # 弾の発射音：短く高め
    pyxel.sound(0).set("c3", "p", "6", "n", 10)

    # 敵が倒れる音：低くて重め
    pyxel.sound(1).set("f2", "n", "7", "n", 10)

# ----------------------------
# ゲーム更新（プレイ中）
# ----------------------------
def update_game():
    global playerX, bullet, enemy_dx, enemy_move_timer, game_state

    speed = 2
    if pyxel.btn(pyxel.KEY_LEFT):
        playerX = max(0, playerX - speed)
    if pyxel.btn(pyxel.KEY_RIGHT):
        playerX = min(SCREEN_WIDTH - PLAYER_WIDTH, playerX + speed)

    # 弾の発射
    if pyxel.btnp(pyxel.KEY_SPACE) and bullet is None:
        bullet = [playerX + PLAYER_WIDTH // 2, playerY]
        pyxel.play(0, 0)  # チャンネル0で発射音

    # 弾の移動・当たり判定
    if bullet is not None:
        bullet[1] -= BULLET_SPEED
        if bullet[1] + BULLET_HEIGHT < 0:
            bullet = None
        else:
            for row in range(ENEMY_ROWS):
                for col in range(ENEMY_COLS):
                    if enemies[row][col]:
                        enemy_x, enemy_y = enemy_positions[row][col]
                        if (
                            bullet[0] < enemy_x + ENEMY_SIZE and
                            bullet[0] + BULLET_WIDTH > enemy_x and
                            bullet[1] < enemy_y + ENEMY_SIZE and
                            bullet[1] + BULLET_HEIGHT > enemy_y
                        ):
                            enemies[row][col] = False
                            bullet = None
                            pyxel.play(1, 1)  # チャンネル1で命中音
                            break
                if bullet is None:
                    break

    # 敵の移動
    enemy_move_timer += 1
    if enemy_move_timer >= ENEMY_MOVE_INTERVAL:
        enemy_move_timer = 0

        should_reverse = False
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                if enemies[row][col]:
                    x, _ = enemy_positions[row][col]
                    if x <= 0 or x + ENEMY_SIZE >= SCREEN_WIDTH:
                        should_reverse = True

        if should_reverse:
            enemy_dx *= -1
            for row in range(ENEMY_ROWS):
                for col in range(ENEMY_COLS):
                    if enemies[row][col]:
                        enemy_positions[row][col][1] += ENEMY_DESCEND_STEP

        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                if enemies[row][col]:
                    enemy_positions[row][col][0] += enemy_dx

    # 敵が下に来たらゲームオーバー
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            if enemies[row][col]:
                _, y = enemy_positions[row][col]
                if y + ENEMY_SIZE >= playerY:
                    game_state = "gameover"
                    return

    # 敵全滅 → クリア
    all_dead = all(not alive for row in enemies for alive in row)
    if all_dead:
        game_state = "gameclear"

# ----------------------------
# ゲーム初期化（再スタート時）
# ----------------------------
def reset_game():
    global playerX, bullet, enemy_dx, enemy_move_timer
    playerX = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
    bullet = None
    enemy_dx = ENEMY_SPEED
    enemy_move_timer = 0
    init_enemies()

# ----------------------------
# 描画系
# ----------------------------
def drawPlayer():
    pyxel.rect(playerX, playerY, PLAYER_WIDTH, PLAYER_HEIGHT, 11)

def drawEnemies():
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            if enemies[row][col]:
                x, y = enemy_positions[row][col]
                pyxel.rect(x, y, ENEMY_SIZE, ENEMY_SIZE, 8)

def drawBullet():
    if bullet is not None:
        pyxel.rect(bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT, 7)

# ----------------------------
# メイン update
# ----------------------------
def update():
    global game_state
    if game_state == "title":
        if pyxel.btnp(pyxel.KEY_SPACE):
            reset_game()
            game_state = "playing"
    elif game_state == "playing":
        update_game()
    elif game_state in ["gameover", "gameclear"]:
        if pyxel.btnp(pyxel.KEY_SPACE):
            game_state = "title"

# ----------------------------
# メイン draw
# ----------------------------
def draw():
    pyxel.cls(0)
    if game_state == "title":
        pyxel.text(45, 50, "INVADER GAME", 9)
        pyxel.text(30, 70, "PRESS SPACE TO START", 7)
    elif game_state == "playing":
        drawEnemies()
        drawPlayer()
        drawBullet()
    elif game_state == "gameover":
        pyxel.text(60, 50, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(30, 70, "PRESS SPACE TO TITLE", 7)
    elif game_state == "gameclear":
        pyxel.text(60, 50, "YOU WIN!", pyxel.frame_count % 16)
        pyxel.text(30, 70, "PRESS SPACE TO TITLE", 7)

# ----------------------------
# 起動
# ----------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="インベーダーゲーム")
init_sounds()
pyxel.run(update, draw)
