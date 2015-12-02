from .. import Element
from ..._pythoncompatibility import collections_abc

class Container(Element, collections_abc.MutableSequence):
  """Contains other elements without any fancy layout stuff.

  Useful when you want to put several elements in a place that can only hold one element (e.g. if you want a :class:`List` item consisting of multiple elements, or if you want to put multiple elements in a :class:`Grid` cell).

  Subclasses `MutableSequence`_, which means that most operations you'd do to a `list` (e.g. insert, remove, get/set/delitem), you can do to a Container as well.

  .. _MutableSequence: https://docs.python.org/2/library/collections.html#collections-abstract-base-classes

  :param children: Elements the Container should contain
  """
  def __init__(self, *children, **kwargs):
    kwargs.setdefault('tag_name', 'div')
    super(Container, self).__init__(**kwargs)
    for child in children:
      self.append(child)

  def __getitem__(self, index):
    return self.children[index]

  def __setitem__(self, index, child):
    if not isinstance(child, Element):
      raise TypeError('expected Element, got {}'.format(type(child).__name__))
    del self[index]
    self.insert(index, child)

  def __delitem__(self, index):
    self.tag.removeChild(self.tag.childNodes[index])
    self.mark_dirty()

  def __len__(self):
    return len(self.children)

  def insert(self, index, child):
    if not isinstance(child, Element):
      raise TypeError('expected Element, got {}'.format(type(child).__name__))
    try:
      next_child = self.tag.childNodes[index]
    except IndexError:
      next_child = None
    self.tag.insertBefore(child.tag, next_child)
    self.mark_dirty()
