from browsergui import Text, Viewport
from . import BrowserGUITestCase

class TextTest(BrowserGUITestCase):
  def test_construction(self):
    viewport = Viewport(Text('hi'), width=100, height=200)

  def test_construction_requires_dimensions(self):
    with self.assertRaises(TypeError):
      Viewport(Text('hi'))

    with self.assertRaises(TypeError):
      Viewport(Text('hi'), width=100)

    with self.assertRaises(TypeError):
      Viewport(Text('hi'), height=100)

  def test_construction_requires_element_child(self):
    with self.assertRaises(TypeError):
      Viewport(width=100, height=200)
    with self.assertRaises(TypeError):
      Viewport(0, width=100, height=200)

  def test_construction_requires_numeric_dimensions(self):
    Viewport(Text('hi'), width=100.0, height=200)

    with self.assertRaises(TypeError):
      Viewport(Text('hi'), width='a', height=200)

  def test_construction_requires_positive_dimensions(self):
    with self.assertRaises(ValueError):
      Viewport(Text('hi'), width=-10, height=200)
    with self.assertRaises(ValueError):
      Viewport(Text('hi'), width=200, height=-10)

  def test_dimensions_are_gettable_and_settable(self):
    viewport = Viewport(Text('hi'), width=200, height=100)
    self.assertEqual(200, viewport.width)
    self.assertEqual(100, viewport.height)

    viewport.width = 50
    self.assertEqual(50, viewport.width)

    viewport.height = 70
    self.assertEqual(70, viewport.height)

  def test_dimensions_must_be_numeric(self):
    viewport = Viewport(Text('hi'), width=200, height=100)
    with self.assertRaises(TypeError):
      viewport.width = 'a'
    with self.assertRaises(TypeError):
      viewport.height = 'a'

    self.assertEqual(200, viewport.width)
    self.assertEqual(100, viewport.height)

  def test_tag(self):
    viewport = Viewport(Text('Hi'), width=50, height=60)
    self.assertHTMLLike('<div style="height: 60; overflow: scroll; width: 50"><span>Hi</span></div>', viewport)
