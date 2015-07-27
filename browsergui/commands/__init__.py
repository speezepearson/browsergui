"""Creation and manipulation of JavaScript commands.

This module defines many functions that return snippets (strings) of valid JavaScript.
This allows the rest of the package to remain ignorant of the semantics of JS.
"""

from json import dumps as j

def compound(commands):
  """Given many JS commands, returns a command that executes them one after the other.

  :param iterable commands: the commands to be joined
  :rtype: str
  """
  return "; ".join(commands)

def get(element):
  return "document.getElementById({})".format(j(element.id))

from . import dom_modification
from .dom_modification import *

from . import callbacks
from .callbacks import *

from . import command_stream
from .command_stream import *