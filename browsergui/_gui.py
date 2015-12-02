import xml.dom.minidom
from .elements import Element, Text, Container
from ._documentchangetracker import DocumentChangeTracker
from . import _server as server

class _Page(Element):
  '''Root Element, corresponding to the <html> tag.

  Since an HTML document always has a <head> and a <body>, a _Page always has a :class:`_Head` and a :class:`_Body`.
  '''
  def __init__(self, gui, **kwargs):
    self._gui = gui
    super(_Page, self).__init__(tag_name='html', **kwargs)
    self.tag.setAttribute('id', '__html__')

    self.head = _Head()
    self.tag.appendChild(self.head.tag)

    self.body = _Body()
    self.tag.appendChild(self.body.tag)

  @property
  def gui(self):
    return self._gui
  @gui.setter
  def gui(self, new_gui):
    self._gui = new_gui

class _Head(Container):
  '''Element corresponding to the HTML <head> tag. Always has a title.'''
  def __init__(self, **kwargs):
    super(_Head, self).__init__(tag_name='head', **kwargs)
    self.title = Text(tag_name='title', text='')
    self.append(self.title)

class _Body(Container):
  '''Element corresponding to the HTML <body> tag.'''
  def __init__(self, **kwargs):
    super(_Body, self).__init__(tag_name='body', **kwargs)


class GUI(object):
  """Manages high-level features of the UI and coordinates between elements.

  Useful attributes/methods:

  See `this wiki page`_ for a guide to the basics.

  .. _this wiki page: https://github.com/speezepearson/browsergui/wiki/How-Do-I...

  :param Element elements: elements to immediately include in the GUI
  :param str title: title of the GUI (i.e. title of browser tab)
  """

  def __init__(self, *elements, **kwargs):
    # Create the page initially with no GUI, because once it has a GUI,
    # modifying it will try to mark it as dirty; but we haven't set up
    # the change tracker yet, so it'll reach for a tracker that isn't there.
    self.page = _Page(gui=None)
    self.title = kwargs.pop('title', 'browsergui')

    self._create_change_tracker()
    self.server = None

    # NOW that we're all initialized, we can connect the page to the GUI.
    self.page.gui = self

    super(GUI, self).__init__(**kwargs)

    self.body.extend(elements)

  @property
  def body(self):
    '''A :class:`Container` that contains all the Elements you put into the GUI.

    Since Containers are mutable sequences, the following all do what you'd expect:

        >>> gui.body.append(e)
        >>> gui.body.extend([e1, e2, e3, e4])
        >>> gui.body[3] = e5
        >>> del gui.body[0]
    '''
    return self.page.body

  @property
  def title(self):
    '''The title for the browser page.'''
    return self.page.head.title.text
  @title.setter
  def title(self, new_title):
    self.page.head.title.text = new_title

  def dispatch_event(self, event):
    """Dispatch an event to whatever element is responsible for handling it."""
    for element in self.body.walk():
      if element.id == event.target_id:
        element.handle_event(event)
        break
    else:
      raise KeyError('no element with id {!r}'.format(event.target_id))

  def _create_change_tracker(self):
    self._change_tracker = DocumentChangeTracker()
    self._change_tracker.mark_dirty(self.page.tag)

  @property
  def running(self):
    return (self.server is not None)

  def run(self, open_browser=True, port=None, quiet=False):
    '''Displays the GUI, and blocks until Ctrl-C is hit or :func:`stop_running()` is called.

    Raises a :class:`RuntimeError` if the GUI is already running.

    :param bool open_browser: whether to open a browser tab for the GUI
    :param int port: which port to start the HTTP server on (``None`` for "don't care")
    :param bool quiet: whether to silence normal the server's normal logging to stderr.
    '''
    if self.running:
      raise RuntimeError('{} is already running'.format(self))

    self.server = server.make_server_for_gui(self, port=port, quiet=quiet)

    if open_browser:
      server.point_browser_to_server(self.server, quiet=quiet)

    try:
      self.server.serve_forever()
    except KeyboardInterrupt:
      self.stop_running()

  def stop_running(self):
    '''Stops displaying the GUI.

    Raises a :class:`RuntimeError` if the GUI is not running.
    '''
    if not self.running:
      raise RuntimeError('{} is not running'.format(self))
    self.server.shutdown()
    self.server.socket.close()
    self._change_tracker.destroy()
    self._create_change_tracker()
    self.server = None
