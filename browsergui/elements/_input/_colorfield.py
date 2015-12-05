import types
import numbers
import re
from .. import NotUniversallySupportedElement
from ._inputfield import InputField
from ..._pythoncompatibility import collections_abc

class ColorField(InputField, NotUniversallySupportedElement):
  '''A field where the user can input a RGB color.

  Inherits from :class:`ValuedElement`, meaning it has a ``value``, ``placeholder``, and ``change_callback``.
  '''
  def __init__(self, value=(0, 0, 0), placeholder='#xxxxxx', **kwargs):
    super(ColorField, self).__init__(value=value, placeholder=placeholder, **kwargs)
    self.tag.setAttribute('type', 'color')

  def _value_to_xml_string(self, value):
    if isinstance(value, collections_abc.Sequence):
      r, g, b = value
      for x in (r, g, b):
        if not isinstance(x, numbers.Integral):
          raise TypeError('color triplet must consist of integers, not {}'.format(type(x).__name__))
        if not 0 <= x <= 255:
          raise ValueError('color triplet values must be between 0 and 255 (got {})'.format(repr(x)))
      return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    raise TypeError("expected sequence, got {}".format(type(value).__name__))

  def _value_from_xml_string(self, string):
    if re.match(r'#[0-9a-f]{6}', string):
      return tuple(int(hex_repr, 16) for hex_repr in (string[1:3], string[3:5], string[5:7]))
    raise ValueError('malformed hex color: {!r}'.format(string))
