class GUITest(unittest.TestCase):
  def setUp(self):
    self.last_event = None

  def set_last_event(self, event):
    self.last_event = event

  @contextlib.contextmanager
  def assertSetsEvent(self, event):
    self.last_event = None
    yield
    self.assertEqual(event, self.last_event)

  def test_construction(self):
    gui = GUI()

    GUI(Text("left"), Text("hi"))

    with self.assertRaises(TypeError):
      gui = GUI(0)

  def test_event_dispatch(self):
    decoy1 = Button()
    button = Button()
    decoy2 = Button()
    button.set_callback(self.set_last_event)

    gui = GUI(decoy1, button, decoy2)

    event = {'type': CLICK, 'id': button.id}
    with self.assertSetsEvent(event):
      gui.handle_event(event)

  def test_command_queue(self):
    gui = GUI()
    self.assertTrue(gui.command_queue.empty())
    gui.send_js_command("foo");
    self.assertEqual("foo", gui.get_js_command())
    with self.assertRaises(destructiblequeue.Empty):
      gui.get_js_command(block=False)

  def test_callbacks_produce_commands(self):
    button_with_predefined_callback = Button(callback=(lambda event: None))
    button_with_later_callback = Button()
    gui = GUI(button_with_predefined_callback, button_with_later_callback)

    self.assertIn(button_with_predefined_callback.id, gui.get_js_command(block=False))
    self.assertTrue(gui.command_queue.empty())

    button.set_callback(lambda event: None)
    self.assertIn(button_with_later_callback.id, gui.get_js_command(block=False))
    self.assertTrue(gui.command_queue.empty())
