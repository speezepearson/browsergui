"""Tools for using a browser as a GUI.

Uses a browser as a dumb terminal (in the old sense), which just dumbly obeys the server and reports back when the user interacts with it.

The central concepts here are:

- The "GUI," which ...
- The "element," which ...
"""

from . import server, gui, elements
from .gui import GUI
from .elements import Element, Container, Button, Text, Paragraph, CodeSnippet, CodeBlock
from .server import run
