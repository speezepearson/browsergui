from ._inputfield import InputField
from ..._pythoncompatibility import STRING_TYPES

class TextField(InputField):
  '''A single-line text input field.

  Inherits from :class:`ValuedElement`, meaning it has a ``value``, ``placeholder``, and ``change_callback``.

  For multi-line text input, see :class:`BigTextField`, which has a very similar interface.
  '''
  def __init__(self, value='', **kwargs):
    super(TextField, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'text')

  def _value_to_xml_string(self, value):
    if isinstance(value, STRING_TYPES):
      return value
    raise TypeError('expected value to be str (or None), got {}'.format(type(value).__name__))

  def _value_from_xml_string(self, string):
    return string
