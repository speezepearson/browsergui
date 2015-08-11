
def _dict_to_javascript_object(dict):
  return ''.join((
    '{',
    ', '.join('{}: {}'.format(k, v) for k, v in sorted(dict.items())),
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
    if 'on'+cls.javascript_type_name not in tag.attributes.keys():
      raise KeyError("tag is not set up to notify server for {} events".format(cls.__name__))
    tag.removeAttribute('on'+cls.javascript_type_name)

  @classmethod
  def dict_to_notify_server(cls):
    return dict(
      target_id='this.getAttribute("id")',
      type_name='event.type')

class Click(Event):
  javascript_type_name = 'click'

class Input(Event):
  javascript_type_name = 'input'

  def __init__(self, value, **kwargs):
    super(Input, self).__init__(**kwargs)
    self.value = value

  @classmethod
  def dict_to_notify_server(cls):
    return dict(
      value='this.value',
      **super(Input, cls).dict_to_notify_server())

EVENT_TYPES_BY_NAME = {
  cls.javascript_type_name: cls
  for cls in [Click, Input]}

def from_dict(event_dict):
  type_name = event_dict.pop('type_name')
  return EVENT_TYPES_BY_NAME[type_name].from_dict(event_dict)
