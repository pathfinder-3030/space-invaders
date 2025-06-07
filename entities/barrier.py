import pyxel

class Barrier:
    def __init__(self, x, y, block_size=2):
        self.x = x
        self.y = y
        self.block_size = block_size

        self.grid = [
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.rows = len(self.grid) 
        self.columns = len(self.grid[0]) 
        self.width = self.columns * block_size 
        self.height = self.rows * block_size 

    def update(self, bullets):
        for bullet in bullets[:]:
            if self.x <= bullet.x <= self.x + self.width and self.y <= bullet.y <= self.y + self.height:
                col = int((bullet.x - self.x) // self.block_size)
                row = int((bullet.y - self.y) // self.block_size)
                if 0 <= row < self.rows and 0 <= col < self.columns:
                    if self.grid[row][col] == 1:
                        self.grid[row][col] = 0
                        bullets.remove(bullet)

    def draw(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid[row][col] == 1:
                    px = self.x + col * self.block_size
                    py = self.y + row * self.block_size
                    pyxel.rect(px, py, self.block_size, self.block_size, 8) 
