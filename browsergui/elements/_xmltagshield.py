import xml.dom.minidom

_unique_id_counter = 0
def unique_id():
  """Returns a new string suitable for a tag id every time it's called."""
  global _unique_id_counter
  _unique_id_counter += 1
  return "_element_{}".format(_unique_id_counter)

class TreeTraversalMixin(object):
  '''Provides tree-traversal methods like ``walk``.

  Subclasses must define ``parent`` and ``children``.

  This would be more appropriate as a metaclass, but metaclass syntax is
  incompatible between Python 2 and 3, and this isn't really user-facing,
  so I can afford to be a little lazy.
  '''

  @property
  def orphaned(self):
    """Whether the node has no parent.

    :rtype: bool
    """
    return (self.parent is None)

  @property
  def ancestors(self):
    '''Lists the object's parent, parent's parent, etc.'''
    if self.orphaned:
      return []
    return [self.parent] + self.parent.ancestors

  @property
  def root(self):
    '''The uppermost ancestor of the object (i.e. the one with no parent).'''
    return self if self.parent is None else self.parent.root

  def walk(self):
    """Iterates over the node and all the nodes below it in the tree."""
    yield self
    for child in self.children:
      for descendant in child.walk():
        yield descendant


class XMLTagShield(TreeTraversalMixin):
  def __init__(self, tag_name, **kwargs):
    super(XMLTagShield, self).__init__(**kwargs)
    self.tag = xml.dom.minidom.Document().createElement(tag_name)
    self.tag.setAttribute('id', unique_id())
    self.tag.__owner = self

  @property
  def id(self):
    return self.tag.getAttribute('id')

  @property
  def parent(self):
    tag = self.tag.parentNode
    while tag is not None:
      try:
        return tag.__owner
      except AttributeError:
        tag = tag.parentNode
    return None

  @property
  def children(self):
    '''List the object's immediate children, in depth-first order.'''
    result = []
    frontier = list(reversed(self.tag.childNodes))
    while frontier:
      frontier, to_expand = frontier[:-1], frontier[-1]
      try:
        result.append(to_expand.__owner)
      except AttributeError:
        frontier += list(reversed(to_expand.childNodes))
    return result

