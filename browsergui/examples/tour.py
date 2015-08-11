import os
from browsergui import *

click_counter = 0
def note_click():
  global click_counter
  click_counter += 1
  button.text = 'Button ({} clicks)'.format(click_counter)
button = Button('Button (0 clicks)', callback=note_click)

elements = (
  Text("Plain text."),
  CodeSnippet("Inline code."),
  Paragraph("A paragraph of text."),
  CodeBlock("A block of code."),
  button,
  Link("A link.", url="http://google.com"),
  Image(os.path.join(os.path.dirname(__file__), 'tour-image.png')),
  Viewport(Paragraph('viewport '*1000, styling={'width': 1000}), width=400, height=200),
  List(items=(Text("lists"), CodeSnippet("lists"), List(items=(Text("sublists"),)))))

gui = GUI(Paragraph("Here are all the elements available to you:"), title="Browser GUI tour")
for element in elements:
  gui.append(Container(element, styling={'margin': '1em', 'border': '1px solid black'}))

def main():
  run(gui)

if __name__ == '__main__':
  main()
