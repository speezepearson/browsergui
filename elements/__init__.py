import collections
import json
import weakref
import xml.etree.ElementTree

import bs4

CLICK = "click"
KEYDOWN = "keydown"
KEYUP = "keyup"

_unique_id_counter = 0
def unique_id():
  global _unique_id_counter
  _unique_id_counter += 1
  return "_element_{}".format(_unique_id_counter)

class ParseError(Exception):
  pass
class NotOrphanedError(Exception):
  pass
class NoSuchCallbackError(Exception):
  pass

def validate_tag(html):
  try:
    xml.etree.ElementTree.fromstring(html)
  except xml.etree.ElementTree.ParseError as e:
    raise ParseError(*e.args)


class Element:
  def __init__(self, html=None, tag_name=None, children=()):
    if not ((html is None) ^ (tag_name is None)):
      raise TypeError("Element.__init__ must be given html or tag_name (but not both)")

    if html is None:
      html = "<{t}></{t}>".format(t=tag_name)

    validate_tag(html)
    (self.tag,) = bs4.BeautifulSoup(html).children

    self.parent_weakref = None
    self.children = list(children)
    self.callbacks = collections.defaultdict(list)

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "Element({!r}, {!r})".format(self.parent, self.id)

  def __hash__(self):
    return hash(self.tag)

  def __eq__(self, other):
    if isinstance(other, Element):
      return self.tag == other.tag and self.callbacks == other.callbacks

  @property
  def id(self):
    if 'id' not in self.tag.attrs:
      self.tag.attrs['id'] = unique_id()
    return self.tag['id']

  def append(self, child):
    if not child.orphaned:
      raise NotOrphanedError('only orphaned elements can be inserted')
    self.tag.append(child.tag)
    self.children.append(child)
    child.parent = self

  def insert_before(self, sibling):
    if not sibling.orphaned:
      raise NotOrphanedError('only orphaned elements can be inserted')
    self.tag.insert_before(sibling.tag)
    self.parent.children.insert(self.parent.children.index(self), sibling)
    sibling.parent = self.parent

  def insert_after(self, sibling):
    if not sibling.orphaned:
      raise NotOrphanedError('only orphaned elements can be inserted')
    self.tag.insert_after(sibling.tag)
    self.parent.children.insert(self.parent.children.index(self)+1, sibling)
    sibling.parent = self.parent

  @property
  def parent(self):
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
  def html(self):
    raise NotImplementedError()

  @property
  def orphaned(self):
    return (self.parent is None)

  @property
  def gui(self):
    raise NotImplementedError()

  def extract(self):
    self.parent.disown(self)

  def disown(self, child):
    self.children.remove(child)
    child.parent = None

  def add_callback(self, event_type, callback):
    self.callbacks[event_type].append(callback)

  def remove_callback(self, event_type, callback):
    if callback not in self.callbacks[event_type]:
      raise NoSuchCallbackError(event_type, callback)
    self.callbacks[event_type].remove(callback)

  def handle_event(self, event):
    for callback in self.callbacks[event['type']]:
      callback(event)


class Text(Element):
  def __init__(self, string):
    super().__init__(tag_name="span")
    raise NotImplementedError()
    self.string = string

class Button(Element):
  def __init__(self, text, callback=None):
    super().__init__(tag_name="button")
    raise NotImplementedError()
    self.text = text
    if callback is not None:
      self.add_callback(CLICK, callback)

  def set_callback(self, callback):
    self.callbacks[CLICK] = [callback]

class Container(Element):
  def __init__(self, *children, inline=False):
    super().__init__(tag_name=("span" if inline else "div"), children=children)
    raise NotImplementedError()
    self._inline = inline

class Image(Element):
  def __init__(self, location):
    super().__init__(tag_name="img")
    raise NotImplementedError()
    self._location = _location
    if callback is not None:
      self.add_callback(CLICK, callback)
