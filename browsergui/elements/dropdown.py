from . import LeafElement
from ..events import Input
from ..pythoncompatibility import collections_abc, STRING_TYPES

class Dropdown(LeafElement, collections_abc.MutableSequence):
  def __init__(self, options, change_callback=None, **kwargs):
    super(Dropdown, self).__init__(tag_name='select', **kwargs)
    self.change_callback = None

    options = list(options)
    if not options:
      raise ValueError('Dropdown must not be empty')

    for option in options:
      self.append(option)

    self._set_value(options[0])

    self.add_callback(Input, lambda event: self._set_value(event.value))
    self.change_callback = change_callback

  @property
  def value(self):
    for option_tag in self.tag.childNodes:
      if option_tag.getAttribute('selected') == 'true':
        return option_tag.childNodes[0].data
    assert False, 'No option in the dropdown seems to be selected. How did this happen?'
  @value.setter
  def value(self, value):
    self._set_value(value)
    self.mark_dirty()

  def _set_value(self, value):
    self.ensure_is_valid_value(value)
    for child in self.tag.childNodes:
      if 'selected' in child.attributes.keys():
        child.removeAttribute('selected')
      if child.childNodes[0].data == value:
        child.setAttribute('selected', 'true')

    if self.change_callback is not None:
      self.change_callback()

  def ensure_is_valid_value(self, value):
    if not (value is None or isinstance(value, STRING_TYPES)):
      raise TypeError('expected value of type str (or None), got {}'.format(type(value).__name__))
    if hasattr(self, 'tag') and value not in self:
      # the `hasattr` check is a kludge because the value might get set during __init__,
      # before the tag is initialized. Really gotta disentangle this all at some point.
      raise ValueError('value not in options: {!r}'.format(value))

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
