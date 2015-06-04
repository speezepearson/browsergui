from json import dumps as j

def compound(commands):
  return "; ".join(commands)

def selector(element):
  return "#"+element.id

def jquery_method_call(element, method_name, *arg_strings):
  return "$({selector}).{method_name}({args_string})".format(
    selector=j(selector(element)),
    method_name=method_name,
    args_string=", ".join(arg_strings))

from . import dom_modification
from .dom_modification import *

from . import callbacks
from .callbacks import *

from . import command_stream
from .command_stream import *