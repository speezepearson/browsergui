import datetime
from . import NotUniversallySupportedElement
from .input_field import InputField

CLIENT_DATE_FORMAT = '%Y-%m-%d'

class DateField(InputField, NotUniversallySupportedElement):
  def __init__(self, **kwargs):
    super(DateField, self).__init__(**kwargs)
    self.tag.setAttribute('type', 'date')

  def value_from_xml_string(self, s):
    return datetime.datetime.strptime(s, CLIENT_DATE_FORMAT).date() if s else None

  def value_to_xml_string(self, value):
    return '' if value is None else value.strftime(CLIENT_DATE_FORMAT)

  def ensure_is_valid_value(self, value):
    if not (value is None or hasattr(value, 'strftime')):
      raise TypeError('expected value to be datelike (have `strftime` method), got {}'.format(type(value).__name__))
    to_string_and_back = self.value_from_xml_string(self.value_to_xml_string(value))
    if to_string_and_back != value:
      raise ValueError('value {!r} does not convert to XML and back as it should'.format(value))
    super(DateField, self).ensure_is_valid_value(value)
