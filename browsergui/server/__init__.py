import socket

import os
import cgi
import webbrowser
import json

from ..pythoncompatibility import (
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

CURRENT_GUI = None

class GUIRequestHandler(BaseHTTPRequestHandler):
  """Handler for GUI-related requests.

  There are four main types of request:

  - client asking for the root page
  - client asking for a static resource required by the root page
  - client asking for a lump of JavaScript to execute
  - client notifying server of some user interaction in the browser
  """

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
    CURRENT_GUI.make_new_document(destroy=True)
    self.get_static_file('index.html')

  def get_command(self):
    """Respond to a request for a JavaScript command to execute.

    If no commands become available after a few seconds, returns nothing,
    just so that if a request is cancelled (e.g. by page-close),
    the response thread won't linger too long.
    """
    try:
      command = CURRENT_GUI.change_tracker.flush_changes()
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
    event = browsergui.events.from_dict(data)
    self.send_response(status_codes.OK)
    self.end_headers()
    CURRENT_GUI.dispatch_event(event)

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

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Server that responds to each request in a separate thread."""
  pass

def run(gui, open_browser=True, port=0, quiet=False):
  """Helper function to simply display a GUI in the browser.

  :param bool open_browser: whether to immediately display the GUI in a new browser window
  :param kwargs: passed through to :func:`serve_forever`
  """
  global CURRENT_GUI
  CURRENT_GUI = gui

  if quiet:
    def noop(*args): pass
    GUIRequestHandler.log_message = noop

  server = ThreadedHTTPServer(('localhost', port), GUIRequestHandler)
  if port == 0:
    port = server.socket.getsockname()[1]

  if open_browser:
    url = "http://localhost:{}".format(port)
    print('Directing browser to {}'.format(url))
    webbrowser.open(url)

  print('Starting server. Use <Ctrl-C> to stop.')
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print("Keyboard interrupt received. Quitting.")
    gui.destroy()
