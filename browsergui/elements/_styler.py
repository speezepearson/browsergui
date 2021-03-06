from .._pythoncompatibility import collections_abc

class Styler(collections_abc.MutableMapping):
  def __init__(self, element, **kwargs):
    self.element = element
    self.rules = {}
    super(Styler, self).__init__(**kwargs)

  def _update_tag_style_attribute(self):
    css = self._css()
    if css:
      self.element.tag.setAttribute('style', css)
    else:
      self.element.tag.removeAttribute('style')
    self.element.mark_dirty()

  def _css(self):
    return '; '.join('{}: {}'.format(k, v) for k, v in sorted(self.items()))

  def __getitem__(self, key):
    return self.rules[key]

  def __setitem__(self, key, value):
    self.rules[key] = value
    self._update_tag_style_attribute()

  def __delitem__(self, key):
    del self.rules[key]
    self._update_tag_style_attribute()

  def __iter__(self):
    return iter(self.rules)

  def __len__(self):
    return len(self.rules)
