import collections
import json
import xml.dom.minidom
import xml.parsers.expat
import logging

from ._node import SequenceNode, LeafNode
from ._hascallbacks import HasCallbacks, NoSuchCallbackError
from ._hasstyling import HasStyling

class Element(HasCallbacks, HasStyling):
  """A conceptual GUI element, like a button or a table.

  Elements are arranged in trees: an Element may have children (other Elements) or not, and it may have a parent or not.
  """

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "{cls}(id={id!r})".format(cls=type(self).__name__, id=self.id)


class Container(Element, SequenceNode):
  """Contains and groups other elements."""
  def __init__(self, *children, **kwargs):
    kwargs.setdefault('tag_name', 'div')
    super(Container, self).__init__(children=children, **kwargs)

  def append(self, child):
    super(Element, self).append(child)
    self.tag.appendChild(child.tag)
    self.mark_dirty()

  def insert_before(self, new_child, reference_child):
    super(Element, self).insert_before(new_child, reference_child)
    self.tag.insertBefore(new_child.tag, reference_child.tag)
    self.mark_dirty()

  def insert_after(self, new_child, reference_child):
    super(Element, self).insert_after(new_child, reference_child)
    self.tag.insertBefore(new_child.tag, reference_child.tag.nextSibling)
    self.mark_dirty()

  def disown(self, child):
    super(Element, self).disown(child)
    self.tag.removeChild(child.tag)
    self.mark_dirty()


class LeafElement(Element, LeafNode):
  pass

class NotUniversallySupportedElement(Element):
  warn_about_potential_browser_incompatibility = True
  def __init__(self, **kwargs):
    super(NotUniversallySupportedElement, self).__init__(**kwargs)
    if self.warn_about_potential_browser_incompatibility:
      logging.warning('{} not supported in all major browsers'.format(type(self).__name__))

from .text import Text, Paragraph, CodeSnippet, CodeBlock, EmphasizedText
from .button import Button
from .link import Link
from .viewport import Viewport
from .image import Image
from .list import List
from .grid import Grid
from .textfield import TextField
from .dropdown import Dropdown
from .number_field import NumberField
from .color_field import ColorField
from .date_field import DateField
