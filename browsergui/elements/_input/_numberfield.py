import numbers
from ._inputfield import InputField

class NumberField(InputField):
  '''A field where the user can input a real number.

  Inherits from :class:`ValuedElement`, meaning it has a ``value``, ``placeholder``, and ``change_callback``.
  '''

  def __init__(self, value=None, **kwargs):
    if value is not None:
      value = float(value)
    super(NumberField, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'number')

  def _value_to_xml_string(self, value):
    if value is None:
      return ''
    elif isinstance(value, numbers.Real):
      return repr(value)
    raise TypeError('expected real-number value (or None), got {}'.format(type(value).__name__))

  def _value_from_xml_string(self, string):
    return float(string)
