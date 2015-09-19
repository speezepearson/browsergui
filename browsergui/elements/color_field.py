import types
import numbers
from . import NotUniversallySupportedElement
from .input_field import InputField

class ColorField(InputField, NotUniversallySupportedElement):
  def __init__(self, value=None, **kwargs):
    if value is None:
      value = (0, 0, 0)

    super(ColorField, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'color')

  @staticmethod
  def value_from_xml_string(s):
    return tuple(int(hex_repr, 16) for hex_repr in (s[1:3], s[3:5], s[5:7]))

  @staticmethod
  def value_to_xml_string(value):
    return '#{:02x}{:02x}{:02x}'.format(*value)

  def ensure_is_valid_value(self, rgb):
    if isinstance(rgb, types.GeneratorType):
      raise TypeError('use types like lists/tuples, not generators, for color triplets')

    r, g, b = rgb
    for x in (r, g, b):
      if not isinstance(x, numbers.Integral):
        raise TypeError('color triplet must consist of integers, not {}'.format(type(x).__name__))
      if not 0 <= x < 256:
        raise ValueError('color triplet values must be between 0 and 256 (got {})'.format(repr(x)))

    super(ColorField, self).ensure_is_valid_value(rgb)
