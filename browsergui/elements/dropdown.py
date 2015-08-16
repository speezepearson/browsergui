import sys
if sys.version_info >= (3, 3):
  import collections.abc as collections_abc
else:
  import collections as collections_abc

from . import LeafElement
from ..events import Input

class Dropdown(LeafElement, collections_abc.MutableSequence):
  def __init__(self, options=(), change_callback=None, **kwargs):
    super(Dropdown, self).__init__(tag_name="select", **kwargs)

    for option in options:
      self.append(option)

    if options:
      self._select(options[0])

    self.add_callback(Input, self._handle_value_change_event)
    if change_callback is not None:
      self.add_callback(Input, (lambda event: change_callback()))

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

  @property
  def value(self):
    for child in self.tag.childNodes:
      if child.getAttribute('selected'):
        return child.childNodes[0].data
    return None
  @value.setter
  def value(self, value):
    if value not in self:
      raise ValueError(value)
    self._select(value)
    self.handle_event(Input(target_id=self.id, value=self.value))
    self.mark_dirty()

  def _select(self, option):
    for child in self.tag.childNodes:
      if 'selected' in child.attributes.keys():
        child.removeAttribute('selected')
      if option == child.childNodes[0].data:
        child.setAttribute('selected', 'true')

  def _handle_value_change_event(self, event):
    self._select(event.value)
