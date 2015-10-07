import json
from browsergui import Element, Container, Event, Click

from . import BrowserGUITestCase

class ElementTest(BrowserGUITestCase):

  def test_construction(self):
    Element(tag_name="a")

  def test_callbacks(self):

    e = Element(tag_name="a")

    e.set_callback(Click, self.set_last_event)
    self.assertEqual(e.get_callback(Click), self.set_last_event)

    e.delete_callback(Click)
    self.assertIsNone(e.get_callback(Click))

    with self.assertRaises(KeyError):
      e.delete_callback(Click)
