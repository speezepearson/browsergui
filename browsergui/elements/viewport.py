import re
import numbers
from . import Element

class Viewport(Element):
  """A scrollable window into some other (probably big) element."""
  def __init__(self, target, width, height):
    super(Viewport, self).__init__(tag_name="div", children=[target])
    self.tag.attributes['style'] = 'overflow: scroll; width: 0; height: 0'.format(w=width, h=height)
    self.width = width
    self.height = height

  @property
  def width(self):
    value = self.tag.attributes['style'].value
    match = re.search(r'width: (\d+)', value)
    return int(match.group(1))
  @width.setter
  def width(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('width must be a non-negative number, not {}'.format(type(value)))
    if value < 0:
      raise ValueError('width must be non-negative')
    style = self.tag.attributes['style'].value
    self.tag.attributes['style'] = re.sub(r'width: \d+', 'width: {}'.format(int(value)), style)

  @property
  def height(self):
    value = self.tag.attributes['style'].value
    match = re.search(r'height: (\d+)', value)
    return int(match.group(1))
  @height.setter
  def height(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('height must be a non-negative number, not {}'.format(type(value)))
    if value < 0:
      raise ValueError('height must be non-negative')
    style = self.tag.attributes['style'].value
    self.tag.attributes['style'] = re.sub(r'height: \d+', 'height: {}'.format(value), style)
