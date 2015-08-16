from ._node import Node
from ._hastag import HasTag

class HasGUI(Node, HasTag):
  @property
  def gui(self):
    """The GUI the element belongs to, or None if there is none."""
    return (None if self.orphaned else self.parent.gui)

  def mark_dirty(self):
    if self.gui is not None:
      self.gui.change_tracker.mark_dirty(self.tag)