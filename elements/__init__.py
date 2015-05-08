import collections
import json

_unique_id_counter = 0
def unique_id():
  global _unique_id_counter
  _unique_id_counter += 1
  return "_element_{}".format(_unique_id_counter)

class Element:
  def __init__(self, html=None, tag_name=None, children=()):
    raise NotImplementedError()

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "Element({!r}, {!r})".format(self.parent, self.id)

  def __eq__(self, other):
    raise NotImplementedError()

  def append(self, child):
    raise NotImplementedError()

  @property
  def html(self):
    raise NotImplementedError()

  @property
  def orphaned(self):
    raise NotImplementedError()

  @property
  def parent(self):
    raise NotImplementedError()

  @property
  def gui(self):
    raise NotImplementedError()

  def add_callback(self, event_type, callback):
    raise NotImplementedError()

  def handle_event(self, event):
    raise NotImplementedError()


class Text(Element):
  def __init__(self, string):
    super().__init__(tag_name="span")
    raise NotImplementedError()
    self.string = string

class Button(Element):
  def __init__(self, text, callback=None):
    super().__init__(tag_name="button")
    raise NotImplementedError()
    self.text = text
    if callback is not None:
      self.add_callback(CLICK, callback)

  def set_callback(self, callback):
    self.callbacks[CLICK] = [callback]

class Container(Element):
  def __init__(self, *children, inline=False):
    super().__init__(tag_name=("span" if inline else "div"), children=children)
    raise NotImplementedError()
    self._inline = inline

class Image(Element):
  def __init__(self, location):
    super().__init__(tag_name="img")
    raise NotImplementedError()
    self._location = _location
    if callback is not None:
      self.add_callback(CLICK, callback)
