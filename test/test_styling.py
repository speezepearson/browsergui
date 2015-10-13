from browsergui import Text
from . import BrowserGUITestCase

class StylingTest(BrowserGUITestCase):
  def setUp(self):
    self.text = Text('Hi!')

  def test_initial_styling(self):
    self.assertNotIn('color', self.text.styles)
    self.assertEqual('red', Text('hi', styling={'color': 'red'}).styles['color'])

  def test_set_styles(self):
    self.text.styles['color'] = 'red'
    self.assertEqual('red', self.text.styles['color'])

  def test_delete_styles(self):
    self.text.styles['color'] = 'red'
    del self.text.styles['color']
    self.assertNotIn('color', self.text.styles)
