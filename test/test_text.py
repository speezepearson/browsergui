from browsergui import Text
from . import BrowserGUITestCase

class TextTest(BrowserGUITestCase):
  def test_construction(self):
    text = Text("blah")
    self.assertEqual(text.text, "blah")
    
    with self.assertRaises(TypeError):
      Text(0)

  def test_tag(self):
    self.assertHTMLLike('<span>Hi</span>', Text('Hi'))

  def test_set_text(self):
    t = Text('blah')
    t.set_text('foo')
    self.assertEqual(t.text, 'foo')
    self.assertHTMLLike('<span>foo</span>', t)
