
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

  registered_subclasses_by_name = {}
  @staticmethod
  def register_subclass(cls):
    Event.registered_subclasses_by_name[cls.javascript_type_name] = cls
    return cls

  @staticmethod
  def from_dict(event_dict):
    type_name = event_dict.pop('type_name')
    cls = Event.registered_subclasses_by_name[type_name]
    return cls.from_dict_of_right_type(event_dict)

  @classmethod
  def from_dict_of_right_type(cls, event_dict):
    return cls(**event_dict)

@Event.register_subclass
class Click(Event):
  javascript_type_name = 'click'

@Event.register_subclass
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

@Event.register_subclass
class Change(Event):
  javascript_type_name = 'change'

  def __init__(self, value, **kwargs):
    super(Change, self).__init__(**kwargs)
    self.value = value

  @classmethod
  def dict_to_notify_server(cls):
    return dict(
      value='this.value',
      **super(Change, cls).dict_to_notify_server())
