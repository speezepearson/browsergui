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

  def test_command_stream(self):
    gui = GUI()
    stream = gui.command_stream()

    while not stream.empty():
      stream.get(block=False)

    gui.send_command("foo")
    self.assertEqual("foo", stream.get(block=False))
    self.assertTrue(stream.empty())

    stream2 = gui.command_stream()
    while not stream2.empty():
      stream2.get(block=False)

    gui.send_command("bar")
    self.assertEqual("bar", stream.get(block=False))
    self.assertTrue(stream.empty())
    self.assertEqual("bar", stream2.get(block=False))
    self.assertTrue(stream2.empty())

  def test_callbacks_produce_commands(self):
    button_with_predefined_callback = Button(callback=(lambda: None))
    button_with_later_callback = Button()
    gui = GUI(button_with_predefined_callback, button_with_later_callback)
    stream = gui.command_stream()

    self.assertIn(button_with_predefined_callback.id, stream.get(block=False))
    self.assertTrue(stream.empty())

    button_with_later_callback.set_callback(lambda: None)
    self.assertIn(button_with_later_callback.id, stream.get(block=False))
    self.assertTrue(stream.empty())
