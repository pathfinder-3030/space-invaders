import pyxel

# ウィンドウサイズ
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

# プレイヤー設定
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 8

# 敵設定
ENEMY_SIZE = 8
ENEMY_COLS = 10
ENEMY_ROWS = 5
ENEMY_SPACING = 2
ENEMY_START_X = 10
ENEMY_START_Y = 10
ENEMY_SPEED = 1
ENEMY_MOVE_INTERVAL = 1  # フレーム数：小さいほど速い

# 弾設定
BULLET_WIDTH = 1
BULLET_HEIGHT = 4
BULLET_SPEED = 4

# プレイヤー初期位置
playerX = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
playerY = SCREEN_HEIGHT - PLAYER_HEIGHT - 5

# 弾（Noneで非表示）
bullet = None

# 敵の生存状態と座標
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

# 敵の移動
enemy_dx = ENEMY_SPEED
enemy_move_timer = 0

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

def update():
    global playerX, bullet, enemy_dx, enemy_move_timer

    # === プレイヤー移動 ===
    speed = 2
    if pyxel.btn(pyxel.KEY_LEFT):
        playerX = max(0, playerX - speed)
    if pyxel.btn(pyxel.KEY_RIGHT):
        playerX = min(SCREEN_WIDTH - PLAYER_WIDTH, playerX + speed)

    # === 弾の発射 ===
    if pyxel.btnp(pyxel.KEY_SPACE) and bullet is None:
        bullet_x = playerX + PLAYER_WIDTH // 2
        bullet_y = playerY
        bullet = [bullet_x, bullet_y]

    # === 弾の移動・当たり判定 ===
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
                            break
                if bullet is None:
                    break

    # === 敵の移動（ゆっくり） ===
    enemy_move_timer += 1
    if enemy_move_timer >= ENEMY_MOVE_INTERVAL:
        enemy_move_timer = 0

        # 端に到達したら方向反転
        should_reverse = False
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                if enemies[row][col]:
                    x, _ = enemy_positions[row][col]
                    if x <= 0 or x + ENEMY_SIZE >= SCREEN_WIDTH:
                        should_reverse = True

        if should_reverse:
            enemy_dx *= -1

        # 位置更新
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                if enemies[row][col]:
                    enemy_positions[row][col][0] += enemy_dx

def draw():
    pyxel.cls(0)
    drawEnemies()
    drawPlayer()
    drawBullet()

pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="インベーダーゲーム")
pyxel.run(update, draw)
