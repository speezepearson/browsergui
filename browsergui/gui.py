import json
from .elements import Element, new_tag
from . import commands

class GUI(object):
  """Manages high-level features of the UI and coordinates between elements.

  :param Element elements: elements to immediately include in the GUI
  """

  def __init__(self, *elements):
    self.tag = new_tag('body')
    self.tag.attributes['id'] = 'body'
    self.children = []
    self.command_streams = set()

    self.elements_by_id = {}

    for element in elements:
      self.append(element)

  def destroy_streams(self, streams=None):
    """Destroys and discards the given command streams.

    :param iterable streams: the streams to destroy (default: all)
    """
    if streams is None:
      streams = self.command_streams
    for stream in streams:
      stream.destroy()
    self.command_streams -= set(streams)

  def send_command(self, command):
    """Sends a snippet of JavaScript to all the GUI's command streams.

    :param str command: the JavaScript snippet
    """
    for stream in self.command_streams:
      stream.put(command)

  def dispatch_event(self, event):
    """Dispatch the event to whatever element is responsible for handling it.

    :param dict event:
    """
    element = self.elements_by_id[event['id']]
    element.handle_event(event)

  @property
  def id(self):
    """To be cleaned up, per issue #23."""
    return self.tag.attributes['id'].value

  @property
  def gui(self):
    """To be cleaned up, per issue #23."""
    return self

  def walk_elements(self):
    """To be cleaned up, per issue #23."""
    for element in self.children:
      for descendant in element.walk():
        yield descendant

  def append(self, child):
    """To be cleaned up, per issue #23."""
    if not isinstance(child, Element):
      raise TypeError(child)
    self.tag.appendChild(child.tag)
    self.children.append(child)
    self.register_child(child)

  def disown(self, child):
    """To be cleaned up, per issue #23."""
    self.children.remove(child)
    self.unregister_element(child)
    child.parent = None

  def register_child(self, child):
    """To be cleaned up, per issue #23."""
    child.parent = self
    self.register_element(child)

  def register_element(self, element):
    """docstring"""
    for subelement in element.walk():
      self.elements_by_id[subelement.id] = subelement
    self.send_command(commands.insert_element(element, add_callbacks=True))

  def unregister_element(self, element):
    """docstring"""
    for subelement in element.walk():
      del self.elements_by_id[subelement.id]

  def command_stream(self):
    """Builds a :class:`CommandStream` that will be kept up to date as the GUI changes."""
    result = commands.CommandStream()
    result.put(self._quickstart_command())
    self.command_streams.add(result)
    return result

  def _quickstart_command(self):
    """JavaScript to add all necessary interactivity to the GUI's plain HTML.

    :rtype: str
    """
    return commands.compound(commands.insert_element(e) for e in self.children)

  def note_callback_added(self, element, event_type, callback):
    """docstring"""
    if len(element.callbacks[event_type]) == 1:
      self.send_command(commands.callbacks.start_listening(element, event_type))

  def note_callback_removed(self, element, event_type, callback):
    """docstring"""
    if len(element.callbacks[event_type]) == 0:
      self.send_command(commands.callbacks.stop_listening(element, event_type))
