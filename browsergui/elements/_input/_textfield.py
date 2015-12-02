from ._inputfield import InputField
from ..._pythoncompatibility import STRING_TYPES

class TextField(InputField):
  '''A single-line text input field.

  For multi-line text input, see :class:`BigTextField`, which has a very similar interface.
  '''
  def __init__(self, value='', **kwargs):
    super(TextField, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'text')

  def ensure_is_valid_value(self, value):
    if not isinstance(value, STRING_TYPES):
      raise TypeError('expected value to be str (or None), got {}'.format(type(value).__name__))
    super(TextField, self).ensure_is_valid_value(value)
