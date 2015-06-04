import json
from .elements import Element, parse_tag
from . import commands

class GUI(object):
  def __init__(self, *elements):
    self.tag = parse_tag('<body></body>')
    self.tag.attributes['id'] = 'body'
    self.children = []
    self.command_streams = set()

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
    self.send_command(commands.insert_element(element))
    self.send_command(commands.callbacks.start_listening(element, recursive=True))

  def unregister_element(self, element):
    for subelement in element.walk():
      del self.elements_by_id[subelement.id]

  def command_stream(self):
    result = commands.CommandStream()
    result.put(self._quickstart_command())
    self.command_streams.add(result)
    return result

  def html_and_command_stream(self):
    return (self.html, self.command_stream())

  def _quickstart_command(self):
    return commands.compound(commands.callbacks.start_listening(e) for e in self.children)

  def note_callback_added(self, element, event_type, callback):
    if len(element.callbacks[event_type]) == 1:
      self.send_command(commands.callbacks.start_listening(element, event_type))

  def note_callback_removed(self, element, event_type, callback):
    if len(element.callbacks[event_type]) == 0:
      self.send_command(commands.callbacks.stop_listening(element, event_type))
