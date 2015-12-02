from .. import Element
from ...events import Input
from ..._pythoncompatibility import STRING_TYPES

class BigTextField(Element):
  '''A multi-line text field.

  Like :class:`InputField` elements, has a ``value``, a ``placeholder``, and a ``change_callback``.
  '''
  def __init__(self, value='', placeholder='', change_callback=None, **kwargs):
    super(BigTextField, self).__init__(tag_name='textarea', **kwargs)
    self._text_node = self.tag.ownerDocument.createTextNode('')
    self.tag.appendChild(self._text_node)
    self.placeholder = placeholder
    self.callbacks[Input] = self._handle_input_event

    self.change_callback = None
    self.value = value
    self.change_callback = change_callback

  @property
  def value(self):
    return self._text_node.data
  @value.setter
  def value(self, value):
    if not any(isinstance(value, t) for t in STRING_TYPES):
      raise TypeError('expected str, got {}'.format(type(value).__name__))
    self._set_value(value)
    self.mark_dirty()

  @property
  def placeholder(self):
    return self.tag.getAttribute('placeholder')
  @placeholder.setter
  def placeholder(self, placeholder):
    if not isinstance(placeholder, STRING_TYPES):
      raise TypeError('expected str, got {}'.format(type(placeholder).__name__))
    self.tag.setAttribute('placeholder', placeholder)
    self.mark_dirty()

  def _handle_input_event(self, event):
    self._set_value(event.value)

  def def_change_callback(self, f):
    self.change_callback = f
    return f

  def ensure_is_valid_value(self, value):
    if not isinstance(value, STRING_TYPES):
      raise TypeError('expected value to be str (or None), got {}'.format(type(value).__name__))
    super(BigTextField, self).ensure_is_valid_value(value)

  def _set_value(self, value):
    if not isinstance(value, STRING_TYPES):
      raise TypeError('expected str, got {}'.format(type(value).__name__))
    self._text_node.data = value
    if self.change_callback is not None:
      self.change_callback()
