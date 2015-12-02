'''Defines ``Events`` that represent actions taken by the user.

You can attach :class:`Events <Event>` to :class:`Elements <Element>` to make sure certain functions get called when the user takes the corresponding kind of action:

    >>> e = Element(tag_name='input')
    >>> e.callbacks[Input] = (lambda event: print(event.value))

The predefined types of Event are:

.. autosummary::

   Click
   Input
   Change
'''

def _dict_to_javascript_object(dict):
  return ''.join((
    '{',
    ', '.join('{}: {}'.format(k, v) for k, v in sorted(dict.items())),
    '}'))

class Event(object):
  '''Represents an event triggered by the user interacting with an Element.

  The Event life cycle:

  - Every Event subclass has a ``javascript_type_name``, which is the name of the corresponding kind of JS event. (The subclass should also use ``Event.register_subclass`` to ensure that it will be instantiated when notifications with that type-name are received; see below.)
  - An Event subclass can enable itself on a tag, so that when that tag handles an event of that type-name in the browser, the server is sent a dict. That dict describes the browser-side event, including the type-name.
  - That type-name is looked up in a table to determine which Event subclass to instantiate. (Subclasses are added to the table via ``Event.register_subclass``.)
  - The subclass is instantiated, using the dict as ``**kwargs``.

  :param str target_id: the ``id`` attribute of the HTML tag interacted with.
  '''
  def __init__(self, target_id, **kwargs):
    super(Event, self).__init__(**kwargs)
    self.target_id = target_id

  @classmethod
  def enable_server_notification(cls, tag):
    '''Attach JS to a tag to notify the server when this event happens targeting the given tag.

    :param xml.dom.minidom.Element tag:
    '''
    tag.setAttribute(
      'on'+cls.javascript_type_name,
      'notify_server({})'.format(_dict_to_javascript_object(cls.dict_to_notify_server())))

  @classmethod
  def disable_server_notification(cls, tag):
    '''Remove server-notification JS for this event from the given tag.'''
    if 'on'+cls.javascript_type_name not in tag.attributes.keys():
      raise KeyError("tag is not set up to notify server for {} events".format(cls.__name__))
    tag.removeAttribute('on'+cls.javascript_type_name)

  @classmethod
  def dict_to_notify_server(cls):
    '''The information the browser should send the server when an event occurs.

    Returns a dict where the keys are strings, and the values are strings (JS expressions to be evaluated and stuck into the server notification).

    Example: for the Click event, the JS to notify the server would be:

            notify_server({target_id: this.getAttribute("id"), type_name: "click"})

    so ``dict_to_notify_server`` should return

            {'target_id': 'this.getAttribute("id")', 'type_name': '"click"'}
    '''
    return dict(
      target_id='this.getAttribute("id")',
      type_name='event.type')

  registered_subclasses_by_name = {}
  @staticmethod
  def register_subclass(cls):
    '''Decorator to add the class to the (JS-type-name -> class) table.'''
    Event.registered_subclasses_by_name[cls.javascript_type_name] = cls
    return cls

  @staticmethod
  def from_dict(event_dict):
    '''Parse a dict received from the browser into an Event instance.'''
    type_name = event_dict.pop('type_name')
    cls = Event.registered_subclasses_by_name[type_name]
    return cls.from_dict_of_right_type(event_dict)

  @classmethod
  def from_dict_of_right_type(cls, event_dict):
    return cls(**event_dict)

@Event.register_subclass
class Click(Event):
  '''Fired when the user clicks on an element.'''
  javascript_type_name = 'click'

@Event.register_subclass
class Input(Event):
  '''Fired when the user changes the value of an input-type element, in some sense.'''
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
  '''Fired when the user changes the value of an input-type element, in some sense.

  To be honest, I don't really know the difference between the "input" and "change" JavaScript events.
  '''
  javascript_type_name = 'change'

  def __init__(self, value, **kwargs):
    super(Change, self).__init__(**kwargs)
    self.value = value

  @classmethod
  def dict_to_notify_server(cls):
    return dict(
      value='this.value',
      **super(Change, cls).dict_to_notify_server())
