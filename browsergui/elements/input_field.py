from . import LeafElement
from ..events import Input

class InputField(LeafElement):
  '''Any form of user value-input element.

  Access/change the value using the ``value`` attribute. Some kinds of input also support
  a ``placeholder`` attribute, displayed to the user when no value is entered.

  :param change_callback: function to be called whenever the input's value changes
  :type change_callback: function of zero arguments
  '''
  def __init__(self, tag_name='input', value=None, placeholder=None, change_callback=None, **kwargs):
    super(InputField, self).__init__(tag_name=tag_name, **kwargs)
    self.change_callback = None
    self._set_value(value)

    self.add_callback(Input, self._handle_input_event)

    self.placeholder = placeholder
    self.change_callback = change_callback

  @property
  def value(self):
    return self.value_from_xml_string(self.tag.getAttribute('value'))
  @value.setter
  def value(self, value):
    self._set_value(value)
    self.mark_dirty()

  @property
  def placeholder(self):
    return self.tag.getAttribute('placeholder')
  @placeholder.setter
  def placeholder(self, placeholder):
    if placeholder is None:
      if 'placeholder' in self.tag.attributes.keys():
        self.tag.removeAttribute('placeholder')
    else:
      self.tag.setAttribute('placeholder', placeholder)
    self.mark_dirty()

  def _set_value(self, value):
    self.ensure_is_valid_value(value)

    if value is None:
      if 'value' in self.tag.attributes.keys():
        self.tag.removeAttribute('value')
    else:
      self.tag.setAttribute('value', self.value_to_xml_string(value))

    if self.change_callback is not None:
      self.change_callback()

  def _handle_input_event(self, event):
    xml_value_string = event.value
    try:
      value = self.value_from_xml_string(xml_value_string)
    except ValueError:
      # We got some garbage value from the browser for some reason. Abort!
      return
    self._set_value(value)

  def value_from_xml_string(self, value):
    return value

  def value_to_xml_string(self, value):
    return str(value)

  def ensure_is_valid_value(self, value):
    pass
