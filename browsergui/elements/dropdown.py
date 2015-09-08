from .input_field import InputField
from ..events import Input
from ..pythoncompatibility import collections_abc, STRING_TYPES

class Dropdown(InputField, collections_abc.MutableSequence):
  def __init__(self, options=(), **kwargs):
    super(Dropdown, self).__init__(tag_name='select', **kwargs)

    for option in options:
      self.append(option)

    if options:
      self.set_cached_value(options[0])

  def __getitem__(self, index):
    if isinstance(index, slice):
      return [tag.childNodes[0].data for tag in self.tag.childNodes[index]]
    else:
      return self.tag.childNodes[index].childNodes[0].data

  def __setitem__(self, index, value):
    if isinstance(index, slice):
      raise NotImplementedError("slice assignment to Dropdowns not yet supported")

    del self[index]
    self.insert(index, value)

  def __delitem__(self, index):
    if isinstance(index, slice):
      raise NotImplementedError("slice deletion from Dropdowns not yet supported")

    self.tag.removeChild(self.tag.childNodes[index])
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

  def update_tag_with_cached_value(self):
    for child in self.tag.childNodes:
      if 'selected' in child.attributes.keys():
        child.removeAttribute('selected')
      if self.cached_value == child.childNodes[0].data:
        child.setAttribute('selected', 'true')

  def ensure_is_valid_value(self, value):
    if not (value is None or isinstance(value, STRING_TYPES)):
      raise TypeError('expected value of type str (or None), got {}'.format(type(value).__name__))
    if hasattr(self, 'tag') and value not in self:
      # the `hasattr` check is a kludge because the value might get set during __init__,
      # before the tag is initialized. Really gotta disentangle this all at some point.
      raise ValueError('value not in options: {!r}'.format(value))
