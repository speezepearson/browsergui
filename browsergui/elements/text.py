import xml.dom.minidom
from . import Element

class Text(Element):
  """Some simple text."""
  def __init__(self, text, tag_name="span"):
    if not isinstance(text, str):
      raise TypeError(text)
    super(Text, self).__init__(tag_name=tag_name)
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
    if self.gui is not None:
      self.gui.send_command("document.getElementById({id}).data = {text}".format(
        id=json.dumps(self.id),
        text=json.dumps(value)))

class CodeSnippet(Text):
  """Inline text representing computer code."""
  def __init__(self, text):
    super(CodeSnippet, self).__init__(text, tag_name="code")
    self.set_styles(**{'white-space': 'pre'})
class Paragraph(Text):
  """A block of plain text."""
  def __init__(self, text):
    super(Paragraph, self).__init__(text, tag_name="p")
class CodeBlock(Text):
  """A block of computer code."""
  def __init__(self, text):
    super(CodeBlock, self).__init__(text, tag_name="pre")
