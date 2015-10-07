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

    self.callback = callback
    self.callbacks[Click] = self._handle_click_event

  def _handle_click_event(self, event):
    if self.callback is not None:
      self.callback()
