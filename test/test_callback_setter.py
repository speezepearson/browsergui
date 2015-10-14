from browsergui import Text, Click

from . import BrowserGUITestCase

class CallbackSetterTest(BrowserGUITestCase):

  def setUp(self):
    self.element = Text('')
    self.tag = self.element.tag
    self.callback_setter = self.element.callbacks

  def test_setitem__adds_attribute(self):
    self.callback_setter[Click] = (lambda event: None)
    self.assertIn('onclick', self.tag.attributes.keys())

  def test_setitem__marks_dirty(self):
    with self.assertMarksDirty(self.element):
      self.callback_setter[Click] = (lambda event: None)

  def test_delitem__removes_attribute(self):
    self.callback_setter[Click] = (lambda event: None)
    del self.callback_setter[Click]
    self.assertNotIn('onclick', self.tag.attributes.keys())

  def test_delitem__marks_dirty(self):
    self.callback_setter[Click] = (lambda event: None)

    with self.assertMarksDirty(self.element):
      del self.callback_setter[Click]
