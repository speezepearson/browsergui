import os
import re
from browsergui import *

def n_leading_spaces(s):
  return len(re.match('^ *', s).group())

def strip_whitespace(s):
  s = s.strip('\n')
  n = min(n_leading_spaces(line) for line in s.split('\n') if line)
  return '\n'.join(line[n:] for line in s.split('\n'))

def main():

  example_codes = {}
  example_elements = {}

  def example_grid_for_types(*types):
    header_row = [EmphasizedText('Code'), EmphasizedText('Result')]
    rows = [[CodeBlock(example_codes[t]), example_elements[t]] for t in types]
    return Grid(cells=[header_row] + rows)

  example_codes[Text] = 'Text("some plain text")'
  example_elements[Text] = Text("some plain text")

  example_codes[Paragraph] = 'Paragraph("one"), Paragraph("two")'
  example_elements[Paragraph] = Container(Paragraph("one"), Paragraph("two"))

  example_codes[EmphasizedText] = 'EmphasizedText("some bold text")'
  example_elements[EmphasizedText] = EmphasizedText("some bold text")

  example_codes[CodeSnippet] = 'CodeSnippet("some code")'
  example_elements[CodeSnippet] = CodeSnippet("some code")

  example_codes[CodeBlock] = r'CodeBlock("one\ntwo")'
  example_elements[CodeBlock] = CodeBlock("one\ntwo")

  example_codes[Link] = 'Link("google", url="http://google.com")'
  example_elements[Link] = Link("google", url="http://google.com")

  example_codes[Container] = 'Container(Text("one"), CodeSnippet("two"))'
  example_elements[Container] = Container(Text("one"), CodeSnippet("two"))

  example_codes[Viewport] = strip_whitespace('''
    Viewport(
      CodeBlock('\\n'.join(50*'viewport ' for _ in range(100))),
      width=400, height=200)''')
  example_elements[Viewport] = Viewport(
    CodeBlock('\n'.join(50*'viewport ' for _ in range(100))),
    width=400, height=200)

  example_codes[List] = 'List(items=[Text("one"), Text("two")])'
  example_elements[List] = List(items=[Text("one"), Text("two")])

  example_codes[Grid] = strip_whitespace('''
    Grid(cells=[
      [Text("00"), Text("01")],
      [Text("10"), Text("11")]])''')
  example_elements[Grid] =  Grid(cells=[
    [Text("00"), Text("01")],
    [Text("10"), Text("11")]])

  example_codes[Image] = "Image(path)"
  example_elements[Image] = Image(os.path.join(os.path.dirname(__file__), 'tour-image.png'))

  example_codes[Button] = strip_whitespace('''
    click_count = Text('0')
    def button_clicked():
      n = int(click_count.text)
      click_count.text = str(n+1)
    button = Button('Click me!', callback=button_clicked''')
  click_count = Text('0')
  def button_clicked():
    n = int(click_count.text)
    click_count.text = str(n+1)
  button = Button('Click me!', callback=button_clicked)
  example_elements[Button] = Container(click_count, button)

  example_codes[TextField] = strip_whitespace('''
    reversed_text_field_contents = Text('')
    def text_field_changed():
      reversed_contents = ''.join(reversed(text_field.value))
      reversed_text_field_contents.text = reversed_contents
    text_field = TextField(change_callback=text_field_changed)
    text_field.value = 'reversed' ''')
  reversed_text_field_contents = Text('')
  def text_field_changed():
    reversed_contents = ''.join(reversed(text_field.value))
    reversed_text_field_contents.text = reversed_contents
  text_field = TextField(change_callback=text_field_changed)
  text_field.value = 'reversed'
  example_elements[TextField] = Container(text_field, reversed_text_field_contents)

  example_codes[Dropdown] = strip_whitespace('''
    selected_dropdown_item = Text('')
    dropdown = Dropdown(
      ['Dr', 'op', 'do', 'wn'],
      change_callback=lambda: selected_dropdown_item.set_text(dropdown.value))
    dropdown.value = "wn"''')
  selected_dropdown_item = Text('')
  dropdown = Dropdown(
    ['Dr', 'op', 'do', 'wn'],
    change_callback=lambda: selected_dropdown_item.set_text(dropdown.value))
  dropdown.value = "wn"
  example_elements[Dropdown] = Container(dropdown, selected_dropdown_item)

  example_codes[NumberField] = strip_whitespace('''
    number_field_squared = Text('')
    def number_changed():
      if number_field.value is None:
        number_field_squared.text = ''
      else:
        number_field_squared.text = str(number_field.value ** 2)
    number_field = NumberField(change_callback=number_changed)
    number_field.value = 12''')
  number_field_squared = Text('')
  def number_changed():
    if number_field.value is None:
      number_field_squared.text = ''
    else:
      number_field_squared.text = str(number_field.value ** 2)
  number_field = NumberField(change_callback=number_changed)
  number_field.value = 12
  example_elements[NumberField] = Container(number_field, number_field_squared)

  example_codes[ColorField] = strip_whitespace('''
    colored_text = Text('colored')
    def color_changed():
      color = color_field.value
      color_hex = '#{:02x}{:02x}{:02x}'.format(*color)
      colored_text.set_styles(color=color_hex)
    color_field = ColorField(change_callback=color_changed)
    color_field.value = (0, 0, 255)''')
  colored_text = Text('colored')
  def color_changed():
    color = color_field.value
    color_hex = '#{:02x}{:02x}{:02x}'.format(*color)
    colored_text.set_styles(color=color_hex)
  color_field = ColorField(change_callback=color_changed)
  color_field.value = (0, 0, 255)
  example_elements[ColorField] = Container(color_field, colored_text)

  example_codes[DateField] = strip_whitespace('''
    weekday_text = Text('...')
    DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday')
    def date_changed():
      if date_field.value is None:
        weekday_text.text = ''
      else:
        weekday_text.text = DAYS[date_field.value.weekday()]
    date_field = DateField(change_callback=date_changed)''')
  weekday_text = Text('...')
  DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
          'Friday', 'Saturday', 'Sunday')
  def date_changed():
    if date_field.value is None:
      weekday_text.text = ''
    else:
      weekday_text.text = DAYS[date_field.value.weekday()]
  date_field = DateField(change_callback=date_changed)
  example_elements[DateField] = Container(date_field, weekday_text)


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
