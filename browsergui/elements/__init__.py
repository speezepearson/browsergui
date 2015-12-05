'''Defines many types of GUI elements.

Element Index
=============

Basic
-----

Simple, static, atomic GUI elements.

.. autosummary::

   Text
   Paragraph
   CodeSnippet
   CodeBlock
   EmphasizedText
   Link

   Image

Input
-----

Elements that gather input from the user.

.. autosummary::

   Button
   TextField
   BigTextField
   Dropdown
   NumberField
   ColorField
   DateField
   FloatSlider
   IntegerSlider

Layout
------

Elements that arrange their children in certain ways.

.. autosummary::

   Container
   Viewport
   List
   Grid

Element Class
=============

The most important thing defined here, from which all other things inherit, is :class:`Element`.

.. autoclass:: Element
   :members:
   :inherited-members:


Full Subclass Documentation
===========================


.. autoclass:: Text
   :members:
.. autoclass:: Paragraph
   :members:
.. autoclass:: CodeSnippet
   :members:
.. autoclass:: CodeBlock
   :members:
.. autoclass:: EmphasizedText
   :members:
.. autoclass:: Link
   :members:

.. autoclass:: Image
   :members:


.. autoclass:: ValuedElement
   :members:

.. autoclass:: Button
   :members:
.. autoclass:: TextField
   :members:
.. autoclass:: BigTextField
   :members:
.. autoclass:: Dropdown
   :members:
.. autoclass:: NumberField
   :members:
.. autoclass:: ColorField
   :members:
.. autoclass:: DateField
   :members:
.. autoclass:: Slider
   :members:
.. autoclass:: FloatSlider
   :members:
.. autoclass:: IntegerSlider
   :members:


.. autoclass:: Container
   :members:
.. autoclass:: Viewport
   :members:
.. autoclass:: List
   :members:
.. autoclass:: Grid
   :members:

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
  """A conceptual GUI element, like a button or a table."""

  def __init__(self, css={}, callbacks={}, **kwargs):
    #: a dict-like object mapping :class:`Event` subclasses to functions that should be called when the corresponding event occurs.
    #:
    #:     >>> my_element.callbacks[Click] = (lambda event: print('Click:', event))
    self.callbacks = CallbackSetter(element=self)

    #: a dict-like object mapping strings (CSS properties) to strings (CSS values).
    #:
    #:     >>> my_text.css['color'] = 'red'
    self.css = Styler(element=self)

    super(Element, self).__init__(**kwargs)

    for key, value in css.items():
      self.css[key] = value
    for key, value in callbacks.items():
      self.callbacks[key] = value

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
      self.gui._change_tracker.mark_dirty(self.tag)

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

from ._basic import *
from ._input import *
from ._layout import *
