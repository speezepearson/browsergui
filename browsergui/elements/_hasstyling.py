def styling_to_css(styling):
  return ' '.join('{}: {};'.format(key, value) for key, value in styling.items())

class HasStyling(object):
  def __init__(self, **kwargs):
    super(HasStyling, self).__init__(**kwargs)
    self._styling = {}

  def set_styles(self, **rules):
    self._styling.update(**rules)
    self._update_styles()

  def get_style(self, property):
    return self._styling.get(property)

  def delete_styles(self, *properties):
    for property in properties:
      self._styling.pop(property, None)
    self._update_styles()

  def toggle_visibility(self):
    """Toggles whether the element can be seen or not."""
    if self._styling.get('display') == 'none':
      self.delete_styles('display')
    else:
      self.set_styles(display='none')

  def _update_styles(self):
    self.tag.setAttribute('style', styling_to_css(self._styling))
    self.mark_dirty()
