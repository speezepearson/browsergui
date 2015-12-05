from .. import Element
from ._valuedelement import ValuedElement

class InputField(ValuedElement):
  def __init__(self, tag_name='input', **kwargs):
    super(InputField, self).__init__(tag_name=tag_name, **kwargs)

  def _get_value_from_tag(self):
    return self._value_from_xml_string(self.tag.getAttribute('value'))

  def _set_value_in_tag(self, value):
    self.tag.setAttribute('value', self._value_to_xml_string(value))

  def _get_value_from_event(self, event):
    return self._value_from_xml_string(event.value)
