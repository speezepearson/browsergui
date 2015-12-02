import socket

import os
import cgi
import webbrowser
import json

from .._pythoncompatibility import (
  http_status_codes as status_codes,
  HTTPServer, BaseHTTPRequestHandler,
  HTTPServerThreadingMixin as ThreadingMixIn)

import browsergui

ROOT_PATH = "/"
PUPPET_PATH = "/puppet.js"
COMMAND_PATH = "/command"
EVENT_PATH = "/event"

def read_json(request_headers, request_file):
  n_bytes = int(request_headers['content-length'])
  content_bytes = request_file.read(n_bytes)
  content_string = content_bytes.decode('ascii')
  return json.loads(content_string)

class GUIRequestHandler(BaseHTTPRequestHandler):
  """Handler for GUI-related requests.

  There are four main types of request:

  - client asking for the root page
  - client asking for a static resource required by the root page
  - client asking for a lump of JavaScript to execute
  - client notifying server of some user interaction in the browser
  """

  # There will be different servers for different GUIs.
  # Each server will have its own request handler class.
  # Those classes will override `gui` to know what to
  # serve up.
  gui = None

  def do_GET(self):
    if self.path == ROOT_PATH:
      self.get_root()
    elif self.path == PUPPET_PATH:
      self.get_static_file("puppet.js")
    elif self.path == COMMAND_PATH:
      self.get_command()

  def do_POST(self):
    if self.path == EVENT_PATH:
      self.post_event()

  def get_static_file(self, relpath):
    """Serve a static file to the client.

    :param str relpath: the path of the resource to serve, relative to this file
    """
    path = os.path.join(os.path.dirname(__file__), relpath)
    if os.path.exists(path):
      self.send_response(status_codes.OK)
      self.send_no_cache_headers()
      self.end_headers()
      self.write_bytes(open(path).read())
    else:
      self.send_response(status_codes.NOT_FOUND)

  def get_root(self):
    """Respond to a request for a new view of the underlying GUI."""
    type(self).gui._change_tracker.destroy()
    type(self).gui._create_change_tracker()
    self.get_static_file('index.html')

  def get_command(self):
    """Respond to a request for a JavaScript command to execute.

    If no commands become available after a few seconds, returns nothing,
    just so that if a request is cancelled (e.g. by page-close),
    the response thread won't linger too long.
    """
    try:
      command = type(self).gui._change_tracker.flush_changes()
      self.send_response(status_codes.OK)
      self.send_no_cache_headers()
      self.end_headers()
      self.write_bytes(command)
    except socket.error:
      # The client stopped listening while we were waiting. Oh well!
      pass

  def post_event(self):
    """Parse the event from the client and notify the GUI."""
    data = read_json(self.headers, self.rfile)
    event = browsergui.events.Event.from_dict(data)
    self.send_response(status_codes.OK)
    self.end_headers()
    type(self).gui.dispatch_event(event)

  def send_no_cache_headers(self):
    """Add headers to the response telling the client to not cache anything."""
    # Source: http://stackoverflow.com/questions/49547/making-sure-a-web-page-is-not-cached-across-all-browsers
    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
    self.send_header('Pragma', 'no-cache')
    self.send_header('Expires', '0')

  def write_bytes(self, x):
    """Write bytes or a string to the client.

    :type x: str or bytes

    TO DO: rename to stop sounding like the argument should be ``bytes``.
    """
    if isinstance(x, str):
      x = x.encode()
    self.wfile.write(x)

def make_request_handler_class_for_gui(served_gui, quiet=False):
  class _AnonymousGUIRequestHandlerSubclass(GUIRequestHandler, object):
    gui = served_gui
  if quiet:
    def noop(*args): pass
    _AnonymousGUIRequestHandlerSubclass.log_message = noop
  return _AnonymousGUIRequestHandlerSubclass

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Server that responds to each request in a separate thread."""
  pass

def make_server_for_gui(gui, port=None, quiet=False):

  handler_class = make_request_handler_class_for_gui(gui, quiet=quiet)

  if port is None:
    port = 0

  return ThreadedHTTPServer(('localhost', port), handler_class)

def point_browser_to_server(server, quiet=False):
  port = server.socket.getsockname()[1]
  url = "http://localhost:{}".format(port)
  if not quiet:
    print('Directing browser to {}'.format(url))
  webbrowser.open(url)
