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

def selector(element):
  """Returns a jQuery selector for the DOM element associated with an :class:`Element`.

  :rtype: str
  """
  return "#"+element.id

def jquery_equivalent(element):
  """Command to get the jQuery DOM element corresponding to an :class:`Element`.

  :rtype: str
  """
  return "$({})".format(j(selector(element)))

def jquery_method_call(element, method_name, *arg_strings):
  """Command to call a method on an :class:`Element`'s jQuery equivalent.

  :param Element element: the Element whose jQuery equivalent to call the method on
  :param str method_name: name of the method to call
  :param arg_strings: JS expressions (strings) to pass to the method
  :rtype: str
  """
  return "{jq}.{method_name}({args_string})".format(
    jq=jquery_equivalent(element),
    method_name=method_name,
    args_string=", ".join(arg_strings))

from . import dom_modification
from .dom_modification import *

from . import callbacks
from .callbacks import *

from . import command_stream
from .command_stream import *