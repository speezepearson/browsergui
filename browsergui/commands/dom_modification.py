"""Tools to modify the structure of the DOM.
"""

from . import j, compound, jquery_method_call, callbacks

def insert_element(element, add_callbacks=True):
  """Command to add a new element to the DOM.

  :param Element element: the :class:`Element`, already in the :class:`GUI`'s element tree, for which an HTML element should be created
  :param bool add_callbacks: (default true) whether to include commands to attach callbacks to the created element and all its descendants
  :rtype: str
  """
  html = j(element.html)
  if element.previous_sibling is None:
    result = jquery_method_call(element.parent, "prepend", html)
  else:
    result = jquery_method_call(element.previous_sibling, "after", html)

  if add_callbacks:
    result = compound((result, callbacks.start_listening(element, recursive=True)))

  return result

def remove_element(element):
  """Command to delete an element and all its descendants.
  """
  html = j(element.html)
  if element.previous_sibling is None:
    return jquery_method_call(element.parent, "prepend", html)
  return jquery_method_call(element.previous_sibling, "after", html)
