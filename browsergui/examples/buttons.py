from browsergui import GUI, Button, Text, CodeSnippet, Container, run

gui = GUI(Text("What follows is the program that generates this page."))

for line in open(__file__).readlines():
  text = CodeSnippet("  "+line.strip("\n"))
  button = Button("Toggle line", callback=text.toggle_visibility)
  gui.append(Container(button, text))

def main():
  run(gui)

if __name__ == '__main__':
  main()