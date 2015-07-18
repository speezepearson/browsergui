from .text import Text
from ..events import CLICK

class Button(Text):
  """A simple button that does something when clicked."""
  def __init__(self, text="Click!", callback=None):
    """
    :param text: the label of the button
    :type text: str
    :param callback: the function to be called
    :type callback: function of zero arguments
    """
    if not isinstance(text, str):
      raise TypeError(text)
    super(Button, self).__init__(text, tag_name="button")
    if callback is not None:
      self.set_callback(callback)

  def set_callback(self, callback):
    """Sets the function to be called whenever the button is clicked.

    :param callback: the function to be called
    :type callback: function of zero arguments
    """
    if self.callbacks[CLICK]:
      self.remove_callback(CLICK, self.callbacks[CLICK][0])
    self.add_callback(CLICK, (lambda event: callback()))
