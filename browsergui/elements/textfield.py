from .input_field import InputField

class TextField(InputField):
  def __init__(self, placeholder='', **kwargs):
    super(TextField, self).__init__(**kwargs)
    self.tag.setAttribute('type', 'text')

    self.placeholder = placeholder

  @property
  def placeholder(self):
    return self.tag.getAttribute('placeholder')
  @placeholder.setter
  def placeholder(self, placeholder):
    self.tag.setAttribute('placeholder', placeholder)
    self.mark_dirty()
