import json
from browsergui import Element, Container, Event, Click
from browsergui.elements import NoSuchCallbackError

from . import BrowserGUITestCase

class ElementTest(BrowserGUITestCase):

  def test_construction(self):
    Element(tag_name="a")

  def test_callbacks(self):

    e = Element(tag_name="a")
    self.assertEqual(list(e.callbacks[Click]), [])

    e.add_callback(Click, self.set_last_event)
    self.assertEqual(list(e.callbacks[Click]), [self.set_last_event])

    e.remove_callback(Click, self.set_last_event)
    with self.assertRaises(NoSuchCallbackError):
      e.remove_callback(Click, self.set_last_event)

  def test_toggle_visibility(self):
    e = Element(tag_name='a')
    e.toggle_visibility()
    self.assertEqual('none', e.get_style('display'))
    e.toggle_visibility()
    self.assertIsNone(e.get_style('display'))
