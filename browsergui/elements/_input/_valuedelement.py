from .. import Element
from ...events import Input

class ValuedElement(Element):
  '''An abstract class for elements that conceptually contain a value (string, number, color...)

  Many kinds of input (e.g. :class:`TextField`, :class:`Slider`, :class:`DateField`) inherit from this.

  :param change_callback: function to be called whenever the input's value changes
  :type change_callback: function of zero arguments
  '''
  def __init__(self, value=None, placeholder=None, change_callback=None, input_event_type=Input, **kwargs):
    super(ValuedElement, self).__init__(**kwargs)
    self.placeholder = placeholder

    # "self.value = ..." accesses change_callback, but calls it if it's not None.
    # It'd be unintuitive to call the change_callback upon instantiation, but we
    # need the change_callback attribute to avoid an AttributeError; so we set it
    # to None for just a minute.
    self.change_callback = None
    self.value = value
    self.change_callback = change_callback

    self.callbacks[input_event_type] = self._handle_input_event

  @property
  def value(self):
    '''The value contained by the element.'''
    return self._get_value_from_tag()
  @value.setter
  def value(self, value):
    self._set_value_in_tag(value)
    if self.change_callback is not None:
      self.change_callback()
    self.mark_dirty()

  @property
  def placeholder(self):
    '''The placeholder text that should be shown when the value is empty.

    Applicable to many, but not all, kinds of ValuedElement.'''
    return self.tag.getAttribute('placeholder')
  @placeholder.setter
  def placeholder(self, placeholder):
    if placeholder is None:
      if 'placeholder' in self.tag.attributes.keys():
        self.tag.removeAttribute('placeholder')
    else:
      self.tag.setAttribute('placeholder', placeholder)
    self.mark_dirty()

  def _handle_input_event(self, event):
    try:
      value = self._get_value_from_event(event)
    except ValueError:
      # We got some garbage value from the browser for some reason. Abort!
      # (This might happen if, say, the browser doesn't support <input type="color">
      #  and so presents it as a text field where the user can type whatever they want.)
      print("{} was unable to read a valid value from {}".format(self, event))
      return
    self._set_value_in_tag(value)
    if self.change_callback is not None:
      self.change_callback()

  def _get_value_from_tag(self):
    raise NotImplementedError('{} does not define _get_value_from_tag'.format(type(self).__name__))
  def _set_value_in_tag(self, value):
    raise NotImplementedError('{} does not define _set_value_in_tag'.format(type(self).__name__))

  def _get_value_from_event(self, event):
    raise NotImplementedError('{} does not define _get_value_from_event'.format(type(self).__name__))

  def def_change_callback(self, f):
    '''Decorator to set the InputField's ``change_callback``.

        >>> text_field = TextField()
        >>> @text_field.def_change_callback
        ... def _():
        ...   print("Current value: " + text_field.value)
    '''
    self.change_callback = f
    return f
