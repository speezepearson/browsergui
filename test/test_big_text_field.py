from browsergui import BigTextField
from browsergui.events import Input
from . import BrowserGUITestCase


class BigTextFieldTest(BrowserGUITestCase):
  def test_constructor(self):
    self.assertEqual('foo', BigTextField(value='foo').value)

  def test_set_value(self):
    e = BigTextField()
    e.value = 'foo'
    self.assertEqual('foo', e.value)

  def test_set_value__marks_dirty(self):
    e = BigTextField()
    with self.assertMarksDirty(e):
      e.value = 'foo'

  def test_set_placeholder(self):
    e = BigTextField()
    e.placeholder = 'foo'
    self.assertEqual('foo', e.placeholder)
    self.assertEqual('foo', e.tag.getAttribute('placeholder'))

  def test_set_placeholder__marks_dirty(self):
    e = BigTextField()
    with self.assertMarksDirty(e):
      e.placeholder = 'foo'

  def test_change_callback(self):
    xs = []
    e = BigTextField(change_callback=(lambda: xs.append(1)))
    e.value = 'hi'
    self.assertEqual([1], xs)

    xs = []
    e.change_callback = (lambda: xs.append(2))
    e.value = 'bye'
    self.assertEqual([2], xs)

  def test_validation(self):
    t = BigTextField()

    for good_object in ('', 'abc', u'abc', 'a b c'):
      t.value = good_object

    for bad_object in (None, 0, [], ()):
      with self.assertRaises(TypeError):
        t.value = bad_object

  def test_def_change_callback(self):
    t = BigTextField()
    @t.def_change_callback
    def callback():
      pass
    self.assertEqual(callback, t.change_callback)
