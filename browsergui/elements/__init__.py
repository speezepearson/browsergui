import collections
import json
import weakref
import xml.dom.minidom
import xml.parsers.expat

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

def parse_tag(html):
  try:
    return xml.dom.minidom.parseString(html).documentElement
  except xml.parsers.expat.ExpatError:
    raise ParseError("invalid html", html)

class Element(object):
  def __init__(self, html=None, tag_name=None, children=()):
    if not ((html is None) ^ (tag_name is None)):
      raise TypeError("Element.__init__ must be given html or tag_name (but not both)")

    if html is None:
      html = "<{t}></{t}>".format(t=tag_name)

    self.tag = parse_tag(html)
    self.tag.attributes['id'] = unique_id()

    self.parent_weakref = None
    self.children = []
    self.callbacks = collections.defaultdict(list)

    for child in children:
      self.append(child)

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "Element({!r}, {!r})".format(self.parent, self.id)

  def __hash__(self):
    return id(self)

  def __eq__(self, other):
    if isinstance(other, Element):
      return self.tag.toxml() == other.tag.toxml() and self.callbacks == other.callbacks

  @property
  def id(self):
    return self.tag.attributes['id'].value

  def walk(self):
    yield self
    for child in self.children:
      for descendant in child.walk():
        yield descendant

  def append(self, child):
    if not isinstance(child, Element):
      raise TypeError(child)
    if not child.orphaned:
      raise NotOrphanedError('only orphaned elements can be inserted')
    self.tag.appendChild(child.tag)
    self.children.append(child)
    self.register_child(child)

  def insert_before(self, sibling):
    if not isinstance(sibling, Element):
      raise TypeError(sibling)
    if not sibling.orphaned:
      raise NotOrphanedError('only orphaned elements can be inserted')
    self.parent.tag.insertBefore(sibling.tag, self.tag)
    self.parent.children.insert(self.parent.children.index(self), sibling)
    self.parent.register_child(sibling)

  def insert_after(self, sibling):
    if not isinstance(sibling, Element):
      raise TypeError(sibling)
    if not sibling.orphaned:
      raise NotOrphanedError('only orphaned elements can be inserted')

    self.parent.tag.insertBefore(sibling.tag, None if self.next_sibling is None else self.next_sibling.tag)
    self.parent.children.insert(self.parent.children.index(self)+1, sibling)
    self.parent.register_child(sibling)

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
  def next_sibling(self):
    siblings = self.parent.children
    i = siblings.index(self) + 1
    if i < len(siblings):
      return siblings[i]
    return None

  @property
  def previous_sibling(self):
    siblings = self.parent.children
    i = siblings.index(self) - 1
    if i >= 0:
      return siblings[i]
    return None

  @property
  def html(self):
    return self.tag.toprettyxml()

  @property
  def orphaned(self):
    return (self.parent is None)

  @property
  def gui(self):
    return (None if self.parent is None else self.parent.gui)

  def extract(self):
    self.parent.disown(self)

  def disown(self, child):
    self.children.remove(child)
    if self.gui is not None:
      self.gui.unregister_element(child)
    child.parent = None

  def register_child(self, child):
    if self.gui is not None:
      self.gui.register_element(child)
    child.parent = self

  def add_callback(self, event_type, callback):
    self.callbacks[event_type].append(callback)
    if self.gui is not None:
      self.gui.note_callback_added(self, event_type, callback)

  def remove_callback(self, event_type, callback):
    if callback not in self.callbacks[event_type]:
      raise NoSuchCallbackError(event_type, callback)
    self.callbacks[event_type].remove(callback)
    if self.gui is not None:
      self.gui.note_callback_added(self, event_type, callback)

  def handle_event(self, event):
    for callback in self.callbacks[event['type']]:
      callback(event)

  def toggle_visibility(self):
    self.gui.send_command("$({selector}).toggle()".format(selector=json.dumps("#"+self.id)))


class Text(Element):
  def __init__(self, text, tag_name="span"):
    if not isinstance(text, str):
      raise TypeError(text)
    super(Text, self).__init__(html="<{tag}></{tag}>".format(tag=tag_name))
    self._text = xml.dom.minidom.Text()
    self._text.data = text
    self.tag.appendChild(self._text)

  @property
  def text(self):
    return self._text.data
  @text.setter
  def text(self, value):
    self._text.data = value
    if self.gui is not None:
      self.gui.send_command("$({selector}).text({text})".format(selector=json.dumps("#"+self.id), text=json.dumps(self.text)))

class CodeSnippet(Text):
  def __init__(self, text):
    super(CodeSnippet, self).__init__(text, tag_name="code")
    self.tag.attributes['style'] = 'white-space: pre;'
class Paragraph(Text):
  def __init__(self, text):
    super(Paragraph, self).__init__(text, tag_name="p")
class CodeBlock(Text):
  def __init__(self, text):
    super(CodeBlock, self).__init__(text, tag_name="pre")

class Button(Text):
  def __init__(self, text="Click!", callback=None):
    if not isinstance(text, str):
      raise TypeError(text)
    super(Button, self).__init__(text, tag_name="button")
    if callback is not None:
      self.set_callback(callback)

  def set_callback(self, callback):
    if self.callbacks[CLICK]:
      self.remove_callback(CLICK, self.callbacks[CLICK][0])
    self.add_callback(CLICK, (lambda event: callback()))

class Container(Element):
  def __init__(self, *children, **kwargs):
    self._inline = kwargs.pop("inline", False)
    super(Container, self).__init__(tag_name=("span" if self._inline else "div"), children=children, **kwargs)

class Image(Element):
  def __init__(self, location):
    super(Image, self).__init__(tag_name="img")
    raise NotImplementedError()
    self._location = _location
    if callback is not None:
      self.add_callback(CLICK, callback)
