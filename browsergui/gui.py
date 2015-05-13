import json
import weakref
from .elements import Element, parse_tag
from .command_stream import CommandStream

def element_insertion_command(element):
  if element.next_sibling is not None:
    selector = "#"+element.next_sibling.id
    format = "$({selector}).before({html})"
  elif element.tag.previousSibling is not None:
    selector = "#"+element.previous_sibling.id
    format = "$({selector}).after({html})"
  else:
    selector = "#"+element.parent.id
    format = "$({selector}).append({html})"

  return format.format(selector=json.dumps(selector), html=json.dumps(element.html))

def element_set_callbacks_command(element, walk=True):
  if walk:
    return "; ".join(element_set_callbacks_command(descendant, walk=False) for descendant in element.walk())
  else:
    return "; ".join(
      event_start_listening_command(element, event_type)
      for event_type, callbacks in element.callbacks.items()
      if callbacks)

def event_listening_function_name(element, event_type):
  return "{}_{}".format(element.id, event_type)

def event_start_listening_command(element, event_type):
  return """
    function {fname}() {{
      notify_server({{
        type: {type},
        id: {id}
      }})
    }}
    $({selector}).on({type}, {fname})""".format(
      fname=event_listening_function_name(element, event_type),
      selector=json.dumps("#"+element.id),
      type=json.dumps(event_type),
      id=json.dumps(element.id))

def event_stop_listening_command(element, event_type):
  return """$({selector}).off({type}, {fname}""".format(
      fname="_".join(element.id, event_type),
      selector=json.dumps("#"+element.id),
      type=json.dumps(event_type),
      id=json.dumps(element.id))

class GUI(object):
  def __init__(self, *elements):
    self.tag = parse_tag('<body></body>')
    self.tag.attributes['id'] = 'body'
    self.children = []
    self.command_streams = weakref.WeakSet()

    self.elements_by_id = {}

    for element in elements:
      self.append(element)

  def destroy(self):
    for stream in self.command_streams:
      stream.destroy()

  def send_command(self, command, stream=None):
    if stream is None:
      for stream in self.command_streams:
        self.send_command(command, stream=stream)
    else:
      stream.put(command)

  def handle_event(self, event):
    element = self.elements_by_id[event['id']]
    element.handle_event(event)

  @property
  def id(self):
    return self.tag.attributes['id'].value

  @property
  def html(self):
    return self.tag.toprettyxml()

  @property
  def gui(self):
    return self

  def walk_elements(self):
    for element in self.children:
      for descendant in element.walk():
        yield descendant

  def append(self, child):
    if not isinstance(child, Element):
      raise TypeError(child)
    self.tag.appendChild(child.tag)
    self.children.append(child)
    self.register_child(child)

  def disown(self, child):
    self.children.remove(child)
    self.unregister_element(child)
    child.parent = None

  def register_child(self, child):
    child.parent = self
    self.register_element(child)

  def register_element(self, element):
    for subelement in element.walk():
      self.elements_by_id[subelement.id] = subelement
    self.send_command(element_insertion_command(element))
    self.send_command(element_set_callbacks_command(element))

  def unregister_element(self, element):
    for subelement in element.walk():
      del self.elements_by_id[subelement.id]

  def command_stream(self):
    result = CommandStream()
    result.put(self._quickstart_command())
    self.command_streams.add(result)
    return result

  def html_and_command_stream(self):
    return (self.html, self.command_stream())

  def _quickstart_command(self):
    return "; ".join(element_set_callbacks_command(e) for e in self.children)

  def note_callback_added(self, element, event_type, callback):
    if len(element.callbacks[event_type]) == 1:
      self.send_command(event_start_listening_command(element, event_type))

  def note_callback_removed(self, element, event_type, callback):
    if len(element.callbacks[event_type]) == 0:
      self.send_command(event_stop_listening_command(element, event_type))