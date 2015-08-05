"""Tools to modify the structure of the DOM.
"""

from . import j, compound, get
from ..elements import Text

def _next_sibling(element):
  siblings = element.parent.children
  i = siblings.index(element)
  return 'null' if i+1 >= len(siblings) else get(siblings[i+1])

def insert_element(element):
  """Command to add a new element to the DOM.

  :param Element element: the :class:`Element`, already in the :class:`GUI`'s element tree, for which an HTML element should be created
  :rtype: str
  """
  lines = []
  for descendant in element.walk():
    name = descendant.id
    lines.append('{name} = document.createElement({tag_name})'.format(name=name, tag_name=j(descendant.tag.tagName)))
    for attribute in descendant.tag.attributes.keys():
      lines.append('{name}.setAttribute({k}, {v})'.format(
        name=name,
        k=j(attribute),
        v=j(descendant.tag.getAttribute(attribute))))

    if descendant is element:
      lines.append('{parent}.insertBefore({name}, {next})'.format(
        parent=get(element.parent),
        name=name, next=_next_sibling(element)))
    else:
      lines.append('{parent}.appendChild({name})'.format(parent=get(descendant.parent), name=name))

    if isinstance(descendant, Text):
      lines.append('{name}.innerText = {text}'.format(name=name, text=j(descendant.text)))

  return compound(lines)

def remove_element(element):
  """Command to delete an element and all its descendants.
  """
  return "{e}.parentNode.removeChild({e})".format(e=get(element))
