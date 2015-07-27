import sys
if sys.version_info >= (3, 0):
  import http.client as status_codes
  from http.server import HTTPServer, BaseHTTPRequestHandler
  from socketserver import ThreadingMixIn
else:
  import httplib as status_codes
  from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
  from SocketServer import ThreadingMixIn

import os
import cgi
import webbrowser
import json

from ..commands import Empty, Destroyed

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
CURRENT_HTML = None
CURRENT_COMMAND_STREAM = None

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
    global CURRENT_COMMAND_STREAM
    CURRENT_COMMAND_STREAM = CURRENT_GUI.command_stream()
    self.get_static_file('index.html')

  def get_command(self):
    """Respond to a request for a JavaScript command to execute.

    If no commands become available after a few seconds, returns nothing,
    just so that if a request is cancelled (e.g. by page-close),
    the response thread won't linger too long.
    """
    try:
      try:
        command = CURRENT_COMMAND_STREAM.get()
      except Destroyed:
        self.send_error(status_codes.NOT_FOUND)
        self.end_headers()
      else:
        self.send_response(status_codes.OK)
        self.send_no_cache_headers()
        self.end_headers()
        self.write_bytes(command)
    except BrokenPipeError:
      # The client stopped listening while we were waiting. Oh well!
      pass

  def post_event(self):
    """Parse the event from the client and notify the GUI."""
    data = read_json(self.headers, self.rfile)
    self.send_response(status_codes.OK)
    self.end_headers()
    CURRENT_GUI.dispatch_event(data)

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
  # When the server shuts down, we don't care about being nice to the client.
  # Therefore, it's okay if the request-handling threads get killed rudely.
  #   (this will happen often with the long-polling ``command`` request)
  # So we make them daemons.
  #
  # ################# WARNING #################
  # THIS MUST CHANGE if any thread is to modify state external to the program.
  # The daemon threads could be halted without warning at any point,
  #  possibly leaving the external resources in an inconsistent state.

  daemon_threads = True

def serve_forever(gui, server_class=ThreadedHTTPServer, request_handler_class=GUIRequestHandler, port=62345, quiet=False):
  """Start a server that will display the given GUI when a browser asks for it.

  :param bool quiet: whether to suppress the server's normal response-handling info messages
  """
  global CURRENT_GUI
  CURRENT_GUI = gui
  if quiet:
    def noop(*args): pass
    request_handler_class.log_message = noop

  server = server_class(('localhost', port), request_handler_class)
  server.serve_forever()

def run(gui, open_browser=True, port=62345, **kwargs):
  """Helper function to simply display a GUI in the browser.

  :param bool open_browser: whether to immediately display the GUI in a new browser window
  :param kwargs: passed through to :func:`serve_forever`
  """
  if open_browser:
    url = "http://localhost:{}".format(port)
    print('Directing browser to {}'.format(url))
    webbrowser.open(url)

  print('Starting server. Use <Ctrl-C> to stop.')
  try:
    serve_forever(gui, port=port, **kwargs)
  except KeyboardInterrupt:
    print("Keyboard interrupt received. Quitting.")
    gui.destroy_streams()
