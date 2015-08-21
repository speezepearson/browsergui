from browsergui import Grid, Text
from . import BrowserGUITestCase

def grid_of_text_xml(*textss):
  return '<table>{}</table>'.format(
    ''.join(
      '<tr>{}</tr>'.format(
        ''.join(
          '<td><span>{}</span></td>'.format(text)
          if text is not None
          else '<td/>'
          for text in texts))
      for texts in textss))

class ButtonTest(BrowserGUITestCase):
  def test_construction(self):
    Grid(n_rows=3, n_columns=3)

    with self.assertRaises(TypeError):
      Grid(n_rows=-3, n_columns=3)

    with self.assertRaises(TypeError):
      Grid(n_rows='hi', n_columns=3)
    with self.assertRaises(TypeError):
      Grid(n_rows=3, n_columns='hi')

    with self.assertRaises(TypeError):
      Grid([['hi']])

  def test_constructor_guesses_dimensions(self):
    g = Grid([[Text('a')], [Text('b'), None, Text('d')]])
    self.assertEqual(2, g.n_rows)
    self.assertEqual(3, g.n_columns)

  def test_getitem(self):
    a, b, c, d = Text('a'), Text('b'), Text('c'), Text('d')
    g = Grid([[a,b], [c,d]])

    with self.assertRaises(TypeError):
      g[0]
    with self.assertRaises(TypeError):
      g[0,'hi']
    with self.assertRaises(IndexError):
      g[3,0]

    self.assertEqual(a, g[0,0])
    self.assertEqual([a,b], g[0,:])
    self.assertEqual([a,c], g[:,0])

  def test_setitem(self):
    a, b, c, d = Text('a'), Text('b'), Text('c'), Text('d')
    g = Grid([[a], [c, d]])

    g[0, 1] = b
    self.assertEqual(g, b.parent)
    self.assertEqual([a,b,c,d], list(g.children))
    self.assertEqual(b, g[0,1])
    self.assertUnstyledHTMLLike(grid_of_text_xml(['a','b'], ['c','d']), g)

    t = Text('t')
    g[0,1] = t
    self.assertIsNone(b.parent)
    self.assertEqual(g, t.parent)
    self.assertEqual([a,t,c,d], list(g.children))
    self.assertEqual(t, g[0,1])
    self.assertUnstyledHTMLLike(grid_of_text_xml(['a','t'], ['c','d']), g)

  def test_delitem(self):
    a, b, c, d = Text('a'), Text('b'), Text('c'), Text('d')
    g = Grid([[a], [c, d]])

    del g[1,0]
    self.assertIsNone(c.parent)
    self.assertEqual([a,d], list(g.children))
    self.assertUnstyledHTMLLike(grid_of_text_xml(['a',None],[None,'d']), g)

  def test_set_n_rows(self):
    a, b, c, d = Text('a'), Text('b'), Text('c'), Text('d')
    g = Grid([[a, b], [c, d]])

    g.n_rows = 1
    self.assertEqual(g, a.parent)
    self.assertEqual(g, b.parent)
    self.assertIsNone(c.parent)
    self.assertIsNone(d.parent)
    self.assertEqual([a,b], list(g.children))
    self.assertEqual(1, g.n_rows)
    with self.assertRaises(IndexError):
      g[1,0]
    self.assertUnstyledHTMLLike(grid_of_text_xml(['a','b']), g)

    g.n_rows = 2
    self.assertIsNone(g[1,0])
    self.assertEqual([a,b], list(g.children))
    g[1,0] = c
    self.assertEqual(g, c.parent)
    self.assertEqual([a,b,c], list(g.children))
    self.assertUnstyledHTMLLike(grid_of_text_xml(['a','b'],['c',None]), g)

  def test_set_n_rows_to_0(self):
    g = Grid(n_rows=2, n_columns=1)
    g.n_rows = 0
    self.assertUnstyledHTMLLike('<table></table>', g)
    g.n_rows = 1
    self.assertUnstyledHTMLLike('<table><tr><td /></tr></table>', g)

  def test_set_n_columns_to_0(self):
    g = Grid(n_rows=1, n_columns=2)
    g.n_columns = 0
    self.assertUnstyledHTMLLike('<table><tr></tr></table>', g)
    g.n_columns = 1
    self.assertUnstyledHTMLLike('<table><tr><td /></tr></table>', g)


  def test_set_n_columns(self):
    a, b, c, d = Text('a'), Text('b'), Text('c'), Text('d')
    g = Grid([[a, b], [c, d]])

    g.n_columns = 1
    self.assertEqual(g, a.parent)
    self.assertEqual(g, c.parent)
    self.assertIsNone(b.parent)
    self.assertIsNone(d.parent)
    self.assertEqual([a,c], list(g.children))
    self.assertEqual(1, g.n_columns)
    with self.assertRaises(IndexError):
      g[0,1]
    self.assertUnstyledHTMLLike(grid_of_text_xml(['a'],['c']), g)

    g.n_columns = 2
    self.assertIsNone(g[0,1])
    self.assertEqual([a,c], list(g.children))
    g[0,1] = b
    self.assertEqual(g, b.parent)
    self.assertEqual([a,b,c], list(g.children))
    self.assertUnstyledHTMLLike(grid_of_text_xml(['a','b'], ['c', None]), g)

  def test_tag(self):
    self.assertUnstyledHTMLLike('<table></table>', Grid(n_rows=0, n_columns=0))
    self.assertUnstyledHTMLLike('<table></table>', Grid(n_rows=0, n_columns=1))
    self.assertUnstyledHTMLLike('<table><tr></tr></table>', Grid(n_rows=1, n_columns=0))
    self.assertUnstyledHTMLLike('<table><tr><td /></tr></table>', Grid(n_rows=1, n_columns=1))
    self.assertUnstyledHTMLLike('<table><tr><td /><td /></tr></table>', Grid(n_rows=1, n_columns=2))

  def test_cell_styling(self):
    g = Grid(n_rows=1, n_columns=1)
    self.assertEqual('border: 1px solid black', g.tag.childNodes[0].childNodes[0].getAttribute('style'))
