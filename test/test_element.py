import json
from browsergui import Element, Container, CLICK, KEYDOWN, KEYUP
from browsergui.elements import NoSuchCallbackError

from . import BrowserGUITestCase

class ElementTest(BrowserGUITestCase):

  def test_construction(self):
    Element(tag_name="a")

  def test_callbacks(self):

    e = Element(tag_name="a")
    e.add_callback(CLICK, self.set_last_event)
    e.add_callback(KEYDOWN, self.set_last_event)

    e.handle_event({'type': CLICK, 'id': e.id})
    self.assertEqual(self.last_event, {'type': CLICK, 'id': e.id})

    e.handle_event({'type': KEYDOWN, 'id': e.id, 'key': 'a'})
    self.assertEqual(self.last_event, {'type': KEYDOWN, 'id': e.id, 'key': 'a'})

    e.remove_callback(CLICK, self.set_last_event)
    with self.assertRaises(NoSuchCallbackError):
      e.remove_callback(CLICK, self.set_last_event)

    self.assertEqual(list(e.callbacks[CLICK]), [])
    self.assertEqual(list(e.callbacks[KEYDOWN]), [self.set_last_event])
    self.assertEqual(list(e.callbacks[KEYUP]), [])

  def test_toggle_visibility(self):
    e = Element(tag_name='a')
    e.toggle_visibility()
    self.assertEqual('none', e.get_style('display'))
    e.toggle_visibility()
    self.assertIsNone(e.get_style('display'))
