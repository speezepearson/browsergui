from browsergui import Container, Text, Button, Link
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

  def test_tag(self):
    self.assertHTMLLike('<div />', Container())

class TextTest(BrowserGUITestCase):
  def test_construction(self):
    text = Text("blah")
    self.assertEqual(text.text, "blah")
    
    with self.assertRaises(TypeError):
      Text(0)

  def test_tag(self):
    self.assertHTMLLike('<span>Hi</span>', Text('Hi'))

class ButtonTest(BrowserGUITestCase):
  def test_construction(self):
    Button("Press me")

    with self.assertRaises(TypeError):
      Button(0)

  def test_default_text(self):
    self.assertEqual(Button().text, "Click!")

  def test_set_callback(self):
    xs = []
    b = Button(callback=(lambda: xs.append(1)))
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertEqual([1], xs)

    xs = []
    b.set_callback(lambda: xs.append(2))
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertEqual([2], xs)

  def test_tag(self):
    self.assertHTMLLike('<button>Hi</button>', Button('Hi'))

class LinkTest(BrowserGUITestCase):
  def test_construction(self):
    link = Link('I am a link!', 'http://google.com')
    self.assertEqual('I am a link!', link.text)
    self.assertEqual('http://google.com', link.url)

  def test_tag(self):
    self.assertHTMLLike('<a target="_blank" href="http://google.com">Google</a>', Link('Google', 'http://google.com'))
