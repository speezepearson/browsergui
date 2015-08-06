"""Tools to modify the structure of the DOM.
"""

import xml.dom.minidom
from . import j, compound, get
from ..elements import Text

def _var(tag):
  '''Returns a good JavaScript variable name unique to a tag.'''
  return tag.getAttribute('id')

def _create_tag(tag):
  '''Command to create a tag, including all its descendants.

  Assigns the resulting DOM element to ``_var(tag)``.
  '''
  var = _var(tag)
  lines = []
  lines.append('{var} = document.createElement({tagName})'.format(var=var, tagName=j(tag.tagName)))
  for attr in tag.attributes.keys():
    lines.append('{var}.setAttribute({attr}, {value})'.format(var=var, attr=j(attr), value=j(tag.getAttribute(attr))))

  for child in tag.childNodes:
    if isinstance(child, xml.dom.minidom.Element):
      lines.append(_create_tag(child))
      lines.append('{var}.appendChild({child})'.format(var=var, child=_var(child)))
    elif isinstance(child, xml.dom.minidom.Text):
      lines.append('{var}.appendChild(document.createTextNode({text}))'.format(var=var, text=j(child.data)))
    else:
      raise TypeError("don't know how to build element of type {}".format(type(child).__name__))

  return compound(lines)

def insert_element(element):
  """Command to add a new element to the DOM.

  :param Element element: the :class:`Element`, already in the :class:`GUI`'s element tree, for which an HTML element should be created
  :rtype: str
  """
  creation_command = _create_tag(element.tag)
  if element.tag.tagName == 'body':
    insertion_command = compound((
      'document.getElementsByTagName("body")[0].remove()',
      'document.documentElement.appendChild({var})'.format(var=_var(element.tag))))
  else:
    insertion_command = '{parent}.insertBefore({var}, {next})'.format(
      parent=_var(element.tag.parentNode),
      var=_var(element.tag),
      next=('null' if element.tag.nextSibling is None else _var(element.tag.nextSibling)))

  return compound((creation_command, insertion_command))

def remove_element(element):
  """Command to delete an element and all its descendants.
  """
  return "{var}.parentNode.removeChild({var})".format(var=_var(element.tag))
