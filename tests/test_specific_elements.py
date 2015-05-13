from browsergui import Container, Text, Button
from browsergui.elements import Element, CLICK

from . import BrowserGUITestCase

class ContainerTest(BrowserGUITestCase):
  def test_construction(self):
    Container()
    Container(inline=True)

    left = Container()
    right = Container()
    top = Container(left, right)
    self.assertEqual(list(top.children), [left, right])

    with self.assertRaises(TypeError):
      Container(0)

class TextTest(BrowserGUITestCase):
  def test_construction(self):
    text = Text("blah")
    self.assertEqual(text.text, "blah")
    
    with self.assertRaises(TypeError):
      Text(0)

class ButtonTest(BrowserGUITestCase):
  def test_construction(self):
    Button("Press me")

    with self.assertRaises(TypeError):
      Button(0)

  def test_default_text(self):
    self.assertEqual(Button().text, "Click!")

  def test_set_callback(self):
    b = Button(callback=self.set_last_event)
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertEqual(self.last_event, {'type': CLICK, 'id': b.id})

    self.last_event = None
    b.set_callback(lambda event: None)
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertIsNone(self.last_event)

    b.set_callback(self.set_last_event)
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertEqual(self.last_event, {'type': CLICK, 'id': b.id})