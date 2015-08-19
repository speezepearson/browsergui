import datetime
import logging
from .input_field import InputField

logger = logging.Logger('browsergui.DateField')

CLIENT_DATE_FORMAT = '%Y-%m-%d'

class DateField(InputField):

  warn_about_potential_browser_incompatibility = True

  def __init__(self, **kwargs):
    super(DateField, self).__init__(**kwargs)
    self.tag.setAttribute('type', 'date')

    if self.warn_about_potential_browser_incompatibility:
      logger.warning('DateField not supported in all major browsers (as of August 2015)')

  @staticmethod
  def value_from_xml_string(s):
    return datetime.datetime.strptime(s, CLIENT_DATE_FORMAT).date() if s else None

  @staticmethod
  def value_to_xml_string(value):
    return '' if value is None else value.strftime(CLIENT_DATE_FORMAT)
