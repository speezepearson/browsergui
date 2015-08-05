import re
import numbers
from . import Element

class Viewport(Element):
  """A scrollable window into some other (probably big) element."""
  def __init__(self, target, width, height, **kwargs):
    if not isinstance(target, Element):
      raise TypeError('expected Element, got {}'.format(type(target).__name__))
    super(Viewport, self).__init__(tag_name='div', **kwargs)
    self.tag.appendChild(target.tag)
    self.tag.setAttribute('style', 'overflow: scroll; width: 0; height: 0'.format(w=width, h=height))
    self.target = target
    self.width = width
    self.height = height

  @property
  def children(self):
    return (self.target,)

  @property
  def width(self):
    value = self.tag.getAttribute('style')
    match = re.search(r'width: (\d+)', value)
    return int(match.group(1))
  @width.setter
  def width(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('width must be a non-negative number, not {}'.format(type(value)))
    if value < 0:
      raise ValueError('width must be non-negative')
    style = self.tag.getAttribute('style')
    self.tag.setAttribute('style', re.sub(r'width: \d+', 'width: {}'.format(int(value)), style))

  @property
  def height(self):
    value = self.tag.getAttribute('style')
    match = re.search(r'height: (\d+)', value)
    return int(match.group(1))
  @height.setter
  def height(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('height must be a non-negative number, not {}'.format(type(value)))
    if value < 0:
      raise ValueError('height must be non-negative')
    style = self.tag.getAttribute('style')
    self.tag.setAttribute('style', re.sub(r'height: \d+', 'height: {}'.format(value), style))
