import re
import numbers
from .. import Element

class Viewport(Element):
  """A scrollable window into some other (probably big) element."""
  def __init__(self, target, width, height, **kwargs):
    if not isinstance(target, Element):
      raise TypeError('expected Element, got {}'.format(type(target).__name__))
    super(Viewport, self).__init__(tag_name='div', **kwargs)

    self.css.update(overflow='scroll', width='0', height='0')
    self.width = width
    self.height = height

    self._target = None
    self.target = target

  @property
  def target(self):
    '''The Element being viewed through the Viewport.'''
    return self._target
  @target.setter
  def target(self, new_target):
    if self._target is not None:
      self.tag.removeChild(self._target.tag)
    self._target = new_target
    self.tag.appendChild(new_target.tag)
    self.mark_dirty()

  @property
  def width(self):
    '''The Viewport's width, in pixels.'''
    return int(self.css['width'])
  @width.setter
  def width(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('width must be a non-negative number, not {}'.format(type(value)))
    if value < 0:
      raise ValueError('width must be non-negative')
    self.css['width'] = str(value)
    self.mark_dirty()

  @property
  def height(self):
    '''The Viewport's height, in pixels.'''
    return int(self.css['height'])
  @height.setter
  def height(self, value):
    if not isinstance(value, numbers.Real):
      raise TypeError('height must be a non-negative number, not {}'.format(type(value)))
    if value < 0:
      raise ValueError('height must be non-negative')
    self.css['height'] = str(value)
    self.mark_dirty()
