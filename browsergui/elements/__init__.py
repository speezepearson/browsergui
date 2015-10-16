import collections
import json
import xml.dom.minidom
import xml.parsers.expat
import logging

from ._xmltagshield import XMLTagShield
from ._callbacksetter import CallbackSetter
from ._styler import Styler


class Element(XMLTagShield):
  """A conceptual GUI element, like a button or a table.

  Elements are arranged in trees: an Element may have children (other Elements) or not, and it may have a parent or not.
  """

  def __init__(self, styling={}, **kwargs):
    self.callbacks = CallbackSetter(element=self)
    self.styles = Styler(element=self)
    super(Element, self).__init__(**kwargs)

    for key, value in styling.items():
      self.styles[key] = value

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "{cls}(id={id!r})".format(cls=type(self).__name__, id=self.id)

  def handle_event(self, event):
    if type(event) in self.callbacks:
      self.callbacks[type(event)](event)

  # Convenience functions accessing the GUI

  @property
  def gui(self):
    """The GUI the element belongs to, or None if there is none."""
    return (None if self.orphaned else self.parent.gui)

  def mark_dirty(self):
    '''Marks the element as needing redrawing.'''
    if self.gui is not None:
      self.gui.change_tracker.mark_dirty(self.tag)

import collections
class Container(Element, collections.MutableSequence):
  """Contains and groups other elements."""
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
