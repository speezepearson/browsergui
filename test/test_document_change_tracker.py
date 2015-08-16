import unittest
import xml.dom.minidom
import threading
import time
from browsergui.documentchangetracker import *

class DocumentChangeTrackerTest(unittest.TestCase):
  def setUp(self):
    self.document = xml.dom.minidom.parseString('<root id="root" />')
    self.root = self.document.documentElement
    self.tracker = DocumentChangeTracker(self.document)

  def test_mark_dirty_awakens_waiting_threads(self):
    t = threading.Thread(target=self.tracker.flush_changes)
    t.start()
    time.sleep(0.01)
    self.tracker.mark_dirty(self.root)
    t.join()

  def test_flush_changes_doesnt_wait_if_already_dirty(self):
    self.tracker.mark_dirty(self.root)
    self.tracker.flush_changes()

  def test_mark_dirty__parent_overrides_child(self):
    e = self.document.createElement('floozle')
    e.setAttribute('id', 'floozle')
    self.root.appendChild(e)

    self.tracker.mark_dirty(e)
    self.tracker.mark_dirty(self.root)
    changes = self.tracker.flush_changes()
    self.assertIn('getElementById("root")', changes)
    self.assertNotIn('getElementById("floozle")', changes)

    self.tracker.mark_dirty(self.root)
    self.tracker.mark_dirty(e)
    changes = self.tracker.flush_changes()
    self.assertIn('getElementById("root")', changes)
    self.assertNotIn('getElementById("floozle")', changes)
