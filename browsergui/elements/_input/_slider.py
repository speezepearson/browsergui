import numbers
import datetime
from ._inputfield import InputField
from ..._pythoncompatibility import is_real_float

class Slider(InputField):
  '''A draggable slider.

  Any attempted assignment to ``min``, ``max``, or ``value`` that would violate ``min <= value <= max`` will fail and instead raise a ``ValueError``.

  Don't instantiate; you probably want :class:`FloatSlider` or :class:`IntegerSlider`. You can also define your own subclasses for other data types: see `this tutorial`_.

  .. _this tutorial: https://github.com/speezepearson/browsergui/wiki/Make-Your-Own-Sliders

  :param min: the smallest value the slider can accept. Writable.
  :param max: the largest value the slider can accept. Writable.
  '''

  DISCRETE = False

  def __init__(self, min, max, value=None, **kwargs):
    if value is None:
      value = type(self).value_from_number((type(self).value_to_number(min)+type(self).value_to_number(max)) / 2.0)

    self._min = min
    self._max = max
    super(Slider, self).__init__(value=value, **kwargs)
    self.max = max
    self.min = min

    self.tag.setAttribute('type', 'range')
    self.tag.setAttribute('step', str(1 if type(self).DISCRETE else (self.value_to_number(max)-self.value_to_number(min))/1000.))

  @property
  def min(self):
    return self._min
  @min.setter
  def min(self, new_min):
    new_min_number = self.value_to_number(new_min)
    if new_min > self.value:
      raise ValueError("can't set min to above current value")
    self._min = new_min
    self.tag.setAttribute('min', str(new_min_number))
    self.mark_dirty()

  @property
  def max(self):
    return self._max
  @max.setter
  def max(self, new_max):
    new_max_number = self.value_to_number(new_max)
    if new_max < self.value:
      raise ValueError("can't set max to below current value")
    self._max = new_max
    self.tag.setAttribute('max', str(new_max_number))
    self.mark_dirty()

  def _value_to_xml_string(self, value):
    self.value_to_number(value)
    if (value < self.min) or (value > self.max):
      raise ValueError('{} not between {} and {}'.format(value, self.min, self.max))
    return repr(self.value_to_number(value))

  def _value_from_xml_string(self, value):
    return self.value_from_number(float(value))

  def value_to_number(self, x):
    raise NotImplementedError('{} has not implemented value_to_number'.format(type(self).__name__))

  def value_from_number(self, x):
    raise NotImplementedError('{} has not implemented value_from_number'.format(type(self).__name__))

class FloatSlider(Slider):
  '''A type of :class:`Slider` that accepts real-valued values/bounds (e.g. float, int, ``fractions.Fraction``).

  When the user drags the slider, the value is set to a float.
  '''

  @staticmethod
  def value_to_number(x):
    if not isinstance(x, numbers.Real):
      raise TypeError('expected real number, got {}'.format(type(x).__name__))
    result = float(x)
    if not is_real_float(result):
      raise TypeError('expected finite value, got {}'.format(result))
    return result

  @staticmethod
  def value_from_number(x):
    return x

class IntegerSlider(Slider):
  '''A type of :class:`Slider` that accepts only integer values/bounds.'''

  DISCRETE = True

  @staticmethod
  def value_to_number(x):
    if not isinstance(x, int):
      raise TypeError('expected int, got {}'.format(type(x).__name__))
    return x

  @staticmethod
  def value_from_number(x):
    return int(x)
