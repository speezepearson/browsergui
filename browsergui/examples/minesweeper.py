import random
from browsergui import *

class Game(object):
  def __init__(self, w=20, h=20, mine_density=0.14):
    self.w = w
    self.h = h
    self.mine_density = mine_density
    self.mine_locations = set((random.randrange(self.h), random.randrange(self.w)) for _ in range(int(self.w*self.h*self.mine_density)))

  def neighbors(self, ij):
    i, j = ij
    for di in (-1, 0, 1):
      for dj in (-1, 0, 1):
        if not (di == dj == 0) and (0 <= i+di < self.h) and (0 <= j+dj < self.w):
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


class MinesweeperGUI(GUI):
  def __init__(self, **kwargs):
    super(MinesweeperGUI, self).__init__(**kwargs)

    self.game = Game()

    self.w_field = TextField(value=str(self.game.w), placeholder='width')
    self.h_field = TextField(value=str(self.game.h), placeholder='height')
    self.mine_density_field = TextField(value=str(self.game.mine_density), placeholder='mine density')
    self.reset_button = Button('Reset and Apply', callback=self.reset)

    self.append(Grid([
      [Text('width'), Text('height'), Text('mine density')],
      [self.w_field, self.h_field, self.mine_density_field, self.reset_button]]))
    self.grid = None

    self.reset()

  def reset(self):
    w = int(self.w_field.value)
    h = int(self.h_field.value)
    mine_density = float(self.mine_density_field.value)

    self.game = Game(w=w, h=h, mine_density=mine_density)

    if self.grid is not None:
      self.body.disown(self.grid)
    self.grid = Grid(n_rows=self.game.h, n_columns=self.game.w)
    self.append(self.grid)

    for i in range(self.game.h):
      for j in range(self.game.w):
        self.grid[i, j] = self.button_for((i, j))

  def button_for(self, ij):
    def callback():
      if ij in self.game.mine_locations:
        self.grid[ij] = Text('YOU LOSE')
      else:
        for nij in self.game.expand_region(ij):
          nmn = self.game.n_mine_neighbors(nij)
          self.grid[nij] = Text('-' if nmn == 0 else str(nmn))

    return Button('?', callback=callback)

def main():
  run(MinesweeperGUI())

if __name__ == '__main__':
  main()
