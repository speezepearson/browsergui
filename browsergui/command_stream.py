import sys
if sys.version_info >= (3, 0):
  from time import monotonic as time
else:
  from time import time

import threading

class Empty(Exception):
  """Raised by CommandStream.get(block=False)"""
  pass

class Destroyed(Exception):
  """Raised when trying to get/put on a destroyed CommandStream"""
  pass

class CommandStream(object):
  def __init__(self):
    self.commands = []
    self.destroyed = False
    self.mutex = threading.Lock()
    self.not_empty = threading.Condition(self.mutex)

  def empty(self):
    return not self.commands

  def destroy(self):
    with self.mutex:
      self.destroyed = True

  def put(self, value):
    with self.mutex:
      if self.destroyed:
        raise Destroyed
      self.commands.append(value)
      self.not_empty.notify()

  def get(self, block=True, timeout=None):
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


