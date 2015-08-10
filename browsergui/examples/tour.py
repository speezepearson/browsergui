import os
from browsergui import *

click_counter = 0
def note_click():
  global click_counter
  click_counter += 1
  button.text = 'Button ({} clicks)'.format(click_counter)
button = Button('Button (0 clicks)', callback=note_click)

big_thing = Paragraph('viewport '*1000)
big_thing.set_styles(width=1000)
viewport = Viewport(big_thing, width=400, height=200)

elements = (
  Text("Plain text."),
  CodeSnippet("Inline code."),
  Paragraph("A paragraph of text."),
  CodeBlock("A block of code."),
  button,
  Link("A link.", url="http://google.com"),
  Image(os.path.join(os.path.dirname(__file__), 'tour-image.png')),
  viewport,
  List(items=(Text("lists"), CodeSnippet("lists"), List(items=(Text("sublists"),)))))

gui = GUI(Paragraph("Here are all the elements available to you:"), title="Browser GUI tour")
for element in elements:
  container = Container(element)
  container.set_styles(**{'margin': '1em', 'border': '1px solid black'})
  gui.append(container)

def main():
  run(gui)

if __name__ == '__main__':
  main()
