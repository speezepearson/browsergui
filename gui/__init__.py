import closablequeue

class GUI:
  def __init__(self):
    self.command_queue = closablequeue.ClosableQueue()
    self.elements = {}
    self.add_element(Element(self, id="body"))

  @property
  def body(self):
    return self.elements["body"]

  def close(self):
    self.command_queue.close()

  def send_js_command(self, command):
    self.command_queue.put(command)

  def get_js_command(self):
    return self.command_queue.get()

  def add_element(self, element):
    self.elements[element.id] = element

  def handle_event(self, event):
    self.elements[event["id"]].handle_event(event)

from .element import Element