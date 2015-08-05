import time
import threading

class RepeatingTimer(object):
  def __init__(self, interval, callback, timer_args=(), timer_kwargs={}, daemon=False, **kwargs):
    super(RepeatingTimer, self).__init__(**kwargs)
    self.interval = interval
    self.callback = callback
    self.daemon = daemon
    self.started = False
    self.cancelled = False

    self._mutex = threading.Lock()
    self._timer_args = timer_args
    self._timer_kwargs = timer_kwargs
    self._timer = self._make_timer()

  def start(self):
    with self._mutex:
      if self.started:
        raise RuntimeError('threads can only be started once')
      self._timer.start()
      self.started = True

  def cancel(self):
    with self._mutex:
      self.cancelled = True

  def _make_timer(self):
    result = threading.Timer(self.interval, self._timer_callback, *self._timer_args, **self._timer_kwargs)
    result.daemon = self.daemon
    return result

  def _timer_callback(self, *args, **kwargs):
    self.callback(*args, **kwargs)
    with self._mutex:
      if not self.cancelled:
        self._timer = self._make_timer()
        self._timer.start()

def call_in_background(callback, args=(), kwargs={}, daemon=False):
  t = threading.Thread(target=callback, args=args, kwargs=kwargs)
  t.daemon = daemon
  t.start()
