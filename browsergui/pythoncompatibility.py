import sys

if sys.version_info >= (3, 0):
  import http.client as http_status_codes
  from http.server import HTTPServer, BaseHTTPRequestHandler
  from socketserver import ThreadingMixIn as HTTPServerThreadingMixin
else:
  import httplib as http_status_codes
  from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
  from SocketServer import ThreadingMixIn as HTTPServerThreadingMixin

if sys.version_info >= (3, 3):
  import collections.abc as collections_abc
else:
  import collections as collections_abc

STRING_TYPES = (str,) if sys.version_info >= (3, 0) else (str, unicode)
