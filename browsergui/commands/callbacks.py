"""Tools to deal with callbacks in the JS world.
"""

from . import j, compound, get

def _listening_function_name(element, event_type):
  """The name for the event-listener JS function for a particular element and event type.

  If a DOM element has a callback associated with it for a certain event type, that callback's name will be given by this function.

  :type element: str
  :type event_type: str
  :rtype: str
  """
  return "{}_{}_listener".format(element.id, event_type)

def start_listening(element, event_type=None, recursive=False):
  """Command to set listeners for the given event type on a given element.

  :type element: Element
  :type event_type: Element or None
  :param bool recursive: if true, listeners will be set for all the element's descendants too
  :rtype: str
  """
  if recursive:
    return compound(start_listening(descendant, event_type=event_type) for descendant in element.walk())

  if event_type is None:
    return compound(start_listening(element, event_type=t) for t in element.callbacks.keys())

  fname = _listening_function_name(element, event_type)
  definition = """
    function {fname}() {{
      notify_server({{
        type: {type},
        id: {id}
      }})
    }}""".format(
      fname=fname,
      type=j(event_type),
      id=j(element.id))
  attach = "{e}.addEventListener({type}, {fname})".format(e=get(element), type=j(event_type), fname=fname)
  return compound((definition, attach))

def stop_listening(element, event_type):
  """Command to remove an event-listener function from an element.

  :type element: Element
  :type event_type: str
  :rtype: str
  """
  fname = _listening_function_name(element, event_type)
  return "{e}.removeEventListener({type}, {fname})".format(e=get(element), type=j(event_type), fname=fname)
