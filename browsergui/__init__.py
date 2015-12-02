"""Tools for building GUIs that use a browser as the front-end.

.. autosummary::

   elements
   events
   GUI

.. autoclass:: GUI
   :members:
"""

from ._gui import GUI

from . import elements, events
from .elements import *
from .events import *
