import unittest
import xml.dom.minidom

from browsergui.events import Event, Click

class EventTest(unittest.TestCase):
  def test_enable_server_notification(self):
    tag = xml.dom.minidom.parseString('<a />').documentElement
    Click.enable_server_notification(tag)
    self.assertEqual(
      'notify_server({target_id: this.getAttribute("id"), type_name: event.type})',
      tag.getAttribute('onclick'))

  def test_disable_server_notification(self):
    tag = xml.dom.minidom.parseString('<a />').documentElement
    Click.enable_server_notification(tag)
    Click.disable_server_notification(tag)
    self.assertFalse(tag.getAttribute('onclick'))

    with self.assertRaises(KeyError):
      Click.disable_server_notification(tag)

  def test_from_dict(self):
    d = dict(type_name=Click.javascript_type_name, target_id="foo")
    e = Event.from_dict(d)
    self.assertIsInstance(e, Click)
    self.assertEqual('foo', e.target_id)
