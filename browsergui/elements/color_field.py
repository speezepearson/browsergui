import numbers
import logging
from .input_field import InputField

logger = logging.Logger('browsergui.ColorField')

def ensure_is_legal_color_triplet(rgb):
  r, g, b = rgb
  for x in (r, g, b):
    if not isinstance(x, numbers.Integral):
      raise TypeError('color triplet must consist of integers, not {}'.format(type(x).__name__))
    if not 0 <= x < 256:
      raise ValueError('color triplet values must be between 0 and 256 (got {})'.format(repr(x)))

class ColorField(InputField):

  warn_about_potential_browser_incompatibility = True

  def __init__(self, value=None, **kwargs):
    if value is None:
      value = (0, 0, 0)

    ensure_is_legal_color_triplet(value)
    super(ColorField, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'color')

    if self.warn_about_potential_browser_incompatibility:
      logger.warning('ColorField not supported in all major browsers (as of August 2015)')

  @staticmethod
  def value_from_xml_string(s):
    if not s:
      return None
    return tuple(int(hex_repr, 16) for hex_repr in (s[1:3], s[3:5], s[5:7]))

  @staticmethod
  def value_to_xml_string(value):
    ensure_is_legal_color_triplet(value)
    return '' if value is None else '#{:02x}{:02x}{:02x}'.format(*value)
