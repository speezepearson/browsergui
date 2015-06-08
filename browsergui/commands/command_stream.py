import sys
if sys.version_info >= (3, 3):
  from time import monotonic as time
else:
  from time import time

import threading

class Empty(Exception):
  """Raised by ``CommandStream.get(block=False)``"""
  pass

class Destroyed(Exception):
  """Raised when trying to get/put on a destroyed :class:`CommandStream`"""
  pass

class CommandStream(object):
  def __init__(self):
    """A thread-safe stream of JavaScript commands.

    Commands (strings) may be put into the stream with ``put``;
    ``get`` will gather up all the commands since the last ``get``,
    compound them into a single string, and return it. Streams
    may be ``destroy``ed, causing all pending/future calls to ``get``
    or ``put`` to raise ``Destroyed``.

    The implementation is a slimmed-down version of the standard library's
    ``queue`` module, except with the :func:`destroy` method added,
    allowing waiting threads to be interrupted.
    """
    self.commands = []
    self.destroyed = False
    self.mutex = threading.Lock()
    self.not_empty = threading.Condition(self.mutex)

  def empty(self):
    return not self.commands

  def destroy(self):
    """Causes all pending/future calls to ``get`` or ``put`` to raise ``Destroyed``."""
    with self.mutex:
      self.destroyed = True

  def put(self, value):
    """Enqueue a snippet of JavaScript for the next ``get``.

    Raises ``Destroyed`` if the queue has been destroyed.
    """
    with self.mutex:
      if self.destroyed:
        raise Destroyed
      self.commands.append(value)
      self.not_empty.notify()

  def get(self, block=True, timeout=None):
    """Return all the commands ``put`` into the stream as a single string.

    ``block`` and ``timeout`` function just like for the standard library's
    :func:`queue.Queue.get`.

    Raises ``Destroyed`` if the stream has been destroyed, or if it's destroyed
    while the call is blocking.
    """
    with self.not_empty:
      if not block:
        if self.empty():
          raise Empty
      elif timeout is None:
        while self.empty():
          self.not_empty.wait()
      elif timeout < 0:
        raise ValueError("'timeout' must be a non-negative number")
      else:
        endtime = time() + timeout
        while self.empty() and not self.destroyed:
          remaining = endtime - time()
          if remaining <= 0.0:
            raise Empty
          self.not_empty.wait(remaining)
      
      if self.destroyed:
        raise Destroyed
      
      item = self._get()
      return item

  def _get(self):
      result = "; ".join(self.commands)
      self.commands = []
      return result


