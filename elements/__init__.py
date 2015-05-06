import collections
import json

_unique_id_counter = 0
def unique_id():
  global _unique_id_counter
  _unique_id_counter += 1
  return "_element_{}".format(_unique_id_counter)

class Element:
  def __init__(self, gui, id=None):
    self.gui = gui
    self.id = id if id else unique_id()
    self.callbacks = collections.defaultdict(list)

    self.gui.add_element(self)

  def __str__(self):
    return "(#{})".format(self.id)

  def __repr__(self):
    return "Element({!r}, {!r})".format(self.gui, self.id)

  def add_child(self, tag, id=None, contents=""):
    result = Element(self.gui, id)
    html = """<{tag} id="{id}">{contents}</{tag}>""".format(tag=tag, id=result.id, contents=contents)
    self.call_method("append", json.dumps(html))
    return result

  @property
  def selector(self):
    return "#"+self.id

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
