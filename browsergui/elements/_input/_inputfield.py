from .. import Element
from ...events import Input

class InputField(Element):
  '''An abstract class for elements that conceptually contain a value (string, number, color...)

  Many kinds of input (e.g. :class:`TextField`, :class:`Slider`, :class:`DateField`) inherit from this, or at least pretend to.

  :param change_callback: function to be called whenever the input's value changes
  :type change_callback: function of zero arguments
  '''
  def __init__(self, tag_name='input', value=None, placeholder=None, change_callback=None, **kwargs):
    super(InputField, self).__init__(tag_name=tag_name, **kwargs)
    self.change_callback = None
    self._set_value(value)

    self.callbacks[Input] = self._handle_input_event

    self.placeholder = placeholder
    self.change_callback = change_callback

  @property
  def value(self):
    '''The value currently entered into the field.

    Setting the value fires the field's ``change_callback``.
    '''
    return self.value_from_xml_string(self.tag.getAttribute('value'))
  @value.setter
  def value(self, value):
    self._set_value(value)
    self.mark_dirty()

  @property
  def placeholder(self):
    '''The placeholder text that should be shown when the field is empty.

    Applicable to many, but not all, kinds of InputField.'''
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

  def def_change_callback(self, f):
    '''Decorator to set the InputField's ``change_callback``.

        >>> text_field = TextField()
        >>> @text_field.def_change_callback
        ... def _():
        ...   print("Current value: " + text_field.value)
    '''
    self.change_callback = f
    return f
