import xml.dom.minidom
from .elements import Text, Container
from .documentchangetracker import DocumentChangeTracker

class _Body(Container):
  def __init__(self, gui, **kwargs):
    super(_Body, self).__init__(tag_name='body', **kwargs)
    self.tag.setAttribute('id', '__body__')
    self._gui = gui

  @property
  def gui(self):
    return self._gui


def _create_gui_xml_document(title_tag, body_tag):
  document = xml.dom.minidom.Document()
  html_tag = document.createElement('html')
  head_tag = document.createElement('head')

  document.appendChild(html_tag)
  html_tag.appendChild(head_tag)
  head_tag.appendChild(title_tag)
  html_tag.appendChild(body_tag)

  return document


class GUI(object):
  """Manages high-level features of the UI and coordinates between elements.

  :param Element elements: elements to immediately include in the GUI
  """

  def __init__(self, *elements, **kwargs):
    self.title = Text(tag_name='title', text=kwargs.pop('title', 'browsergui'))
    self.body = _Body(gui=self)
    self.make_new_document(destroy=False)
    super(GUI, self).__init__(**kwargs)

    for element in elements:
      self.append(element)

  def dispatch_event(self, event):
    """Dispatch the event to whatever element is responsible for handling it.

    :param dict event:
    """
    for element in self.body.walk():
      if element.id == event['id']:
        element.handle_event(event)
        break
    else:
      raise KeyError('no element with id {!r}'.format(event['id']))

  def append(self, child):
    """To be cleaned up, per issue #23."""
    self.body.append(child)

  def disown(self, child):
    """To be cleaned up, per issue #23."""
    self.body.disown(child)

  def make_new_document(self, destroy=True):
    if destroy:
      self.change_tracker.destroy()
    self.document = _create_gui_xml_document(title_tag=self.title.tag, body_tag=self.body.tag)
    self.change_tracker = DocumentChangeTracker(self.document)

  def destroy(self):
    self.change_tracker.destroy()
