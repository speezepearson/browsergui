from . import j, compound, jquery_method_call

def _listening_function_name(element, event_type):
  return "{}_{}".format(element.id, event_type)

def start_listening(element, event_type=None, recursive=False):
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
  attach = jquery_method_call(element, "on", j(event_type), fname)
  return compound((definition, attach))

def stop_listening(element, event_type):
  fname = _listening_function_name(element, event_type)
  return jquery_method_call(element, "off", j(event_type), fname)

def element_set_callbacks_command(element, recursive=True):
  if recursive:
    return compound(element_set_callbacks_command(descendant, recursive=False) for descendant in element.walk())
  else:
    return compound(
      event_start_listening_command(element, event_type)
      for event_type, callbacks in element.callbacks.items()
      if callbacks)