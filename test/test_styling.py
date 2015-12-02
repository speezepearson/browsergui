from browsergui import Text
from . import BrowserGUITestCase

class StylingTest(BrowserGUITestCase):
  def setUp(self):
    self.text = Text('Hi!')

  def test_initial_css(self):
    self.assertNotIn('color', self.text.css)
    self.assertEqual('red', Text('hi', css={'color': 'red'}).css['color'])

  def test_set_styles(self):
    self.text.css['color'] = 'red'
    self.assertEqual('red', self.text.css['color'])

  def test_delete_styles(self):
    self.text.css['color'] = 'red'
    del self.text.css['color']
    self.assertNotIn('color', self.text.css)
