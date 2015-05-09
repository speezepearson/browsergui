import re
import unittest
import contextlib

class BrowserGUITestCase(unittest.TestCase):
  def setUp(self):
    self.last_event = None

  def set_last_event(self, event):
    self.last_event = event

  @contextlib.contextmanager
  def assertSetsEvent(self, event):
    self.last_event = None
    yield
    self.assertEqual(event, self.last_event)

  def assertHTMLIn(self, included, html):
    self.assertIn(re.sub("\s", "", included), re.sub("\s", "", html))

  def assertVeryEqual(self, x, y):
    self.assertEqual(x, y)
    self.assertEqual(hash(x), hash(y))