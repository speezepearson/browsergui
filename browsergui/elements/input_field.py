from . import LeafElement
from ..events import Input

class InputField(LeafElement):
  def __init__(self, tag_name='input', value=None, change_callback=None, **kwargs):
    self.set_cached_value(value)
    super(InputField, self).__init__(tag_name=tag_name, **kwargs)
    self.update_tag_with_cached_value()

    self.add_callback(Input, lambda event: self.set_cached_value(event.value))
    if change_callback is not None:
      self.add_callback(Input, (lambda event: change_callback()))

  @property
  def value(self):
    return self.cached_value
  @value.setter
  def value(self, value):
    self.set_cached_value(value)
    self.handle_event(Input(target_id=self.id, value=self.value))
    self.mark_dirty()

  def mark_dirty(self):
    self.update_tag_with_cached_value()
    super(InputField, self).mark_dirty()

  def update_tag_with_cached_value(self):
    self.tag.setAttribute('value', self.cached_value)

  def set_cached_value(self, value):
    self.cached_value = value
