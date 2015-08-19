import os
from browsergui import *

click_count = 0
def main():
  def note_click():
    global click_count
    click_count += 1
    button.text = 'Button ({} clicks)'.format(click_count)
  button = Button('Button (0 clicks)', callback=note_click)

  reversed_text_field_contents = Text(''.join(reversed('Reversed')))
  def note_text_field_change():
    reversed_text_field_contents.text = ''.join(reversed(text_field.value))
  text_field = TextField(value='Reversed', change_callback=note_text_field_change)

  selected_dropdown_item = Text('')
  def note_dropdown_change():
    selected_dropdown_item.text = dropdown.value
  dropdown = Dropdown(['Dr', 'op', 'do', 'wn'], change_callback=note_dropdown_change)
  selected_dropdown_item.text = dropdown.value

  number_field_contents = Text('')
  def note_number_change():
    number_field_contents.text = '' if number_field.value is None else str(number_field.value**2)
  number_field = NumberField(change_callback=note_number_change)
  number_field.value = 12

  colored_text = Text('colored')
  def note_color_change():
    colored_text.set_styles(color=color_field.value_to_xml_string(color_field.value))
  color_field = ColorField(change_callback=note_color_change)
  color_field.value = (0, 0, 255)

  weekday_text = Text('...')
  def note_date_change():
    if date_field.value is None:
      weekday_text.text = '...'
    d = date_field.value.weekday()
    weekday_text.text = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][d]
  date_field = DateField(change_callback=note_date_change)

  elements = (
    Container(
      Text("Text of many flavors:"),
      List(items=(
        Text("plain"),
        CodeSnippet("code"),
        Container(Paragraph("paragraphs"), Paragraph("paragraphs"), Paragraph("paragraphs woohoo")),
        CodeBlock('code blocks\ncode blocks\ncode blocks woohoo'),
        Link("links", url="http://github.com/speezepearson/browsergui")))),
    Container(
      Text("Input of many flavors:"),
      List(items=(
        button,
        Container(Text('Text:'), text_field, reversed_text_field_contents),
        Container(Text('Dropdown:'), dropdown, Text(' Selected: '), selected_dropdown_item),
        Container(Text('Number:'), number_field, Text('x^2: '), number_field_contents),
        Container(Text('Color (on some browsers):'), color_field, colored_text),
        Container(Text('Date (on some browsers):'), date_field, Text(' is a '), weekday_text)))),
    Image(os.path.join(os.path.dirname(__file__), 'tour-image.png')),
    Viewport(Paragraph('viewport '*1000, styling={'width': 1000}), width=400, height=200),
    List(items=(Text("lists"), CodeSnippet("lists"), List(items=(Text("sublists"),)))),
    Grid([[None, Text('browsergui', styling={'font-weight':'600'}), Text('tkinter', styling={'font-weight':'600'})],
          [Text('has grids', styling={'font-weight':'600'}), Text('yes'), Text('yes')],
          [Text('made by me', styling={'font-weight':'600'}), Text('yes'), Text('no')]]))

  gui = GUI(Paragraph("Here are all the elements available to you:"), title="Browser GUI tour")
  gui.append(List(items=elements))

  run(gui)

if __name__ == '__main__':
  main()
