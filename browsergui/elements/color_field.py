import types
import numbers
import re
from . import NotUniversallySupportedElement
from .input_field import InputField

class ColorField(InputField, NotUniversallySupportedElement):
  def __init__(self, value=(0, 0, 0), placeholder='#xxxxxx', **kwargs):
    super(ColorField, self).__init__(value=value, placeholder=placeholder, **kwargs)
    self.tag.setAttribute('type', 'color')

  @staticmethod
  def value_from_xml_string(s):
    # Kludge incoming.
    # Some browsers don't support date-input fields, and display them as text instead.
    # We still get notified about changes, but the reported value might be malformed.
    # In this case, we might get '#f0f0' as a value, which should not be accepted.
    # So we throw an error here.
    if not re.match(r'#[0-9a-f]{6}', s):
      raise ValueError('malformed hex color: {!r}'.format(s))
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
