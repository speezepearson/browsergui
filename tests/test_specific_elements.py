from browsergui import Container, Text, Button
from browsergui.elements import CLICK

from . import BrowserGUITestCase

class ContainerTest(BrowserGUITestCase):
  def test_construction(self):
    self.assertEqual(Container(), Element(tag_name="div"))
    self.assertEqual(Container(inline=True), Element(tag_name="span"))

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
    self.assertEqual(Button("Press me"), Element(html="<button>Press me</button>"))

  def test_default_text(self):
    self.assertEqual(Button().text, "Button!")

  def test_set_callback(self):
    clicked = False
    def toggle():
      nonlocal clicked
      clicked = True

    b = Button(callback=(lambda event: toggle()))
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertTrue(clicked)

    clicked = False
    b = Button()
    b.set_callback(lambda event: toggle())
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertTrue(clicked)