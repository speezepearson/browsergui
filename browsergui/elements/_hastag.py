import xml.dom.minidom

_unique_id_counter = 0
def unique_id():
  """Returns a new string suitable for a tag id every time it's called."""
  global _unique_id_counter
  _unique_id_counter += 1
  return "_element_{}".format(_unique_id_counter)

class HasTag(object):
  def __init__(self, tag_name, **kwargs):
    super(HasTag, self).__init__(**kwargs)
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
    result = []
    frontier = list(reversed(self.tag.childNodes))
    while frontier:
      frontier, to_expand = frontier[:-1], frontier[-1]
      try:
        result.append(to_expand.__owner)
      except AttributeError:
        frontier += list(reversed(to_expand.childNodes))
    return result

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
