import threading
import json

class Destroyed(Exception):
  '''Raised when trying to operate on a destroyed DocumentChangeTracker.'''
  pass

class DocumentChangeTracker(object):
  '''Provides JavaScript to help a browser keep its document up to date with a local one.

  Intended use case: there's a locally stored XML document, and there's another document
  stored in a browser window. The browser wants to execute some JavaScript to make its
  document look like the one on the server, so it makes a request to the server.
  The server should wait until a change is made to the local document (if necessary),
  then respond with the appropriate JS to apply the change to the remote document.

  How it works: the DocumentChangeTracker is instantiated, being given an XML document.
  It keeps track of whether the document is "clean" or "dirty" (i.e. whether there have been
  changes since the last time the browser was brought up to date).

  The :func:`flush_changes` method waits until the document is dirty (if necessary),
  marks the document as clean, and returns a JavaScript string that will bring the browser's
  DOM up to date.

  The :func:`mark_dirty` method marks the document as dirty, possibly waking up threads
  waiting on :func:`flush_changes`.

  The :func:`destroy` method wakes up all waiting threads, but causes them to return
  JavaScript that will close the browser window.
  '''
  def __init__(self, document, **kwargs):
    self.document = document
    super(DocumentChangeTracker, self).__init__(**kwargs)

    self._mutex = threading.RLock()
    self._changed_condition = threading.Condition(self._mutex)
    self._dirty = True
    self._destroyed = False

  def destroy(self):
    '''Wake up waiting threads and give them JS to close the browser window.'''
    with self._mutex:
      self._destroyed = True
      self._changed_condition.notify_all()

  def flush_changes(self):
    '''Wait until the document is dirty, then return JS to bring a browser up to date.

    :returns: str
    '''
    with self._changed_condition:
      self._changed_condition.wait_for(lambda: self._dirty or self._destroyed)
      if self._destroyed:
        return 'window.close(); sleep(9999)'
      self._dirty = False
      innerHTML = ''.join(tag.toxml() for tag in self.document.documentElement.childNodes)
      return 'document.documentElement.innerHTML = {innerHTML}'.format(innerHTML=json.dumps(innerHTML))

  def mark_dirty(self):
    '''Mark the document as dirty, waking up calls to :func:`flush_changes`'''
    with self._changed_condition:
      if self._destroyed:
        raise Destroyed(self)
      self._dirty = True
      self._changed_condition.notify_all()
