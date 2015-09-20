import os
from browsergui import *

click_count = 0
def main():
  click_count = Text('0')
  button = Button('Click me!', callback=lambda: click_count.set_text(int(click_count.text) + 1))

  reversed_text_field_contents = Text('')
  text_field = TextField(change_callback=lambda: reversed_text_field_contents.set_text(''.join(reversed(text_field.value))))
  text_field.value = 'Reversed'

  selected_dropdown_item = Text('')
  dropdown = Dropdown(['Dr', 'op', 'do', 'wn'], change_callback=lambda: selected_dropdown_item.set_text(dropdown.value))
  dropdown.value = 'Dr'

  number_field_squared = Text('')
  number_field = NumberField(change_callback=lambda: number_field_squared.set_text('' if number_field.value is None else str(number_field.value**2)))
  number_field.value = 12

  colored_text = Text('colored')
  color_field = ColorField(change_callback=lambda: colored_text.set_styles(color=color_field.value_to_xml_string(color_field.value)))
  color_field.value = (0, 0, 255)

  weekday_text = Text('...')
  DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
  date_field = DateField(change_callback=lambda: weekday_text.set_text('' if date_field.value is None else DAYS[date_field.value.weekday()]))

  elements = (
    Container(
      Text("Text of many flavors:"),
      List(items=(
        Text("plain"),
        EmphasizedText("emphasized"),
        CodeSnippet("code"),
        Container(Paragraph("paragraphs"), Paragraph("paragraphs"), Paragraph("paragraphs woohoo")),
        CodeBlock('code blocks\ncode blocks\ncode blocks woohoo'),
        Link("links", url="http://github.com/speezepearson/browsergui")))),
    Container(
      Text("Input of many flavors:"),
      List(items=(
        Container(Text('Button: '), button, Text(' Clicks: '), click_count),
        Container(Text('Text:'), text_field, reversed_text_field_contents),
        Container(Text('Dropdown:'), dropdown, Text(' Selected: '), selected_dropdown_item),
        Container(Text('Number:'), number_field, Text('x^2: '), number_field_squared),
        Container(Text('Color (on some browsers):'), color_field, colored_text),
        Container(Text('Date (on some browsers):'), date_field, Text(' is a '), weekday_text)))),
    Container(
      Text("Structural elements of many flavors:"),
      List(items=(
        Viewport(CodeBlock('\n'.join(50*'viewport ' for _ in range(100))), width=400, height=200),
        List(items=(
          Text("bulleted"),
          Text("lists"),
          List(numbered=True, items=[
            Text("numbered"),
            Text("lists")]))),
        Grid([[None, EmphasizedText('browsergui'), EmphasizedText('tkinter')],
              [EmphasizedText('has grids'), Text('yes'), Text('yes')],
              [EmphasizedText('made by me'), Text('yes'), Text('no')]]))
        )),
    Image(os.path.join(os.path.dirname(__file__), 'tour-image.png')))

  gui = GUI(Paragraph("Here are all the elements available to you:"), title="Browser GUI tour")
  gui.append(List(items=elements))

  run(gui)

if __name__ == '__main__':
  main()
