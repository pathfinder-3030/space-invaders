import pyxel


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

# プレイヤー初期位置
playerX = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
playerY = SCREEN_HEIGHT - PLAYER_HEIGHT - 5  # 画面下に配置

def drawPlayer():
    pyxel.rect(playerX, playerY, PLAYER_WIDTH, PLAYER_HEIGHT, 11)

def drawEnemies():
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x = ENEMY_START_X + col * (ENEMY_SIZE + ENEMY_SPACING)
            y = ENEMY_START_Y + row * (ENEMY_SIZE + ENEMY_SPACING)
            pyxel.rect(x, y, ENEMY_SIZE, ENEMY_SIZE, 8)

def update():
    pass  # 今後、プレイヤー移動などをここに追加

def draw():
    pyxel.cls(0)
    drawEnemies()
    drawPlayer()

pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="インベーダーゲーム")
pyxel.run(update, draw)

