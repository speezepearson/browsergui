import re
import datetime
from .. import NotUniversallySupportedElement
from ._inputfield import InputField

CLIENT_DATE_FORMAT = '%Y-%m-%d'

class DateField(InputField, NotUniversallySupportedElement):
  '''A field where the user can input a date.

  Inherits from :class:`ValuedElement`, meaning it has a ``value``, ``placeholder``, and ``change_callback``.
  '''
  def __init__(self, placeholder='yyyy-mm-dd', **kwargs):
    super(DateField, self).__init__(placeholder=placeholder, **kwargs)
    self.tag.setAttribute('type', 'date')

  def _value_to_xml_string(self, value):
    if value is None:
      return ''
    elif hasattr(value, 'strftime'):
      return value.strftime(CLIENT_DATE_FORMAT)
    raise TypeError('expected value to be datelike (have `strftime` method), got {}'.format(type(value).__name__))

  def _value_from_xml_string(self, string):
    if not string:
      return None

    # Kludge incoming.
    # Some browsers don't support date-input fields, and display them as text instead.
    # We still get notified about changes, but the reported value might be malformed.
    # In this case, we might get '2013-3-1' as a value, which I don't think should be accepted.
    # However, `date.strptime` will happily parse it. So we have to throw an error here.
    if not re.match(r'\d{4}-\d{2}-\d{2}', string):
      raise ValueError('malformed date: {!r}'.format(string))
    return datetime.datetime.strptime(string, CLIENT_DATE_FORMAT).date()
