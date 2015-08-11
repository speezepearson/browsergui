from ._node import Node

class HasGUI(Node):
  @property
  def gui(self):
    """The GUI the element belongs to, or None if there is none."""
    return (None if self.orphaned else self.parent.gui)

  def mark_dirty(self):
    if self.gui is not None:
      self.gui.change_tracker.mark_dirty()