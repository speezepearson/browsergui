from .input_field import InputField

class TextField(InputField):
  def __init__(self, **kwargs):
    super(TextField, self).__init__(**kwargs)
    self.tag.setAttribute('type', 'text')
