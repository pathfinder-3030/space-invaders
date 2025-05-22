import pyxel

# ----------------------------
# 各種設定
# ----------------------------
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16

BULLET_WIDTH = 1
BULLET_HEIGHT = 4
BULLET_SPEED = 4

# ----------------------------
# プレイヤークラス
# ----------------------------
class Player:
    def __init__(self, x, y): # 初期化処理
        self.x = x # プレイヤーのx座標
        self.y = y # プレイヤーのy座標
        self.bullet = None # 弾の状態

    def update(self):
        speed = 2 # プレイヤーの速度(2 pixel/1 frame)

        if pyxel.btn(pyxel.KEY_LEFT): # 左キーを押下した場合
            self.x = max(0, self.x - speed) 
            # max(a, b) は「a と b のうち、大きい方を返す」
            # 0 より小さくなりそうなら 0 に止める

        if pyxel.btn(pyxel.KEY_RIGHT): # 右キーを押下した場合
            self.x = min(SCREEN_WIDTH - PLAYER_WIDTH, self.x + speed)

        if pyxel.btnp(pyxel.KEY_SPACE) and self.bullet is None:
            self.bullet = [self.x + PLAYER_WIDTH // 2, self.y]
            pyxel.play(0, 0)

        if self.bullet is not None: # 弾が発射されているかどうか判定
            self.bullet[1] -= BULLET_SPEED
            if self.bullet[1] + BULLET_HEIGHT < 0:
                self.bullet = None

    def draw(self):
        # pyxel.blt(x, y, img, u, v, w, h, colkey)
        pyxel.blt(self.x, self.y, 0, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 0)
        if self.bullet is not None:
            pyxel.rect(self.bullet[0], self.bullet[1], BULLET_WIDTH, BULLET_HEIGHT, 7)

# ----------------------------
# 効果音初期化
# ----------------------------
def init_sounds():
    pyxel.sound(0).set("c3", "p", "6", "n", 10)

# ----------------------------
# ゲーム全体の初期化
# ----------------------------
def update():
    player.update()

def draw():
    pyxel.cls(0)
    player.draw()

# ----------------------------
# 起動処理
# ----------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Invader with Class")
pyxel.load("invader_game.pyxres")
init_sounds()
player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 5)
pyxel.run(update, draw)
