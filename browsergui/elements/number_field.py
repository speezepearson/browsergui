import numbers
from .input_field import InputField

class NumberField(InputField):

  def __init__(self, value=None, **kwargs):
    if value is not None:
      value = float(value)
    super(NumberField, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'number')

  def value_from_xml_string(self, s):
    return float(s) if s else None

  def value_to_xml_string(self, x):
    return '' if x is None else repr(float(x))

  def ensure_is_valid_value(self, value):
    if not (value is None or isinstance(value, numbers.Real)):
      raise TypeError('expected real-number value (or None), got {}'.format(type(value).__name__))
    super(NumberField, self).ensure_is_valid_value(value)
