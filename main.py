import pyxel

# ----------------------------
# 各種設定
# ----------------------------
#ウィンドウ
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

# プレイヤー
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16

# インベーダー
ENEMY_SIZE = 8 # 敵の大きさ
ENEMY_COLS = 10 # 敵を横方向に何体配置するか
ENEMY_ROWS = 5 # 敵の行数
ENEMY_SPACING = 2 # 敵同士の隙間
ENEMY_START_X = 10 # 敵の最初の左端のX座標
ENEMY_START_Y = 10 # 敵の最初の上のY座標
ENEMY_SPEED = 1 # 敵の横移動のスピード(x方向) 
ENEMY_MOVE_INTERVAL = 1 # 敵を何フレームごとに敵を動かすか
ENEMY_DESCEND_STEP = 4 # 敵が壁にぶつかって進行方向を反転するとき、Y座標を Xピクセル下げる

# 弾
BULLET_WIDTH = 1
BULLET_HEIGHT = 4
BULLET_SPEED = 4

# ----------------------------
# グローバル変数
# ----------------------------
playerX = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2 # プレイヤーの初期位置(X軸の中央位置)
playerY = SCREEN_HEIGHT - PLAYER_HEIGHT - 5 # プレイヤーのy座標
bullet = None # プレイヤーが発射した弾の状態 (ウィンドウの外や敵に当たるとNoneになる)
enemy_dx = ENEMY_SPEED # 敵のスピード
enemy_move_timer = 0 # 敵の移動タイミングを制御するためのカウンター
game_state = "title" # ページの状態管理 # title / playing / gameover / gameclear

# ----------------------------
# 敵初期化
# ----------------------------
def init_enemies():
    global enemies,enemy_positions
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
    pyxel.sound(0).set("c3", "p", "6", "n", 10)
    pyxel.sound(1).set("f2", "n", "7", "n", 10)
    pyxel.sound(2).set("c3g2c2", "nnn", "654", "n", 20)
    pyxel.sound(3).set("c3e3g3c4", "nnnn", "4444", "n", 20)

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

    if pyxel.btnp(pyxel.KEY_SPACE) and bullet is None:
        bullet = [playerX + PLAYER_WIDTH // 2, playerY]
        pyxel.play(0, 0)

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
                            pyxel.play(1, 1)
                            break
                if bullet is None:
                    break

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

    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            if enemies[row][col]:
                _, y = enemy_positions[row][col]
                if y + ENEMY_SIZE >= playerY:
                    pyxel.play(0, 2)
                    game_state = "gameover"
                    return

    all_dead = all(not alive for row in enemies for alive in row)
    if all_dead:
        pyxel.play(0, 3)
        game_state = "gameclear"

# ----------------------------
# ゲーム初期化
# ----------------------------
def reset_game():
    global playerX, bullet, enemy_dx, enemy_move_timer
    playerX = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
    bullet = None
    enemy_dx = ENEMY_SPEED
    enemy_move_timer = 0
    init_enemies()

# ----------------------------
# 描画
# ----------------------------
def drawPlayer():
    # pyxel.blt(x, y, img, u, v, w, h, colkey)
    pyxel.blt(playerX, playerY, 0, 0, 0, 16, 16, 0)

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
pyxel.load("invader_game.pyxres") 
init_sounds()
pyxel.run(update, draw)
