from browsergui import Container
from . import BrowserGUITestCase

class ContainerTest(BrowserGUITestCase):
  def test_construction(self):
    Container()
    Container(inline=True)

    left = Container()
    right = Container()
    top = Container(left, right)
    self.assertEqual(list(top.children), [left, right])

    with self.assertRaises(TypeError):
      Container(0)

  def test_tag(self):
    self.assertHTMLLike('<div />', Container())
