from ._valuedelement import ValuedElement
from ...events import Change
from ..._pythoncompatibility import collections_abc, STRING_TYPES

class Dropdown(ValuedElement, collections_abc.MutableSequence):
  '''A dropdown-selector for a set of options (strings).

  A Dropdown is a :class:`ValuedElement`, meaning it has a ``value``, ``placeholder``, and ``change_callback``. It's also a `mutable sequence`_, meaning most things you can do to lists (append, get/set/delitem), you can do to Dropdowns too.

  .. _mutable sequence: https://docs.python.org/2/library/collections.html#collections-abstract-base-classes
  '''

  def __init__(self, options, **kwargs):
    super(Dropdown, self).__init__(tag_name='select', input_event_type=Change, **kwargs)

    options = list(options)
    if not options:
      raise ValueError('Dropdown must not be empty')

    for option in options:
      self.append(option)

    self._set_value_in_tag(options[0])

  def _get_value_from_tag(self):
    for option_tag in self.tag.childNodes:
      if option_tag.getAttribute('selected') == 'true':
        return option_tag.childNodes[0].data
    assert False, 'No option in the dropdown seems to be selected. How did this happen?'

  def _set_value_in_tag(self, value):
    if not self.tag.childNodes:
      # Kludge here. The value gets set during super().__init__(), but at that point
      # we haven't initialized the tag's children yet. Just accept it, because we're
      # going to set the value later in the initializer anyway.
      return

    if not isinstance(value, STRING_TYPES):
      raise TypeError('expected str, got {}'.format(type(value).__name__))

    if value not in self:
      raise ValueError('value not in options: {!r}'.format(value))

    for child in self.tag.childNodes:
      if 'selected' in child.attributes.keys():
        child.removeAttribute('selected')
      if child.childNodes[0].data == value:
        child.setAttribute('selected', 'true')

  def _get_value_from_event(self, event):
    return event.value

  # MutableSequence implementation

  def __getitem__(self, index):
    if isinstance(index, slice):
      return [tag.childNodes[0].data for tag in self.tag.childNodes[index]]
    else:
      return self.tag.childNodes[index].childNodes[0].data

  def __setitem__(self, index, value):
    if not isinstance(value, str):
      raise TypeError("Dropdown options must be strings")
    if isinstance(index, slice):
      raise NotImplementedError("slice assignment to Dropdowns not yet supported")

    option_tag = self.tag.childNodes[index]
    option_tag.setAttribute('value', value)
    option_tag.childNodes[0].data = value
    self.mark_dirty()

  def __delitem__(self, index):
    if isinstance(index, slice):
      raise NotImplementedError("slice deletion from Dropdowns not yet supported")
    if len(self) == 1 and int(index) in (0, -1):
      raise ValueError('Dropdown must not be made empty')

    option_tag = self.tag.childNodes[index]
    self.tag.removeChild(option_tag)
    if option_tag.getAttribute('selected') == 'true':
      self.value = self[0]
    self.mark_dirty()

  def __len__(self):
    return len(self.tag.childNodes)

  def insert(self, index, option):
    if not isinstance(option, str):
      raise TypeError("Dropdown options must be strings")

    option_tag = self.tag.ownerDocument.createElement('option')
    option_tag.setAttribute('value', option)
    option_tag.appendChild(self.tag.ownerDocument.createTextNode(option))
    next_option_tag = self.tag.childNodes[index] if index < len(self.tag.childNodes) else None
    self.tag.insertBefore(option_tag, next_option_tag)
    self.mark_dirty()

  def def_change_callback(self, f):
    '''Decorator to set the Dropdown's ``change_callback``'''
    self.change_callback = f
    return f
