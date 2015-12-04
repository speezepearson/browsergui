from ._valuedelement import ValuedElement
from ..._pythoncompatibility import STRING_TYPES

class BigTextField(ValuedElement):
  '''A multi-line text field.
  '''
  def __init__(self, value='', **kwargs):
    super(BigTextField, self).__init__(tag_name='textarea', value=value, **kwargs)

  def _get_value_from_tag(self):
    return self.tag.childNodes[0].data if self.tag.childNodes else ''

  def _set_value_in_tag(self, value):
    if not isinstance(value, STRING_TYPES):
      raise TypeError('expected str, got {}'.format(type(value).__name__))
    if not self.tag.childNodes:
      self.tag.appendChild(self.tag.ownerDocument.createTextNode(''))
    self.tag.childNodes[0].data = value

  def _get_value_from_event(self, event):
    return event.value
