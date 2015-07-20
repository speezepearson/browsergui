from browsergui import Text
from . import BrowserGUITestCase

class StylingTest(BrowserGUITestCase):
  def setUp(self):
    self.text = Text('Hi!')

  def test_get_style_initial_is_None(self):
    self.assertIsNone(self.text.get_style('color'))

  def test_set_styles(self):
    self.text.set_styles(color='red')
    self.assertEqual('red', self.text.get_style('color'))

  def test_delete_styles(self):
    self.text.set_styles(color='red')
    self.text.delete_styles('color')
    self.assertIsNone(self.text.get_style('color'))
