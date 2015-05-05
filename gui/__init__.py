import destructiblequeue

class GUI:
  def __init__(self):
    self.command_queue = destructiblequeue.DestructibleQueue()
    self.elements = {}
    self.add_element(Element(self, id="body"))

  @property
  def body(self):
    return self.elements["body"]

  def destroy(self):
    self.command_queue.destroy()

  def send_js_command(self, command):
    self.command_queue.put(command)

  def get_js_command(self, **kwargs):
    return self.command_queue.get(**kwargs)

  def add_element(self, element):
    self.elements[element.id] = element

  def handle_event(self, event):
    self.elements[event["id"]].handle_event(event)

from .element import Element