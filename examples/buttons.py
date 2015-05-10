from browsergui import GUI, Button, Text, Container, run

gui = GUI()

gui.append(Text("What follows is the program that generates this page."))

def toggler(element):
  def callback(event):
    element.toggle_visibility()
  return callback

for line in open(__file__).readlines():
  text = Text("  "+line.strip("\n"), code=True)
  button = Button("Toggle line", callback=toggler(text))
  gui.append(Container(button, text, inline=False))

run(gui)
