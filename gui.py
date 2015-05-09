import json
import weakref
import bs4
import destructiblequeue
from .elements import Element

def element_creation_command(element):
  return "$({parent_selector}).append({html})".format(
    parent_selector=json.dumps(("#"+element.parent.id if isinstance(element.parent, Element) else 'body')),
    html=json.dumps(element.html))

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

class GUI:
  def __init__(self, *elements):
    self.command_queue = destructiblequeue.DestructibleQueue()
    self.soup = bs4.BeautifulSoup()
    self.children = []
    self.command_streams = weakref.WeakSet()

    self.tags_to_elements = weakref.WeakKeyDictionary()

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
    tag = self.soup.find(id=event['id'])
    element = self.tags_to_elements[tag]
    print("having {} handle event {}".format(element, event))
    element.handle_event(event)

  @property
  def html(self):
    return str(self.soup)

  @property
  def gui(self):
    return self

  def walk_elements(self):
    for element in self.children:
      yield from element.walk()

  def append(self, child):
    if not isinstance(child, Element):
      raise TypeError(child)
    self.soup.append(child.tag)
    self.children.append(child)
    self.register_child(child)

  def disown(self, child):
    self.children.remove(child)
    self.unregister_element(child)
    child.parent = None

  def register_child(self, child):
    self.register_element(child)
    child.parent = self
    self.send_command(element_creation_command(child))

  def register_element(self, element):
    for subelement in element.walk():
      self.tags_to_elements[subelement.tag] = subelement
  def unregister_element(self, element):
    for subelement in element.walk():
      del self.tags_to_elements[subelement.tag]

  def command_stream(self):
    result = destructiblequeue.DestructibleQueue()
    self._send_startup_commands_to_stream(result)
    self.command_streams.add(result)
    return result

  def html_and_command_stream(self):
    return (self.html, self.command_stream())

  def _send_startup_commands_to_stream(self, stream):
    for element in self.walk_elements():
      for event_type, callbacks in element.callbacks.items():
        if not callbacks:
          continue
        self.send_command(event_start_listening_command(element, event_type), stream=stream)

  def note_callback_added(self, element, event_type, callback):
    if len(element.callbacks[event_type]) == 1:
      self.send_command(event_start_listening_command(element, event_type))

  def note_callback_removed(self, element, event_type, callback):
    if len(element.callbacks[event_type]) == 0:
      self.send_command(event_stop_listening_command(element, event_type))