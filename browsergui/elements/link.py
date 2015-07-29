from .text import Text

class Link(Text):
  """A hyperlink to some URL."""
  def __init__(self, text, url):
    super(Link, self).__init__(text, tag_name="a")
    self.tag.setAttribute('target', '_blank')
    self.url = url

  @property
  def url(self):
    return self.tag.getAttribute('href')
  @url.setter
  def url(self, value):
    self.tag.setAttribute('href', value)
