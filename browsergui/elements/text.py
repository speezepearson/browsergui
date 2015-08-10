import json
import xml.dom.minidom
from . import LeafElement

class Text(LeafElement):
  """Some simple text."""
  def __init__(self, text, tag_name="span", **kwargs):
    if not isinstance(text, str):
      raise TypeError(text)
    super(Text, self).__init__(tag_name=tag_name, **kwargs)
    self._text = xml.dom.minidom.Text()
    self._text.data = text
    self.tag.appendChild(self._text)

  @property
  def text(self):
    """docstring"""
    return self._text.data
  @text.setter
  def text(self, value):
    """docstring"""
    if self.text == value:
      return

    self._text.data = value
    self.mark_dirty()

class CodeSnippet(Text):
  """Inline text representing computer code."""
  def __init__(self, text, **kwargs):
    super(CodeSnippet, self).__init__(text, tag_name="code", **kwargs)
    self.set_styles(**{'white-space': 'pre'})
class Paragraph(Text):
  """A block of plain text."""
  def __init__(self, text, **kwargs):
    super(Paragraph, self).__init__(text, tag_name="p", **kwargs)
class CodeBlock(Text):
  """A block of computer code."""
  def __init__(self, text, **kwargs):
    super(CodeBlock, self).__init__(text, tag_name="pre", **kwargs)
