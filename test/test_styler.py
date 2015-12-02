from browsergui import Text

from . import BrowserGUITestCase

class StylerTest(BrowserGUITestCase):

  def setUp(self):
    self.element = Text('')
    self.tag = self.element.tag
    self.css = self.element.css

  def test_setitem__sets_style(self):
    self.css['k'] = 'v'
    self.assertEqual('k: v', self.tag.getAttribute('style'))

  def test_setitem__marks_dirty(self):
    with self.assertMarksDirty(self.element):
      self.css['k'] = 'v'

  def test_delitem__sets_style(self):
    self.css['a'] = '1'
    self.css['b'] = '2'
    del self.css['a']
    self.assertEqual('b: 2', self.tag.getAttribute('style'))

  def test_delitem__deletes_style_if_empty(self):
    self.css['a'] = '1'
    del self.css['a']
    self.assertNotIn('style', self.tag.attributes.keys())

  def test_delitem__marks_dirty(self):
    self.css['k'] = 'v'

    with self.assertMarksDirty(self.element):
      del self.css['k']
