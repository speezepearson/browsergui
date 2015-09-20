from . import Element
from ..pythoncompatibility import collections_abc

class List(Element, collections_abc.MutableSequence):
  """A list of elements.

  May be numbered or bulleted, according to the `numbered` property (a boolean).

  Supports pretty much all the operations that a normal list does, e.g.

      my_list = List(items=[first, second])
      my_list.append(third)
      my_list.insert(0, new_first)
      assert my_list[0] is new_first
      my_list[1] = new_second
      del my_list[2]
  """
  def __init__(self, items=(), numbered=False, **kwargs):
    super(List, self).__init__(tag_name='ol', **kwargs)
    self.numbered = numbered
    self._items = []
    for item in items:
      self.append(item)

  @property
  def children(self):
    return tuple(self._items)

  @property
  def numbered(self):
    return (self.get_style('list-style-type') == 'decimal')
  @numbered.setter
  def numbered(self, value):
    # The "right" way to do this would be to change the tagName between "ol" and "ul",
    # but the DOM API doesn't specify a way to change a tagName. Using CSS seems like
    # a better solution than destroying the tag and creating a new one.
    #
    # According to https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#Browser_compatibility
    # the values "disc" and "decimal" are supported in all major browsers.
    self.set_styles(**{'list-style-type': ('decimal' if value else 'disc')})

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
