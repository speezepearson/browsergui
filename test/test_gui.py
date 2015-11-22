import threading
import contextlib
import time
from browsergui import GUI, Text, Button, Event, Click

from . import BrowserGUITestCase


class GUITest(BrowserGUITestCase):

  def run_quietly(self, gui):
    gui.run(quiet=True, open_browser=False)

  @contextlib.contextmanager
  def running_in_background(self, gui, stop_running=True):
    t = threading.Thread(target=self.run_quietly, args=[gui])
    t.start()
    time.sleep(0.01) # give server time to boot up
    yield
    if stop_running:
      gui.stop_running()
    t.join(0.01) # give server time to shut down
    if t.is_alive():
      raise AssertionError('gui did not stop running')

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
    button.callback = (lambda: xs.append(1))

    gui = GUI(decoy1, button, decoy2)

    gui.dispatch_event(Click(target_id=button.id))
    self.assertEqual([1], xs)

  def test_run(self):
    # Just make sure that modifications before/during/after runs don't blow up,
    # and that stop_running() terminates the run()-thread.
    gui = GUI(Text('before first run'))

    with self.running_in_background(gui):
      gui.body.append(Text('during first run'))

    gui.body.append(Text('before second fun'))

    with self.running_in_background(gui):
      gui.body.append(Text('during second run'))

  def test_run__raises_if_running(self):
    gui = GUI()

    with self.running_in_background(gui):
      with self.assertRaises(RuntimeError):
        self.run_quietly(gui)

  def test_stop_running__raises_if_not_running(self):
    gui = GUI()
    with self.assertRaises(RuntimeError):
      gui.stop_running()

    # Also make sure it raises if the GUI ran in the past, but then stopped.
    with self.running_in_background(gui):
      pass
    with self.assertRaises(RuntimeError):
      gui.stop_running()
