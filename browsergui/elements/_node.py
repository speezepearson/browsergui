import weakref

class OrphanedError(Exception):
  """Raised when trying to do something nonsensical to an Element with no parent."""
  pass
class NotOrphanedError(Exception):
  """Raised when trying to give an Element a new parent without removing the old one."""
  pass

class Node(object):
  def __init__(self, **kwargs):
    super(Node, self).__init__(**kwargs)
    self.parent_weakref = None

  @property
  def children(self):
    raise NotImplementedError('"children" not implemented for {}'.format(type(self).__name__))

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


class LeafNode(Node):
  @property
  def children(self):
    return ()

class SequenceNode(Node):
  def __init__(self, children=(), **kwargs):
    super(SequenceNode, self).__init__(**kwargs)
    self._children = []

    for child in children:
      self.append(child)

  @property
  def children(self):
    return tuple(self._children)

  def append(self, child):
    """Add a new child after all existing children.

    :raises TypeError: if ``child`` isn't a Node
    :raises NotOrphanedError: if ``child`` already has a parent Node
    """
    if not isinstance(child, Node):
      raise TypeError('can only append Nodes, not {}'.format(type(child).__name__))
    child.parent = self
    self._children.append(child)

  def insert_before(self, new_child, reference_child):
    """Add a new child before a given child.

    :raises NotOrphanedError: if ``new_child`` already has a parent Node
    :raises IndexError: if ``reference_child`` is not a child of this node
    """
    self.insert(self.children.index(reference_child), new_child)

  def insert_after(self, new_child, reference_child):
    """Add a new child after a given child.

    :raises NotOrphanedError: if ``new_child`` already has a parent Node
    :raises IndexError: if ``reference_child`` is not a child of this node
    """
    self.insert(self.children.index(reference_child) + 1, new_child)

  def insert(self, index, child):
    """Add a new child at a specified position.

    :raises NotOrphanedError: if ``child`` already has a parent Node
    """
    child.parent = self
    self._children.insert(index, child)

  def disown(self, child):
    """Remove a child from this node.

    :raises ValueError: if ``child`` is not a child of this node
    """
    self._children.remove(child)
    child.parent = None
