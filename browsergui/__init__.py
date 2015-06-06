"""Tools for using a browser as a GUI.

The central concepts here are:

- The "GUI," which ...
- The "element," which ...
"""

from . import server, gui, elements, utilities
from .gui import GUI
from .elements import Element, Container, Button, Text, Paragraph, CodeSnippet, CodeBlock
from .server import run
from .utilities import RepeatingTimer, call_in_background