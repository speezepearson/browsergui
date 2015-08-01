import json
from .elements import Element, new_tag
from . import commands

class _Body(Element):
  def __init__(self, gui):
    super(_Body, self).__init__(tag_name='body')
    self.tag.setAttribute('id', '__body__')
    self._gui = gui

  @property
  def gui(self):
    return self._gui



class GUI(object):
  """Manages high-level features of the UI and coordinates between elements.

  :param Element elements: elements to immediately include in the GUI
  """

  def __init__(self, *elements):
    self.body = _Body(gui=self)
    self.command_broadcaster = commands.Broadcaster()

    self.elements_by_id = {}

    for element in elements:
      self.append(element)

  def send_command(self, command):
    """Sends a snippet of JavaScript to all the GUI's command streams.

    :param str command: the JavaScript snippet
    """
    self.command_broadcaster.broadcast(command)

  def dispatch_event(self, event):
    """Dispatch the event to whatever element is responsible for handling it.

    :param dict event:
    """
    element = self.elements_by_id[event['id']]
    element.handle_event(event)

  def append(self, child):
    """To be cleaned up, per issue #23."""
    self.body.append(child)

  def disown(self, child):
    """To be cleaned up, per issue #23."""
    self.body.disown(child)

  def register_element(self, element):
    """docstring"""
    for subelement in element.walk():
      self.elements_by_id[subelement.id] = subelement
    self.send_command(commands.insert_element(element, add_callbacks=True))

  def unregister_element(self, element):
    """docstring"""
    for subelement in element.walk():
      del self.elements_by_id[subelement.id]
    self.send_command(commands.remove_element(element))

  def initialization_command(self):
    """JS command to immediately bring a command stream up to date.

    :rtype: str
    """
    return commands.compound(commands.insert_element(e) for e in self.body.children)

  def note_callback_added(self, element, event_type, callback):
    """docstring"""
    if len(element.callbacks[event_type]) == 1:
      self.send_command(commands.callbacks.start_listening(element, event_type))

  def note_callback_removed(self, element, event_type, callback):
    """docstring"""
    if len(element.callbacks[event_type]) == 0:
      self.send_command(commands.callbacks.stop_listening(element, event_type))

  def destroy(self):
    self.command_broadcaster.destroy()
