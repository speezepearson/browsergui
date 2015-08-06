import collections
import json
import xml.dom.minidom
import xml.parsers.expat

from ._node import Node, SequenceNode, LeafNode
from ._hascallbacks import HasCallbacks, NoSuchCallbackError
from ._hasstyling import HasStyling

_unique_id_counter = 0
def unique_id():
  """Returns a new string suitable for an :class:`Element` id every time it's called."""
  global _unique_id_counter
  _unique_id_counter += 1
  return "_element_{}".format(_unique_id_counter)

def new_tag(tag_name):
  html = '<{t}></{t}>'.format(t=tag_name)
  return xml.dom.minidom.parseString(html).documentElement

class Element(Node, HasCallbacks, HasStyling):
  """A conceptual GUI element, like a button or a table.

  Elements are arranged in trees: an Element may have children (other Elements) or not, and it may have a parent or not.
  Every element has a unique identifier, accessible by the :func:`id` method.
  """
  def __init__(self, tag_name, **kwargs):
    self.tag = new_tag(tag_name)
    self.tag.setAttribute('id', unique_id())

    super(Element, self).__init__(**kwargs)

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "Element(id={!r})".format(self.id)

  def __hash__(self):
    return id(self)

  def __eq__(self, other):
    if isinstance(other, Element):
      return self.tag.toxml() == other.tag.toxml() and self.callbacks == other.callbacks

  @property
  def id(self):
    return self.tag.getAttribute('id')

  @property
  def gui(self):
    """The GUI the element belongs to, or None if there is none."""
    return (None if self.orphaned else self.parent.gui)

  def _call_dom_method(self, name, args):
    getattr(self.tag, name)(*args)
    if self.gui is not None:
      self.gui.send_command("document.getElementById({id}).{name}({args})".format(
        id=json.dumps(self.id),
        name=name,
        args=', '.join(arg_to_js(x) for x in args)))

def arg_to_js(x):
  if isinstance(x, Element):
    return "document.getElementById({})".format(json.dumps(x.id))
  elif isinstance(x, xml.dom.minidom.Element):
    return "document.getElementById({})".format(json.dumps(x.getAttribute('id')))
  else:
    return json.dumps(x)


class Container(Element, SequenceNode):
  """Contains and groups other elements."""
  def __init__(self, *children, **kwargs):
    kwargs.setdefault('tag_name', 'div')
    super(Container, self).__init__(children=children, **kwargs)

  def append(self, child):
    super(Element, self).append(child)
    self.tag.appendChild(child.tag)
    if self.gui is not None:
      self.gui.register_element(child)

  def insert_before(self, new_child, reference_child):
    super(Element, self).insert_before(new_child, reference_child)
    self.tag.insertBefore(new_child.tag, reference_child.tag)
    if self.gui is not None:
      self.gui.register_element(new_child)

  def insert_after(self, new_child, reference_child):
    super(Element, self).insert_after(new_child, reference_child)
    self.tag.insertBefore(new_child.tag, reference_child.tag.nextSibling)
    if self.gui is not None:
      self.gui.register_element(new_child)

  def disown(self, child):
    super(Element, self).disown(child)
    self.tag.removeChild(child.tag)
    if self.gui is not None:
      self.gui.unregister_element(child)


class LeafElement(Element, LeafNode):
  pass

from .text import Text, Paragraph, CodeSnippet, CodeBlock
from .button import Button
from .link import Link
from .viewport import Viewport
from .image import Image
