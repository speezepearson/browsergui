import unittest
import browsergui
import threading
import sys
if sys.version_info >= (3, 0):
  from http.client import HTTPConnection
else:
  from httplib import HTTPConnection

from browsergui._server import make_request_handler_class_for_gui, ThreadedHTTPServer

class ServerTest(unittest.TestCase):
  def setUp(self):
    self.gui = browsergui.GUI()
    self.handler_class = make_request_handler_class_for_gui(self.gui, quiet=True)
    self.server = ThreadedHTTPServer(('localhost', 0), self.handler_class)

  def tearDown(self):
    self.server.socket.close()

  def request(self, *args, **kwargs):
    timeout = kwargs.pop('timeout', 1)
    thread = threading.Thread(target=self.server.handle_request)
    thread.daemon = True
    thread.start()
    conn = HTTPConnection('localhost', self.server.socket.getsockname()[1])
    conn.request(*args, **kwargs)
    result = conn.getresponse().read()

    thread.join(timeout)
    if thread.is_alive():
      raise Exception('request-handling thread timed out')

    return result

  def test_is_responsive(self):
    # This test assumes that the first request to /command will not block.
    # (At the time of writing, that's true, because the GUI sends a startup
    #  command that wipes out and rewrites the entire document. If that stops
    #  being true, this test will need to be changed.)
    self.assertTrue(self.request('GET', '/command'))
