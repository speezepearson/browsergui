import collections

class NoSuchCallbackError(Exception):
  """Raised when trying to remove a nonexistent callback from an Element."""
  pass

def _javascript_to_notify_server(element, event_type):
  return """
    notify_server({{
      type: '{type}',
      id: '{id}'
    }})""".format(
      type=event_type,
      id=element.id)

class HasCallbacks(object):
  def __init__(self, **kwargs):
    super(HasCallbacks, self).__init__(**kwargs)
    self.callbacks = collections.defaultdict(list)

  def add_callback(self, event_type, callback):
    """Arranges for ``callback`` to be called whenever the Element handles an event of ``event_type``.

    :type event_type: str
    :type callback: a function of one argument (the event being handled)
    """
    self.callbacks[event_type].append(callback)
    self.tag.setAttribute('on'+event_type, _javascript_to_notify_server(self, event_type))
    self.mark_dirty()

  def remove_callback(self, event_type, callback):
    """Stops calling ``callback`` when events of ``event_type`` are handled.

    For parameter information, see :func:`add_callback`.
    """
    if callback not in self.callbacks[event_type]:
      raise NoSuchCallbackError(event_type, callback)

    self.callbacks[event_type].remove(callback)

    if not self.callbacks[event_type]:
      self.tag.removeAttribute('on'+event_type)
      self.mark_dirty()

  def handle_event(self, event):
    """Calls all the callbacks registered for the given event's type.

    :type event: dict
    """
    for callback in self.callbacks[event['type']]:
      callback(event)
