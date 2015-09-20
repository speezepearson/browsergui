import numbers
from . import Element

def empty_grid(n_rows, n_columns):
  if n_rows < 0 or not isinstance(n_rows, numbers.Integral):
    raise TypeError('number of rows must be non-negative integer')
  if n_columns < 0 or not isinstance(n_columns, numbers.Integral):
    raise TypeError('number of columns must be non-negative integer')
  return [[None for j in range(n_columns)] for i in range(n_rows)]

def smallest_fitting_dimensions(cells):
  return (len(cells), (max(len(row) for row in cells) if cells else 0))

class Grid(Element):
  """A two-dimensional grid of elements.

  A grid's number of rows and columns are given by `n_rows` and `n_columns`.
  Those properties may also be set, to change the number of rows and columns.

  Grids are indexable by pairs of non-negative integers, e.g.

          my_grid[0, 0]
          my_grid[3, 2] = Text('hi')
          my_grid[1, 2] = None
          del my_grid[3, 3]
  """
  def __init__(self, cells=(), n_rows=None, n_columns=None, **kwargs):
    super(Grid, self).__init__(tag_name='table', **kwargs)
    self.set_styles(**{'border-spacing': '0', 'border-collapse': 'collapse'})

    if not all(all(isinstance(x, Element) or x is None for x in row) for row in cells):
      raise TypeError('cell contents must be Elements')

    if not (cells or (n_rows is not None and n_columns is not None)):
      raise ValueError("can't guess dimensions for Grid")

    self._n_rows = 0
    self._n_columns = 0
    self._cells = []
    if cells:
      self.n_rows, self.n_columns = smallest_fitting_dimensions(cells)
    else:
      self.n_rows, self.n_columns = n_rows, n_columns

    for (i, row) in enumerate(cells):
      for (j, cell) in enumerate(row):
        if cell is not None:
          self[i,j] = cell

  @property
  def n_rows(self):
    return self._n_rows
  @n_rows.setter
  def n_rows(self, value):
    if value < 0 or not isinstance(value, numbers.Integral):
      raise TypeError('number of rows must be non-negative integer')
    if value < self.n_rows:
      for i in range(value, self.n_rows):
        for j in range(self.n_columns):
          if self[i,j] is not None:
            del self[i,j]
      for tr in self.tag.childNodes[value:]:
        self.tag.removeChild(tr)
      self._cells = self._cells[:value]
    else:
      while len(self._cells) < value:
        self._cells.append([None]*self.n_columns)
        tr = self._new_tr()
        for j in range(self.n_columns):
          td = self._new_td()
          tr.appendChild(td)
        self.tag.appendChild(tr)

    self._n_rows = value
    self.mark_dirty()

  @property
  def n_columns(self):
    return self._n_columns
  @n_columns.setter
  def n_columns(self, value):
    if value < 0 or not isinstance(value, numbers.Integral):
      raise TypeError('number of columns must be non-negative integer')
    if value < self.n_columns:
      for i in range(self.n_rows):
        for j in range(value, self.n_columns):
          if self[i,j] is not None:
            del self[i,j]
        self._cells[i] = self._cells[i][:value]
        for td in self.tag.childNodes[i].childNodes[value:]:
          self.tag.childNodes[i].removeChild(td)
    else:
      for i, row in enumerate(self._cells):
        while len(row) < value:
          row.append(None)
          td = self._new_td()
          self.tag.childNodes[i].appendChild(td)
    self._n_columns = value
    self.mark_dirty()

  @property
  def children(self):
    return [x for x in sum(self._cells, []) if x is not None]

  def _new_tr(self):
    return self.tag.ownerDocument.createElement('tr')
  def _new_td(self):
    td = self.tag.ownerDocument.createElement('td')
    td.setAttribute('style', 'border: 1px solid black')
    return td

  def __getitem__(self, indices):
    (i, j) = indices
    if isinstance(i, slice):
      rows = self._cells[i]
      return [row[j] for row in rows]
    else:
      return self._cells[i][j]

  def __setitem__(self, indices, child):
    (i, j) = indices
    if isinstance(i, slice) or isinstance(j, slice):
      raise NotImplementedError("slice assignment to Grids not yet supported")

    td = self.tag.childNodes[i].childNodes[j]
    child.parent = self
    
    old_child = self._cells[i][j]
    if old_child is not None:
      old_child.parent = None
      td.removeChild(td.childNodes[0])

    self._cells[i][j] = child

    td.appendChild(child.tag)

    self.mark_dirty()

  def __delitem__(self, indices):
    (i, j) = indices
    if isinstance(i, slice) or isinstance(j, slice):
      raise NotImplementedError("slice deletion from Grids not yet supported")

    old_child = self._cells[i][j]
    self._cells[i][j] = None
    old_child.parent = None
    old_child.tag.parentNode.removeChild(old_child.tag)
    self.mark_dirty()
