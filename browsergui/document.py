import threading
import json

class Destroyed(Exception):
  pass

class DocumentChangeTracker(object):
  def __init__(self, document, **kwargs):
    self.document = document
    super(DocumentChangeTracker, self).__init__(**kwargs)

    self._mutex = threading.RLock()
    self._changed_condition = threading.Condition(self._mutex)
    self._dirty = True
    self._destroyed = False

  def destroy(self):
    with self._mutex:
      self._destroyed = True
      self._changed_condition.notify_all()

  def flush_changes(self):
    with self._changed_condition:
      self._changed_condition.wait_for(lambda: self._dirty or self._destroyed)
      if self._destroyed:
        raise Destroyed(self)
      self._dirty = False
      innerHTML = ''.join(tag.toxml() for tag in self.document.documentElement.childNodes)
      return 'document.documentElement.innerHTML = {innerHTML}'.format(innerHTML=json.dumps(innerHTML))

  def mark_dirty(self):
    with self._changed_condition:
      self._dirty = True
      self._changed_condition.notify()
