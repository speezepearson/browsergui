import re
import numbers
from . import Element

class Viewport(Element):
  """A scrollable window into some other (probably big) element.

  Width and height can be accessed or changed using the `width` and `height` attributes.

  :param Element target: the element to be displayed inside the box
  :param int width: the width, in pixels, of the viewport
  :param int height: the height, in pixels, of the viewport
  """
  def __init__(self, target, width, height, **kwargs):
    if not isinstance(target, Element):
      raise TypeError('expected Element, got {}'.format(type(target).__name__))
    super(Viewport, self).__init__(tag_name='div', **kwargs)

    self.styles['overflow'] = 'scroll'
    self.styles['width'] = '0'
    self.styles['height'] = '0'
    self.width = width
    self.height = height

    target.parent = self
    self.target = target
    self.tag.appendChild(target.tag)

  @property
  def children(self):
    return (self.target,)

  @property
  def width(self):
    return int(self.styles['width'])
  @width.setter
  def width(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('width must be a non-negative number, not {}'.format(type(value)))
    if value < 0:
      raise ValueError('width must be non-negative')
    self.styles['width'] = str(value)

  @property
  def height(self):
    return int(self.styles['height'])
  @height.setter
  def height(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('height must be a non-negative number, not {}'.format(type(value)))
    if value < 0:
      raise ValueError('height must be non-negative')
    self.styles['height'] = str(value)
