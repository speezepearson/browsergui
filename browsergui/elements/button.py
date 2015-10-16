from .text import Text
from ..events import Click

class Button(Text):
  """A simple button that does something when clicked.

  The ``text`` and ``callback`` fields may be safely set at any time.

  :param str text: the label of the button
  :param callback: the function to be called
  :type callback: function of zero arguments, or None
  """
  def __init__(self, text="Click!", callback=None, **kwargs):
    if not isinstance(text, str):
      raise TypeError(text)
    super(Button, self).__init__(text, tag_name="button", **kwargs)
    self.callback = callback
    self.callbacks[Click] = self._handle_click

  def _handle_click(self, event):
    if self.callback is not None:
      self.callback()
