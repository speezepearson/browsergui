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

from ..command_stream import Empty, Destroyed

ROOT_PATH = "/"
JQUERY_PATH = "/jquery.min.js"
PUPPET_PATH = "/puppet.js"
COMMAND_PATH = "/command"
EVENT_PATH = "/event"

def parse_post_data(headers, rfile):
  ctype, pdict = cgi.parse_header(headers['content-type'])
  if ctype == 'multipart/form-data':
    result = cgi.parse_multipart(rfile, pdict)
  elif ctype == 'application/x-www-form-urlencoded':
    length = int(headers['content-length'])
    result = cgi.parse_qs(rfile.read(length))
  else:
    result = {}

  return {k.decode(): v[0].decode() for k, v in result.items()}

CURRENT_GUI = None
CURRENT_HTML = None
CURRENT_COMMAND_STREAM = None

class GUIRequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    if self.path == ROOT_PATH:
      self.get_root()
    elif self.path == JQUERY_PATH:
      self.get_static_file("jquery.min.js")
    elif self.path == PUPPET_PATH:
      self.get_static_file("puppet.js")
    elif self.path == COMMAND_PATH:
      self.get_command()

  def do_POST(self):
    if self.path == EVENT_PATH:
      self.post_event()

  def get_static_file(self, relpath):
    path = os.path.join(os.path.dirname(__file__), relpath)
    if os.path.exists(path):
      self.send_response(status_codes.OK)
      self.send_no_cache_headers()
      self.end_headers()
      self.write_bytes(open(path).read())
    else:
      self.send_response(status_codes.NOT_FOUND)

  def get_root(self):
    path = os.path.join(os.path.dirname(__file__), "index.html")
    self.send_response(status_codes.OK)
    self.send_no_cache_headers()
    self.end_headers()
    global CURRENT_HTML, CURRENT_COMMAND_STREAM
    CURRENT_HTML, CURRENT_COMMAND_STREAM = CURRENT_GUI.html_and_command_stream()
    self.write_bytes(open(path).read().replace("<!-- GUI_HTML -->", CURRENT_HTML))

  def get_command(self):
    try:
      command = CURRENT_COMMAND_STREAM.get(timeout=5)
    except Empty:
      self.send_response(status_codes.NO_CONTENT)
      self.end_headers()
    except Destroyed:
      try:
        # Try to be nice and tell the client we're over.
        self.send_error(status_codes.NOT_FOUND)
        self.end_headers()
      except:
        # But if we can't (e.g. because the socket is already closed), don't sweat it.
        pass
    else:
      self.send_response(status_codes.OK)
      self.send_no_cache_headers()
      self.end_headers()
      self.write_bytes(command)

  def post_event(self):
    data = parse_post_data(self.headers, self.rfile)
    self.send_response(status_codes.OK)
    self.end_headers()
    CURRENT_GUI.handle_event(data)

  def send_no_cache_headers(self):
    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
    self.send_header('Pragma', 'no-cache')
    self.send_header('Expires', '0')

  def write_bytes(self, x):
    if isinstance(x, str):
      x = x.encode()
    self.wfile.write(x)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

def serve_forever(gui, server_class=ThreadedHTTPServer, request_handler_class=GUIRequestHandler, port=62345, quiet=False):
  global CURRENT_GUI
  CURRENT_GUI = gui
  if quiet:
    def noop(*args): pass
    request_handler_class.log_message = noop

  server = server_class(('localhost', port), request_handler_class)
  server.serve_forever()

def run(gui, open_browser=True, port=62345, **kwargs):
  if open_browser:
    url = "http://localhost:{}".format(port)
    print('Directing browser to {}'.format(url))
    webbrowser.open(url)

  print('Starting server. Use <Ctrl-C> to stop.')
  try:
    serve_forever(gui, port=port, **kwargs)
  except KeyboardInterrupt:
    print("Keyboard interrupt received. Quitting.")
    gui.destroy()
