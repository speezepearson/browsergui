import numbers
import math
from .input_field import InputField

class IntegerSlider(InputField):

  def __init__(self, value=None, min=0, max=100, **kwargs):
    if not isinstance(min, int):
      raise TypeError('min must be int, not {}'.format(type(min).__name__))
    if not isinstance(max, int):
      raise TypeError('max must be int, not {}'.format(type(max).__name__))

    if value is None:
      value = (min+max)//2

    self._min = min
    self._max = max
    super(IntegerSlider, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'range')
    self.tag.setAttribute('step', '1')
    self.max = max
    self.min = min

  @property
  def min(self):
    return self._min
  @min.setter
  def min(self, new_min):
    if not isinstance(new_min, int):
      raise TypeError('min must be int, not {}'.format(type(new_min).__name__))
    if new_min > self.value:
      raise ValueError("can't set min to above current value")
    self._min = new_min
    self.tag.setAttribute('min', repr(new_min))
    self.mark_dirty()

  @property
  def max(self):
    return self._max
  @max.setter
  def max(self, new_max):
    if not isinstance(new_max, int):
      raise TypeError('max must be int, not {}'.format(type(new_max).__name__))
    if new_max < self.value:
      raise ValueError("can't set max to below current value")
    self._max = new_max
    self.tag.setAttribute('max', repr(new_max))
    self.mark_dirty()

  def value_from_xml_string(self, s):
    return int(s) if s else None

  def value_to_xml_string(self, x):
    return '' if x is None else repr(int(x))

  def ensure_is_valid_value(self, value):
    if not isinstance(value, int):
      raise TypeError('expected integer value, got {}'.format(type(value).__name__))

    if (value < self.min) or (value > self.max):
      raise ValueError('{} not between {} and {}'.format(value, self.min, self.max))

    super(IntegerSlider, self).ensure_is_valid_value(value)
