from . import LeafElement
from ..events import Input

class TextField(LeafElement):
  def __init__(self, value='', placeholder='', change_callback=None, **kwargs):
    super(TextField, self).__init__(tag_name="input", **kwargs)
    self.tag.setAttribute('type', 'text')

    self.value = value
    self.placeholder = placeholder

    self.add_callback(Input, self._handle_contents_change_event)
    if change_callback is not None:
      self.add_callback(Input, (lambda event: change_callback()))

  @property
  def value(self):
    return self.tag.getAttribute('value')
  @value.setter
  def value(self, value):
    self.tag.setAttribute('value', value)
    self.mark_dirty()
    self.handle_event(Input(target_id=self.id, value=self.value))

  @property
  def placeholder(self):
    return self.tag.getAttribute('placeholder')
  @placeholder.setter
  def placeholder(self, placeholder):
    self.tag.setAttribute('placeholder', placeholder)
    self.mark_dirty()

  def _handle_contents_change_event(self, event):
    self.tag.setAttribute('value', event.value)
