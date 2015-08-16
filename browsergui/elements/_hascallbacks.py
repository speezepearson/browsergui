import collections
from ._hasgui import HasGUI
from ._hastag import HasTag

class NoSuchCallbackError(Exception):
  """Raised when trying to remove a nonexistent callback from an Element."""
  pass

class HasCallbacks(HasGUI, HasTag):
  def __init__(self, **kwargs):
    super(HasCallbacks, self).__init__(**kwargs)
    self.callbacks = collections.defaultdict(list)

  def add_callback(self, event_type, callback):
    """Arranges for ``callback`` to be called whenever the Element handles an event of ``event_type``.

    :type event_type: str
    :type callback: a function of one argument (the event being handled)
    """
    self.callbacks[event_type].append(callback)
    event_type.enable_server_notification(self.tag)
    self.mark_dirty()

  def remove_callback(self, event_type, callback):
    """Stops calling ``callback`` when events of ``event_type`` are handled.

    For parameter information, see :func:`add_callback`.
    """
    if callback not in self.callbacks[event_type]:
      raise NoSuchCallbackError(event_type, callback)

    self.callbacks[event_type].remove(callback)

    if not self.callbacks[event_type]:
      event_type.disable_server_notification(self.tag)
      self.mark_dirty()

  def handle_event(self, event):
    """Calls all the callbacks registered for the given event's type.

    :param Event event:
    """
    for callback_event_class, callbacks in self.callbacks.items():
      if isinstance(event, callback_event_class):
        for callback in callbacks:
          callback(event)
