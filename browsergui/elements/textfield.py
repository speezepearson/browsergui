from .input_field import InputField
from ..pythoncompatibility import STRING_TYPES

class TextField(InputField):
  def __init__(self, value='', **kwargs):
    super(TextField, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'text')

  def ensure_is_valid_value(self, value):
    if not isinstance(value, STRING_TYPES):
      raise TypeError('expected value to be str (or None), got {}'.format(type(value).__name__))
    super(TextField, self).ensure_is_valid_value(value)
