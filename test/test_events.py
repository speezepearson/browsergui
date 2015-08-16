import unittest
import xml.dom.minidom

from browsergui.events import Event, Click, from_dict

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
    class MyEvent(Event):
      def __init__(self, flub, **kwargs):
        super(MyEvent, self).__init__(**kwargs)
        self.flub = flub

    e = MyEvent.from_dict({'flub': 'x', 'target_id': 'y'})
    self.assertEqual('x', e.flub)
    self.assertEqual('y', e.target_id)

    with self.assertRaises(TypeError):
      MyEvent.from_dict({'flub': 'x', 'target_id': 'y', 'extra': 'foo'})

  def test_global_from_dict(self):
    e = from_dict({'type_name': Click.javascript_type_name, 'target_id': 'x'})
    self.assertIsInstance(e, Click)
    self.assertEqual('x', e.target_id)

    with self.assertRaises(KeyError):
      from_dict({'type_name': 'nonexistenttype'})
