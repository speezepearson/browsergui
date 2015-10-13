import collections

class CallbackSetter(collections.MutableMapping):
  def __init__(self, element, **kwargs):
    self.callbacks = {}
    self.element = element
    super(CallbackSetter, self).__init__(**kwargs)

  def __getitem__(self, key):
    return self.callbacks[key]

  def __setitem__(self, key, value):
    self.callbacks[key] = value
    key.enable_server_notification(self.element.tag)
    self.element.mark_dirty()

  def __delitem__(self, key):
    del self.callbacks[key]
    key.disable_server_notification(self.element.tag)
    self.element.mark_dirty()

  def __iter__(self):
    return iter(self.callbacks)

  def __len__(self):
    return len(self.callbacks)
