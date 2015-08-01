import weakref

class Node(object):
  def __init__(self):
    self.parent_weakref = None

  @property
  def parent(self):
    """
    :returns: the element's parent, or None if the Element is orphaned
    """
    return (None if self.parent_weakref is None else self.parent_weakref())
  @parent.setter
  def parent(self, parent):
    if parent is None:
      self.parent_weakref = None
    elif self.orphaned:
      self.parent_weakref = weakref.ref(parent)
    else:
      raise NotOrphanedError('only orphaned elements can be given new parents')

  @property
  def orphaned(self):
    """Whether the Element has no parent.

    :rtype: bool
    """
    return (self.parent is None)

  @property
  def root(self):
    return self if self.parent is None else self.parent.root

  def walk(self):
    """Iterates over the Element and all the Elements below it in the tree."""
    yield self
    for child in self.children:
      for descendant in child.walk():
        yield descendant
