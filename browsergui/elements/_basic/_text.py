import json
import xml.dom.minidom
from .. import Element

class Text(Element):
  """A piece of text with no structure inside it.

  The currently displayed string may be accessed or changed via the `text` attribute.

  If you want to be fancy, a Text instance can represent any HTML tag that contains only plain text. For instance, :class:`Button` subclasses Text, even though it's not just a plain piece of text.

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
    '''The string to be displayed.'''
    return self._text.data
  @text.setter
  def text(self, value):
    if self.text == value:
      return

    self._text.data = value
    self.mark_dirty()

class CodeSnippet(Text):
  """Inline text representing ``computer code``."""
  def __init__(self, text, **kwargs):
    super(CodeSnippet, self).__init__(text, tag_name="code", css={'white-space': 'pre'}, **kwargs)
class Paragraph(Text):
  """A block of plain text."""
  def __init__(self, text, **kwargs):
    super(Paragraph, self).__init__(text, tag_name="p", **kwargs)
class CodeBlock(Text):
  """A block of ``computer code``."""
  def __init__(self, text, **kwargs):
    super(CodeBlock, self).__init__(text, tag_name="pre", **kwargs)
class EmphasizedText(Text):
  """Text that should have **emphasis** on it."""
  def __init__(self, text, **kwargs):
    super(EmphasizedText, self).__init__(text, tag_name="strong", **kwargs)

class Link(Text):
  """A `hyperlink <http://github.com/speezepearson/browsergui>`_."""
  def __init__(self, text, url, **kwargs):
    super(Link, self).__init__(text, tag_name="a", **kwargs)
    self.tag.setAttribute('target', '_blank')
    self.url = url

  @property
  def url(self):
    '''The URL to which the link points.'''
    return self.tag.getAttribute('href')
  @url.setter
  def url(self, value):
    self.tag.setAttribute('href', value)
    self.mark_dirty()
