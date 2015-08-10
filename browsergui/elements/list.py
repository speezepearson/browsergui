import sys
if sys.version_info >= (3, 3):
  import collections.abc as collections_abc
else:
  import collections as collections_abc

from . import Element

class List(Element, collections_abc.MutableSequence):
  """A bulleted/numbered list of elements.

  May be indexed into like a normal list. (See :class:`collections.abc.MutableSequence`.)
  """
  def __init__(self, items=(), numbered=False, **kwargs):
    super(List, self).__init__(tag_name='ul', **kwargs)
    self.numbered = numbered
    self._items = []
    for item in items:
      self.append(item)

  @property
  def children(self):
    return tuple(self._items)

  @property
  def numbered(self):
    return self.tag.tagName == 'ol'
  @numbered.setter
  def numbered(self, value):
    self.tag.tagName = ('ol' if value else 'ul')
    self.mark_dirty()

  def __getitem__(self, index):
    return self._items[index]
  def __setitem__(self, index, child):
    if isinstance(index, slice):
      raise NotImplementedError("slice assignment to Lists not yet supported")

    del self[index]
    self.insert(index, child)

  def __delitem__(self, index):
    if isinstance(index, slice):
      raise NotImplementedError("slice deletion from Lists not yet supported")

    old_child = self._items[index]
    del self._items[index]
    old_child.parent = None
    self.tag.removeChild(old_child.tag.parentNode)
    self.mark_dirty()

  def __len__(self):
    return len(self._items)

  def insert(self, index, child):
    if not isinstance(child, Element):
      raise TypeError("List children must be Elements")

    child.parent = self

    li_tag = self.tag.ownerDocument.createElement('li')
    li_tag.appendChild(child.tag)

    self._items.insert(index, child)

    next_li = self.tag.childNodes[index] if index < len(self.tag.childNodes) else None
    self.tag.insertBefore(li_tag, next_li)

    self.mark_dirty()
