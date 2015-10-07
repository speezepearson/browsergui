import json
from browsergui import Element, Container, Event, Click

from . import BrowserGUITestCase

class ElementTest(BrowserGUITestCase):

  def test_construction(self):
    Element(tag_name="a")

  def test_callbacks(self):

    e = Element(tag_name="a")

    e.callbacks[Click] = self.set_last_event
    self.assertEqual(e.callbacks[Click], self.set_last_event)

    del e.callbacks[Click]
    self.assertNotIn(Click, e.callbacks)

    with self.assertRaises(KeyError):
      del e.callbacks[Click]
