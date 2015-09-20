from .text import Text
from ..events import Click

class Button(Text):
  """A simple button that does something when clicked."""
  def __init__(self, text="Click!", callback=None, **kwargs):
    """
    :param str text: the label of the button
    :param callback: the function to be called
    :type callback: function of zero arguments
    """
    if not isinstance(text, str):
      raise TypeError(text)
    super(Button, self).__init__(text, tag_name="button", **kwargs)
    if callback is not None:
      self.set_callback(callback)

  def set_callback(self, callback):
    """Sets the function to be called whenever the button is clicked.

    :param callback: the function to be called
    :type callback: function of zero arguments
    """
    if self.callbacks[Click]:
      self.remove_callback(Click, self.callbacks[Click][0])
    self.add_callback(Click, (lambda event: callback()))
