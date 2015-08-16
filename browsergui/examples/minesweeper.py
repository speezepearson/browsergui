import random
from browsergui import *

W, H = 20, 20
MINE_DENSITY = 0.14

grid = Grid(n_rows=W, n_columns=H)

class MinesweeperGUI(GUI):
  def __init__(self, w=20, h=20, mine_density=0.14):
    self.w = w
    self.h = h
    self.mine_density = mine_density
    self.mine_locations = set()
    self.reset_button = Button('Reset', callback=self.reset)
    self.grid = Grid(n_rows=w, n_columns=h)
    self.reset()
    super(MinesweeperGUI, self).__init__(self.reset_button, self.grid)

  def reset(self):
    self.mine_locations = set((random.randrange(H), random.randrange(W)) for _ in range(int(self.w*self.h*self.mine_density)))
    for i in range(self.h):
      for j in range(self.w):
        self.grid[i, j] = self.button_for((i, j))

  def button_for(self, ij):
    def callback():
      if ij in self.mine_locations:
        self.grid[ij] = Text('YOU LOSE')
      else:
        for nij in self.expand_region(ij):
          nmn = self.n_mine_neighbors(nij)
          self.grid[nij] = Text(' ' if nmn == 0 else str(nmn))

    return Button('?', callback=callback)

  @staticmethod
  def neighbors(ij):
    i, j = ij
    for di in (-1, 0, 1):
      for dj in (-1, 0, 1):
        if not (di == dj == 0) and (0 <= i+di < H) and (0 <= j+dj < W):
          yield (i+di, j+dj)

  def n_mine_neighbors(self, ij):
    return len(list(n for n in self.neighbors(ij) if n in self.mine_locations))

  def expand_region(self, ij):
    clean = set()
    boundary = set()
    to_expand = set([ij])
    while to_expand:
      ij = to_expand.pop()
      if self.n_mine_neighbors(ij) == 0:
        clean.add(ij)
        for nij in self.neighbors(ij):
          if nij not in (clean | boundary):
            to_expand.add(nij)
      else:
        boundary.add(ij)

    return clean | boundary

def main():
  run(MinesweeperGUI())

if __name__ == '__main__':
  main()
