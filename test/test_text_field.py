from browsergui import TextField
from browsergui.events import Input
from . import BrowserGUITestCase


class TextFieldTest(BrowserGUITestCase):
  def test_constructor(self):
    self.assertEqual('foo', TextField(value='foo').value)
    self.assertEqual('foo', TextField(placeholder='foo').placeholder)

  def test_set_value(self):
    e = TextField()
    e.value = 'foo'
    self.assertEqual('foo', e.value)
    self.assertEqual('foo', e.tag.getAttribute('value'))

  def test_set_placeholder(self):
    e = TextField()
    e.placeholder = 'foo'
    self.assertEqual('foo', e.placeholder)
    self.assertEqual('foo', e.tag.getAttribute('placeholder'))

  def test_change_callback(self):
    xs = []
    e = TextField(change_callback=(lambda: xs.append(1)))
    e.value = 'hi'
    self.assertEqual([1], xs)
