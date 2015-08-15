
def _dict_to_javascript_object(dict):
  return ''.join((
    '{',
    ', '.join('{}: {}'.format(k, v) for k, v in dict.items()),
    '}'))

class Event(object):

  def __init__(self, target_id, **kwargs):
    super(Event, self).__init__(**kwargs)
    self.target_id = target_id

  @classmethod
  def from_dict(cls, event_dict):
    return cls(**event_dict)

  @classmethod
  def enable_server_notification(cls, tag):
    tag.setAttribute(
      'on'+cls.javascript_type_name,
      'notify_server({})'.format(_dict_to_javascript_object(cls.dict_to_notify_server())))

  @classmethod
  def disable_server_notification(cls, tag):
    tag.removeAttribute('on'+cls.javascript_type_name)

  @classmethod
  def dict_to_notify_server(cls):
    return dict(
      target_id='this.getAttribute("id")',
      type_name='event.type')

class Click(Event):
  javascript_type_name = 'click'

EVENT_TYPES_BY_NAME = {
  cls.javascript_type_name: cls
  for cls in [Click]}

def from_dict(event_dict):
  type_name = event_dict.pop('type_name')
  for cls_type_name, cls in EVENT_TYPES_BY_NAME.items():
    if type_name == cls_type_name:
      return cls.from_dict(event_dict)
