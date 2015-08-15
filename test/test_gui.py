from browsergui import GUI, Text, Button, Event, Click

from . import BrowserGUITestCase


class GUITest(BrowserGUITestCase):

  def test_construction(self):
    gui = GUI()

    GUI(Text("left"), Text("hi"))

    with self.assertRaises(TypeError):
      gui = GUI(0)

  def test_event_dispatch(self):
    decoy1 = Button()
    button = Button()
    decoy2 = Button()

    xs = []
    button.set_callback(lambda: xs.append(1))

    gui = GUI(decoy1, button, decoy2)

    gui.dispatch_event(Click(target_id=button.id))
    self.assertEqual([1], xs)
