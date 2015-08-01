from browsergui import GUI, Text, Button, CLICK

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

    event = {'type': CLICK, 'id': button.id}
    gui.dispatch_event({'type': CLICK, 'id': button.id})
    self.assertEqual([1], xs)

  def test_send_command(self):
    gui = GUI()
    stream = gui.command_broadcaster.create_stream()

    gui.send_command("foo")
    self.assertEqual("foo", stream.get(block=False))
    self.assertTrue(stream.empty())
