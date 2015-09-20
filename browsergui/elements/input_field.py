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
    self.set_cached_value(value)
    super(InputField, self).__init__(tag_name=tag_name, **kwargs)
    self.update_tag_with_cached_value()

    self.add_callback(Input, lambda event: self.set_cached_value(self.value_from_xml_string(event.value)))
    if change_callback is not None:
      self.add_callback(Input, (lambda event: change_callback()))

    self.placeholder = placeholder

  @property
  def value(self):
    return self.cached_value
  @value.setter
  def value(self, value):
    self.set_cached_value(value)
    self.handle_event(Input(target_id=self.id, value=self.value_to_xml_string(value)))
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

  def update_tag_with_cached_value(self):
    if self.cached_value is None:
      if 'value' in self.tag.attributes.keys():
        self.tag.removeAttribute('value')
    else:
      self.tag.setAttribute('value', self.value_to_xml_string(self.cached_value))
    self.mark_dirty()

  def set_cached_value(self, value):
    self.ensure_is_valid_value(value)
    self.cached_value = value
    if hasattr(self, 'tag'):
      self.update_tag_with_cached_value()

  def value_from_xml_string(self, value):
    return value

  def value_to_xml_string(self, value):
    return str(value)

  def ensure_is_valid_value(self, value):
    pass
