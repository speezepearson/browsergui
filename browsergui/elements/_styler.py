import collections

class Styler(collections.MutableMapping):
  def __init__(self, element, **kwargs):
    self.element = element
    self.rules = {}
    super(Styler, self).__init__(**kwargs)

  def _update_tag_style_attribute(self):
    if self:
      self.element.tag.setAttribute('style', self._css())
    elif 'style' in self.element.tag.attributes.keys():
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
