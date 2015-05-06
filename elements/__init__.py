import collections
import json

_unique_id_counter = 0
def unique_id():
  global _unique_id_counter
  _unique_id_counter += 1
  return "_element_{}".format(_unique_id_counter)

class Element:
  def __init__(self, parent=None, id=None):
    self.parent = parent
    self.id = id if id else unique_id()
    self.callbacks = collections.defaultdict(list)

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "Element({!r}, {!r})".format(self.parent, self.id)

  def append(self, child):
    if not child.orphaned:
      raise RuntimeError("can only insert orphaned elements")
    self.call_method("append", json.dumps(child.html))
    child.parent = self
    self.gui.add_element(child)

  @property
  def selector(self):
    return "#"+self.id

  @property
  def html(self):
    return """<{tag} id={id}>{contents}</{tag}>""".format(tag=self.tag, id=self.id, contents=self.contents)

  @property
  def orphaned(self):
    return (self.parent is None)

  @property
  def gui(self):
    return None if self.parent is None else self.parent.gui if isinstance(self.parent, Element) else self.parent

  @property
  def container(self):
    return self.parent if isinstance(self.parent, Element) else None

  def call_method(self, method_name, *args):
    arg_string = ", ".join(args)
    self.gui.send_js_command('$({}).{}({})'.format(json.dumps(self.selector), method_name, arg_string))

  def add_callback(self, event_type, callback):
    if not self.callbacks[event_type]:
      self.gui.send_js_command("""
        $({selector}).on({type}, function() {{
          notify_server({{
            type: {type},
            id: {id}
          }})
        }})""".format(selector=json.dumps(self.selector), type=json.dumps(event_type), id=json.dumps(self.id)))
    self.callbacks[event_type].append(callback)

  def handle_event(self, event):
    for callback in self.callbacks[event["type"]]:
      callback(event)

class Button(Element):
  
  tag = "button"

  def __init__(self, text, **kwargs):
    super().__init__(**kwargs)
    self.text = text

  @property
  def contents(self):
    return self.text

class Div(Element):
  tag = "div"
  def __init__(self, contents="", **kwargs):
    super().__init__(**kwargs)
    self.contents = contents
