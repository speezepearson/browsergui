import numbers
import math
from .input_field import InputField

class Slider(InputField):
  '''A continuously draggable slider.

  Useful attributes:

  - ``slider.min`` is the smallest number the slider can be set to. Writable.
  - ``slider.max`` is the largest number the slider can be set to. Writable.

  ``min``, ``max``, or ``value`` can be set to any real number (e.g. float, int, ``fractions.Fraction``), but any attempted assignment that would violate ``min <= value <= max`` will fail and instead raise a ``ValueError``. When the user drags the slider, the value is set to a float.

  :param min: the smallest value the slider can accept
  :param max: the largest value the slider can accept
  '''

  def __init__(self, min, max, value=None, **kwargs):
    if value is None:
      value = (min+max)/2

    self._min = min
    self._max = max
    super(Slider, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'range')
    self.tag.setAttribute('step', str((self.max-self.min)/1000.))
    self.max = max
    self.min = min

  @property
  def min(self):
    return self._min
  @min.setter
  def min(self, new_min):
    if new_min > self.value:
      raise ValueError("can't set min to above current value")
    self._min = new_min
    self.tag.setAttribute('min', repr(float(new_min)))
    self.mark_dirty()

  @property
  def max(self):
    return self._max
  @max.setter
  def max(self, new_max):
    if new_max < self.value:
      raise ValueError("can't set max to below current value")
    self._max = new_max
    self.tag.setAttribute('max', repr(float(new_max)))
    self.mark_dirty()

  def value_from_xml_string(self, s):
    return float(s) if s else None

  def value_to_xml_string(self, x):
    return '' if x is None else repr(float(x))

  def ensure_is_valid_value(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('expected real-number value, got {}'.format(type(value).__name__))

    if math.isnan(value):
      raise TypeError('expected real-number value, got NaN')

    if (value < self.min) or (value > self.max):
      raise ValueError('{} not between {} and {}'.format(value, self.min, self.max))

    super(Slider, self).ensure_is_valid_value(value)
