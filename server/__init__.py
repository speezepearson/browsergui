from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import os
import cgi
import closablequeue

ROOT_PATH = "/"
JQUERY_PATH = "/jquery.min.js"
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


class GUIRequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    if self.path == ROOT_PATH:
      self.get_root()
    elif self.path == JQUERY_PATH:
      self.get_jquery()
    elif self.path == COMMAND_PATH:
      self.get_command()

  def do_POST(self):
    if self.path == EVENT_PATH:
      self.post_event()

  def get_root(self):
    self.send_response(200)
    self.end_headers()
    path = os.path.join(os.path.dirname(__file__), "index.html")
    self.write_bytes(open(path).read())

  def get_jquery(self):
    self.send_response(200)
    self.end_headers()
    path = os.path.join(os.path.dirname(__file__), "jquery.min.js")
    self.write_bytes(open(path).read())

  def get_command(self):
    try:
      command = self.gui.get_js_command()
    except closablequeue.Closed:
      self.send_response(400)
      self.end_headers
    else:
      self.write_bytes(command)

  def post_event(self):
    data = parse_post_data(self.headers, self.rfile)
    self.send_response(200)
    self.end_headers()
    self.gui.handle_event(data)

  def write_bytes(self, x):
    if isinstance(x, str):
      x = x.encode()
    self.wfile.write(x)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

def serve_forever(gui, server_class=ThreadedHTTPServer, request_handler_class=GUIRequestHandler, port=62345):
  request_handler_class.gui = gui # Super hack
  server = server_class(('localhost', port), request_handler_class)
  server.serve_forever()
