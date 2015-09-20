import os
import re
from browsergui import *

def n_leading_spaces(s):
  return len(re.match('^ *', s).group())

def strip_whitespace(s):
  s = s.strip('\n')
  n = min(n_leading_spaces(line) for line in s.split('\n') if line)
  return '\n'.join(line[n:] for line in s.split('\n'))

def exec_then_eval(to_exec, to_eval):
  # Due to some scoping subtlety, the locals and globals in
  # exec and eval should be the same, or we won't be able to
  # exec a program like
  #
  #   xs = []
  #   (lambda: xs)()
  #
  # I dunno. I just dunno.
  scope = globals().copy()
  if to_exec is not None:
    exec(to_exec, scope, scope)
  return eval(to_eval, scope, scope)

class Example(object):
  def __init__(self, show_code, prep_code=None):
    self.show_code = show_code
    self.prep_code = prep_code

  def to_grid_row(self):
    element = exec_then_eval(to_exec=self.prep_code, to_eval=self.show_code)
    code = self.show_code if self.prep_code is None else (self.prep_code + '\n\n' + self.show_code)
    return [CodeBlock(code), element]

def main():

  examples = {}

  def example_grid_for_types(*types):
    header_row = [EmphasizedText('Code'), EmphasizedText('Result')]
    rows = [examples[t].to_grid_row() for t in types]
    return Grid(cells=[header_row] + rows)

  examples[Text] = Example('Text("some plain text")')
  examples[Paragraph] = Example('Container(Paragraph("one"), Paragraph("two"))')
  examples[EmphasizedText] = Example('EmphasizedText("some bold text")')
  examples[CodeSnippet] = Example('CodeSnippet("some code")')
  examples[CodeBlock] = Example(r'CodeBlock("one\ntwo")')
  examples[Link] = Example('Link("google", url="http://google.com")')

  examples[Container] = Example('Container(Text("one"), CodeSnippet("two"))')
  examples[Viewport] = Example(strip_whitespace(r'''
    Viewport(
      CodeBlock('\n'.join(50*'viewport ' for _ in range(100))),
      width=400, height=200)'''))
  examples[List] = Example('List(items=[Text("one"), Text("two")])')
  examples[Grid] = Example(strip_whitespace('''
    Grid(cells=[
      [Text("00"), Text("01")],
      [Text("10"), Text("11")]])'''))

  examples[Image] = Example("Image(os.path.join(os.path.dirname(__file__), 'tour-image.png'))")

  examples[Button] = Example(
    'Container(click_count, button)',
    strip_whitespace('''
      click_count = Text('0')
      def button_clicked():
        n = int(click_count.text)
        click_count.text = str(n+1)
      button = Button('Click me!', callback=button_clicked)'''))

  examples[TextField] = Example(
    'Container(text_field, reversed_text_field_contents)',
    strip_whitespace('''
      reversed_text_field_contents = Text('')
      def text_field_changed():
        reversed_contents = ''.join(reversed(text_field.value))
        reversed_text_field_contents.text = reversed_contents
      text_field = TextField(change_callback=text_field_changed)
      text_field.value = "Reversed"'''))

  examples[Dropdown] = Example(
    'Container(dropdown, selected_dropdown_item)',
    strip_whitespace('''
      selected_dropdown_item = Text('')
      dropdown = Dropdown(
        ['Dr', 'op', 'do', 'wn'],
        change_callback=lambda: selected_dropdown_item.set_text(dropdown.value))
      dropdown.value = "wn"'''))

  examples[NumberField] = Example(
    'Container(number_field, number_field_squared)',
    strip_whitespace('''
      number_field_squared = Text('')
      def number_changed():
        if number_field.value is None:
          number_field_squared.text = ''
        else:
          number_field_squared.text = str(number_field.value ** 2)
      number_field = NumberField(change_callback=number_changed)
      number_field.value = 12'''))

  examples[ColorField] = Example(
    'Container(color_field, colored_text)',
    strip_whitespace('''
      colored_text = Text('colored')
      def color_changed():
        color = color_field.value
        color_hex = '#{:02x}{:02x}{:02x}'.format(*color)
        colored_text.set_styles(color=color_hex)
      color_field = ColorField(change_callback=color_changed)
      color_field.value = (0, 0, 255)'''))

  examples[DateField] = Example(
    'Container(date_field, weekday_text)',
    strip_whitespace('''
      weekday_text = Text('...')
      DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
              'Friday', 'Saturday', 'Sunday')
      def date_changed():
        if date_field.value is None:
          weekday_text.text = ''
        else:
          weekday_text.text = DAYS[date_field.value.weekday()]
      date_field = DateField(change_callback=date_changed)'''))


  run(GUI(
    Paragraph('''
      Here is a list of all the kinds of Element available to you.
      See the classes' documentation for more detailed information on them.'''),
    List(items=[
      Container(
        Paragraph('Text of many flavors:'),
        example_grid_for_types(Text, Paragraph, EmphasizedText, CodeSnippet, CodeBlock, Link)),
      Container(
        Paragraph('Input of many flavors:'),
        example_grid_for_types(Button, TextField, Dropdown, NumberField, ColorField, DateField)),
      Container(
        Paragraph('Structural elements of many flavors:'),
        example_grid_for_types(Container, Viewport, List, Grid)),
      Container(
        Paragraph('Other:'),
        example_grid_for_types(Image))]),
    title='browsergui tour'))

if __name__ == '__main__':
  main()
