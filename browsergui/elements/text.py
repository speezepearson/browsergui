import json
import xml.dom.minidom
from . import LeafElement

class Text(LeafElement):
  """An element containing only a text string.

  The currently displayed string may be accessed or changed via the `text` attribute.

  :param str text: the text to display
  """
  def __init__(self, text, tag_name="span", **kwargs):
    if not isinstance(text, str):
      raise TypeError(text)
    super(Text, self).__init__(tag_name=tag_name, **kwargs)
    self._text = xml.dom.minidom.Text()
    self._text.data = text
    self.tag.appendChild(self._text)

  @property
  def text(self):
    return self._text.data
  @text.setter
  def text(self, value):
    if self.text == value:
      return

    self._text.data = value
    self.mark_dirty()

  def set_text(self, value):
    self.text = value

class CodeSnippet(Text):
  """Inline text representing computer code."""
  def __init__(self, text, **kwargs):
    super(CodeSnippet, self).__init__(text, tag_name="code", styling={'white-space': 'pre'}, **kwargs)
class Paragraph(Text):
  """A block of plain text."""
  def __init__(self, text, **kwargs):
    super(Paragraph, self).__init__(text, tag_name="p", **kwargs)
class CodeBlock(Text):
  """A block of computer code."""
  def __init__(self, text, **kwargs):
    super(CodeBlock, self).__init__(text, tag_name="pre", **kwargs)
class EmphasizedText(Text):
  """Text that should have emphasis on it."""
  def __init__(self, text, **kwargs):
    super(EmphasizedText, self).__init__(text, tag_name="strong", **kwargs)
