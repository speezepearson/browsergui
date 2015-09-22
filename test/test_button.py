from browsergui import Button, Event, Click
from . import BrowserGUITestCase

class ButtonTest(BrowserGUITestCase):
  def test_construction(self):
    Button("Press me")

    with self.assertRaises(TypeError):
      Button(0)

  def test_default_text(self):
    self.assertEqual(Button().text, "Click!")

  def test_callback_is_settable(self):
    xs = []
    b = Button(callback=(lambda: xs.append(1)))
    b.handle_event(Click(target_id=b.id))
    self.assertEqual([1], xs)

    xs = []
    b.callback = (lambda: xs.append(2))
    b.handle_event(Click(target_id=b.id))
    self.assertEqual([2], xs)

    xs = []
    b.callback = None
    b.handle_event(Click(target_id=b.id))
    self.assertEqual([], xs)

  def test_tag(self):
    self.assertHTMLLike('<button onclick="notify_server({target_id: this.getAttribute(&quot;id&quot;), type_name: event.type})">Hi</button>', Button('Hi'))
