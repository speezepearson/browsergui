'''Defines many types of GUI elements:

.. autosummary::

   basic
   input
   layout

'''

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

  Useful attributes/methods:

  - ``element.styles`` is a dict-like object mapping strings (CSS properties) to strings (CSS values). e.g. ``my_text.styles['color'] = 'red'``
  - ``element.callbacks`` is a dict-like object mapping :class:`.Event` subclasses to functions that should be called when the corresponding event occurs. e.g. ``my_element.callbacks[Click] = (lambda event: print('Click:', event))``
  - ``element.parent`` is the element which contains ``element`` (if any; else None). Elements are (like HTML tags) arranged in trees: an Element may have children (other Elements) or not, and it may have a parent or not.
  - ``element.children`` is a list of all elements which have ``element`` as their parent.
  - ``element.gui`` is the GUI containing the element (if any; else None).
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

class NotUniversallySupportedElement(Element):
  '''Mixin for elements that aren't supported in all major browsers.

  Prints a warning upon instantiation, i.e. if MyElement subclasses NotUniversallySupportedElement, then ``MyElement()`` will log a warning.

  To avoid the warning, either set ``MyElement.warn_about_potential_browser_incompatibility = False`` or pass the keyword argument ``warn_about_potential_browser_incompatibility=False`` into the constructor. (Yes, it's intentionally verbose. This package is meant to be super-portable and work the same way for everyone.)
  '''
  warn_about_potential_browser_incompatibility = True
  def __init__(self, **kwargs):
    warn = kwargs.pop('warn_about_potential_browser_incompatibility', self.warn_about_potential_browser_incompatibility)
    super(NotUniversallySupportedElement, self).__init__(**kwargs)
    if warn:
      logging.warning('{} not supported in all major browsers'.format(type(self).__name__))

from . import basic, input, layout
from .basic import *
from .input import *
from .layout import *
