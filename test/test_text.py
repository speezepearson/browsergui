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
