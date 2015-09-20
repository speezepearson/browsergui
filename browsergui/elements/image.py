import base64
import re
import os.path
from . import LeafElement

class Image(LeafElement):
  def __init__(self, filename, format=None, **kwargs):
    """
    :param str filename: the name of the file to read image data from
    :param str format: the image's file format, or None to guess from filename
    """
    super(Image, self).__init__(tag_name='img', **kwargs)

    self.filename = filename
    if format is None:
      _, format = os.path.splitext(filename)
      format = format[1:]
      if not format:
        raise ValueError('no format given and none guessable from filename '+filename)
    self.format = format

    self.reload_data()

  @property
  def data(self):
    '''The raw image data, as bytes.'''
    src = self.tag.getAttribute('src')
    base64_data = re.search(r'base64,(.*)', src).group(1)
    return base64.b64decode(base64_data)

  def reload_data(self):
    """Reads image contents from disk, in case they've changed."""
    with open(self.filename, 'rb') as f:
      data = f.read()
    self.tag.setAttribute('src', 'data:image/{format};base64,{data}'.format(format=self.format, data=base64.b64encode(data).decode('ascii')))
    self.mark_dirty()
