import destructiblequeue
from .elements import Element

class GUI:
  def __init__(self, *elements):
    self.command_queue = destructiblequeue.DestructibleQueue()
    self.soup = None # To do

    self.command_streams = weakref.WeakSet()

  def destroy(self):
    for stream in self.command_streams:
      stream.destroy()

  def send_command(self, command):
    for stream in self.command_streams:
      stream.put(command)

  def handle_event(self, event):
    self.elements[event["id"]].handle_event(event)

  @property
  def html(self):
    raise NotImplementedError()

  def command_stream(self):
    result = destructiblequeue.DestructibleQueue()
    self._send_startup_commands_to_stream(result)
    self.command_streams.add(result)
    return result

  def html_and_command_stream(self):
    return (self.html, self.command_stream())

  def _send_startup_commands_to_stream(self, stream):
    raise NotImplementedError()