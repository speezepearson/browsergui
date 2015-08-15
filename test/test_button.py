from browsergui import Button, Event, Click
from . import BrowserGUITestCase

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
    b.handle_event(Click(target_id=b.id))
    self.assertEqual([1], xs)

    xs = []
    b.set_callback(lambda: xs.append(2))
    b.handle_event(Click(target_id=b.id))
    self.assertEqual([2], xs)

  def test_tag(self):
    self.assertHTMLLike('<button>Hi</button>', Button('Hi'))
