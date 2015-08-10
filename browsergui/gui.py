import json
from .elements import Text, Container
from .document import Document

class _Body(Container):
  def __init__(self, gui, **kwargs):
    super(_Body, self).__init__(tag_name='body', **kwargs)
    self.tag.setAttribute('id', '__body__')
    self._gui = gui

  @property
  def gui(self):
    return self._gui



class GUI(object):
  """Manages high-level features of the UI and coordinates between elements.

  :param Element elements: elements to immediately include in the GUI
  """

  def __init__(self, *elements, **kwargs):
    self.title = Text(tag_name='title', text=kwargs.pop('title', 'browsergui'))
    self.body = _Body(gui=self)
    self.make_new_document(destroy=False)
    super(GUI, self).__init__(**kwargs)

    self.elements_by_id = {}

    for element in elements:
      self.append(element)

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
    self.document.mark_dirty()

  def unregister_element(self, element):
    """docstring"""
    for subelement in element.walk():
      del self.elements_by_id[subelement.id]
    self.document.mark_dirty()

  def make_new_document(self, destroy=True):
    if destroy:
      self.document.destroy()
    self.document = Document(title_tag=self.title.tag, body_tag=self.body.tag)

  def destroy(self):
    self.document.destroy()
