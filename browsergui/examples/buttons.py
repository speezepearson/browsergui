from browsergui import GUI, Button, Text, CodeSnippet, Container, run

gui = GUI()

gui.append(Text("What follows is the program that generates this page."))

for line in open(__file__).readlines():
  text = CodeSnippet("  "+line.strip("\n"))
  button = Button("Toggle line", callback=text.toggle_visibility)
  gui.append(Container(button, text))

run(gui)
