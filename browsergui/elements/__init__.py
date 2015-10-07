import collections
import json
import xml.dom.minidom
import xml.parsers.expat
import logging

from ._node import Node, SequenceNode, LeafNode
from ._hastag import HasTag

class HasOptionalTag(object):
  def __init__(self, tag=None):
    self._tag = tag
    super(HasOptionalTag, self).__init__()

  @property
  def tag(self):
    return self._tag
  @tag.setter
  def tag(self, value):
    raise AttributeError('setting tag on {} has side effects; use .set_tag(tag)'.format(type(self).__name__))

  def set_tag(self, new_tag):
    if self._tag is not None:
      self.detach_from_tag()
    self._tag = new_tag
    if new_tag is not None:
      self.attach_to_tag()

  def detach_from_tag(self):
    pass
  def attach_to_tag(self):
    pass

class Styler(HasOptionalTag, collections.MutableMapping):
  def __init__(self, **rules):
    self.rules = rules
    super(Styler, self).__init__()

  def detach_from_tag(self):
    if 'style' in self.tag.attributes.keys():
      self.tag.removeAttribute('style')
  def attach_to_tag(self):
    self._update_tag_style_attribute()

  def _update_tag_style_attribute(self):
    if self:
      self.tag.setAttribute('style', self._css())
    elif 'style' in self.tag.attributes.keys():
      self.tag.removeAttribute('style')

  def _css(self):
    return '; '.join('{}: {}'.format(k, v) for k, v in sorted(self.items()))

  def __getitem__(self, key):
    return self.rules[key]

  def __setitem__(self, key, value):
    self.rules[key] = value
    self._update_tag_style_attribute()

  def __delitem__(self, key):
    del self.rules[key]
    self._update_tag_style_attribute()

  def __iter__(self):
    return iter(self.rules)

  def __len__(self):
    return len(self.rules)

class CallbackSetter(HasOptionalTag, collections.MutableMapping):
  def __init__(self):
    self.callbacks = {}
    super(CallbackSetter, self).__init__()

  def detach_from_tag(self):
    for event_type in self:
      event_type.disable_server_notification(self.tag)
  def attach_to_tag(self):
    for event_type in self:
      event_type.enable_server_notification(self.tag)

  def __getitem__(self, key):
    return self.callbacks[key]

  def __setitem__(self, key, value):
    self.callbacks[key] = value
    if self.tag is not None:
      key.enable_server_notification(self.tag)

  def __delitem__(self, key):
    del self.callbacks[key]
    if self.tag is not None:
      key.disable_server_notification(self.tag)

  def __iter__(self):
    return iter(self.callbacks)

  def __len__(self):
    return len(self.callbacks)


class Element(Node, HasTag):
  """A conceptual GUI element, like a button or a table.

  Elements are arranged in trees: an Element may have children (other Elements) or not, and it may have a parent or not.
  """

  def __init__(self, styling={}, **kwargs):
    self.callback_setter = CallbackSetter()
    self.styler = Styler(**styling)
    super(Element, self).__init__(**kwargs)
    self.callback_setter.set_tag(self.tag)
    self.styler.set_tag(self.tag)

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "{cls}(id={id!r})".format(cls=type(self).__name__, id=self.id)

  # WRAP STYLER FUNCTIONALITY TO ENSURE mark_dirty() GETS CALLED

  def get_style(self, key):
    return self.styler.get(key)

  def set_styles(self, **kwargs):
    for key, value in kwargs.items():
      self.styler[key] = value
    self.mark_dirty()

  def delete_style(self, key):
    del self.styler[key]
    self.mark_dirty()

  # WRAP CALLBACK FUNCTIONALITY TO ENSURE mark_dirty() GETS CALLED

  def get_callback(self, key):
    return self.callback_setter.get(key)

  def set_callback(self, key, value):
    self.callback_setter[key] = value
    self.mark_dirty()

  def delete_callback(self, key):
    del self.callback_setter[key]
    self.mark_dirty()

  def handle_event(self, event):
    if type(event) in self.callback_setter:
      self.callback_setter[type(event)](event)

  # Convenience functions accessing the GUI

  @property
  def gui(self):
    """The GUI the element belongs to, or None if there is none."""
    return (None if self.orphaned else self.parent.gui)

  def mark_dirty(self):
    '''Marks the element as needing redrawing.'''
    if self.gui is not None:
      self.gui.change_tracker.mark_dirty(self.tag)


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
