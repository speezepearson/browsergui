CLICK = "click"
KEYDOWN = "keydown"
KEYUP = "keyup"

def _dict_to_javascript_object(dict):
  return ''.join((
    '{',
    ', '.join('{}: {}'.format(k, v) for k, v in dict.items()),
    '}'))

class Event(object):

  def __init__(self, target_id, type_name, **kwargs):
    super(Event, self).__init__(**kwargs)
    self.target_id = target_id
    self.type_name = type_name

  @classmethod
  def from_dict(cls, event_dict):
    return cls(**event_dict)

  @classmethod
  def enable_server_notification(cls, type_name, tag):
    tag.setAttribute(
      'on'+type_name,
      'notify_server({})'.format(_dict_to_javascript_object(cls.dict_to_notify_server())))

  @classmethod
  def disable_server_notification(cls, type_name, tag):
    tag.removeAttribute('on'+type_name)

  @classmethod
  def dict_to_notify_server(cls):
    return dict(
      target_id='this.getAttribute("id")',
      type_name='event.type')
