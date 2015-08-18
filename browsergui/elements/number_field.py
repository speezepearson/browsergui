from .input_field import InputField

class NumberField(InputField):

  def __init__(self, value=None, **kwargs):
    if value is not None:
      value = float(value)
    super(NumberField, self).__init__(value=value, **kwargs)
    self.tag.setAttribute('type', 'number')

  @staticmethod
  def value_from_xml_string(s):
    return float(s) if s else None

  @staticmethod
  def value_to_xml_string(x):
    return '' if x is None else repr(x)
