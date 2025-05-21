import pyxel

# ウィンドウ
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

# プレイヤー
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 8

# インベーダー
ENEMY_SIZE = 8
ENEMY_COLS = 10
ENEMY_ROWS = 5
ENEMY_SPACING = 2
ENEMY_START_X = 10
ENEMY_START_Y = 10

# 弾
BULLET_WIDTH = 1
BULLET_HEIGHT = 4
BULLET_SPEED = 4

# プレイヤー初期位置
playerX = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
playerY = SCREEN_HEIGHT - PLAYER_HEIGHT - 5

# 弾
bullet = None

# 敵の生存状態を保持
enemies = [[True for _ in range(ENEMY_COLS)] for _ in range(ENEMY_ROWS)]

def drawPlayer():
    pyxel.rect(playerX, playerY, PLAYER_WIDTH, PLAYER_HEIGHT, 11)

def drawEnemies():
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            if enemies[row][col]:
                x = ENEMY_START_X + col * (ENEMY_SIZE + ENEMY_SPACING)
                y = ENEMY_START_Y + row * (ENEMY_SIZE + ENEMY_SPACING)
                pyxel.rect(x, y, ENEMY_SIZE, ENEMY_SIZE, 8)

def drawBullet():
    if bullet is not None:
        pyxel.rect(bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT, 7)

def update():
    global playerX, bullet
    speed = 2

    # プレイヤー移動
    if pyxel.btn(pyxel.KEY_LEFT):
        playerX = max(0, playerX - speed)
    if pyxel.btn(pyxel.KEY_RIGHT):
        playerX = min(SCREEN_WIDTH - PLAYER_WIDTH, playerX + speed)

    # 弾発射
    if pyxel.btnp(pyxel.KEY_SPACE) and bullet is None:
        bullet_x = playerX + PLAYER_WIDTH // 2
        bullet_y = playerY
        bullet = [bullet_x, bullet_y]

    # 弾の移動と当たり判定
    if bullet is not None:
        bullet[1] -= BULLET_SPEED

        # 画面外なら削除
        if bullet[1] + BULLET_HEIGHT < 0:
            bullet = None
        else:
            # 敵との当たり判定
            for row in range(ENEMY_ROWS):
                for col in range(ENEMY_COLS):
                    if enemies[row][col]:
                        enemy_x = ENEMY_START_X + col * (ENEMY_SIZE + ENEMY_SPACING)
                        enemy_y = ENEMY_START_Y + row * (ENEMY_SIZE + ENEMY_SPACING)

                        if (
                            bullet[0] < enemy_x + ENEMY_SIZE and
                            bullet[0] + BULLET_WIDTH > enemy_x and
                            bullet[1] < enemy_y + ENEMY_SIZE and
                            bullet[1] + BULLET_HEIGHT > enemy_y
                        ):
                            enemies[row][col] = False  # 敵を倒す
                            bullet = None  # 弾も消す
                            break
                if bullet is None:
                    break

def draw():
    pyxel.cls(0)
    drawEnemies()
    drawPlayer()
    drawBullet()

pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="インベーダーゲーム")
pyxel.run(update, draw)
