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

  @property
  def id(self):
    return self.tag.getAttribute('id')
