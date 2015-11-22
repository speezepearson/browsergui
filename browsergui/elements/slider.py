import numbers
import math
from .input_field import InputField

class Slider(InputField):
  '''A draggable slider.

  Any attempted assignment to ``min``, ``max``, or ``value`` that would violate ``min <= value <= max`` will fail and instead raise a ``ValueError``.

  :param min: the smallest value the slider can accept. Writable.
  :param max: the largest value the slider can accept. Writable.

  I think :class:`ContinuousSlider` and :class:`IntegerSlider` are probably the only subclasses you'll ever need, but in case you write your own subclass, it must define:

  - ``value_to_xml_string(x)``: convert a value to a string (string should be a number)
  - ``value_from_xml_string(s)``: inverse of ``value_to_xml_string``
  - ``_step(min, max)``: step the value should take in the browser
  - ``_default_value(min, max)``: value to take during initialization if none specified
  - ``typecheck_value_or_bound(x)``: raise ``TypeError`` if a value isn't suitable for a value or bound
  '''

  def __init__(self, min, max, value=None, **kwargs):
    if value is None:
      value = self._default_value(min, max)

    self._min = min
    self._max = max
    super(Slider, self).__init__(value=value, **kwargs)
    self.max = max
    self.min = min

    self.tag.setAttribute('type', 'range')
    self.tag.setAttribute('step', str(self._step(min, max)))

  @property
  def min(self):
    return self._min
  @min.setter
  def min(self, new_min):
    self.typecheck_value_or_bound(new_min)
    if new_min > self.value:
      raise ValueError("can't set min to above current value")
    self._min = new_min
    self.tag.setAttribute('min', self.value_to_xml_string(new_min))
    self.mark_dirty()

  @property
  def max(self):
    return self._max
  @max.setter
  def max(self, new_max):
    self.typecheck_value_or_bound(new_max)
    if new_max < self.value:
      raise ValueError("can't set max to below current value")
    self._max = new_max
    self.tag.setAttribute('max', self.value_to_xml_string(new_max))
    self.mark_dirty()

  def ensure_is_valid_value(self, value):
    self.typecheck_value_or_bound(value)

    if (value < self.min) or (value > self.max):
      raise ValueError('{} not between {} and {}'.format(value, self.min, self.max))

    super(Slider, self).ensure_is_valid_value(value)

  @classmethod
  def _step(cls, min, max):
    raise NotImplementedError('{} does not implement _step'.format(cls.__name__))
  @classmethod
  def _default_value(cls, min, max):
    raise NotImplementedError('{} does not implement _default_value'.format(cls.__name__))
  @classmethod
  def typecheck_value_or_bound(cls, x):
    raise NotImplementedError('{} does not implement typecheck_value_or_bound'.format(cls.__name__))

class ContinuousSlider(Slider):
  '''A type of :class:`Slider` that accepts real-valued values/bounds (e.g. float, int, ``fractions.Fraction``).

  When the user drags the slider, the value is set to a float.
  '''

  @staticmethod
  def value_from_xml_string(s):
    return float(s)

  @staticmethod
  def value_to_xml_string(x):
    return repr(float(x))

  @staticmethod
  def _step(min, max):
    return (max-min) / 1000.

  @staticmethod
  def _default_value(min, max):
    return (min+max) / 2.

  @staticmethod
  def typecheck_value_or_bound(x):
    if not isinstance(x, numbers.Real):
      raise TypeError('expected real-number value, got {}'.format(type(x).__name__))
    if math.isnan(x):
      raise TypeError('expected real-number value, got NaN')

class IntegerSlider(Slider):
  '''A type of :class:`Slider` that accepts only integer values/bounds.'''

  @staticmethod
  def value_from_xml_string(s):
    return int(s)

  @staticmethod
  def value_to_xml_string(x):
    return '{:d}'.format(x)

  @staticmethod
  def _step(min, max):
    return 1

  @staticmethod
  def _default_value(min, max):
    return (min+max) // 2

  @staticmethod
  def typecheck_value_or_bound(x):
    if not isinstance(x, int):
      raise TypeError('expected int value, got {}'.format(type(x).__name__))
