from browsergui import GUI, Button, Text, Container
from browsergui.server import serve_forever

gui = GUI()

gui.append(Text("""
  What follows is the program that generates this page.
  This GUI works by starting a server that serves up a very simple web page.
  The web page tells the browser, "Execute whatever JavaScript I give you."
  This allows the server to modify the browser's DOM essentially at will,
  and by using that JS to attach callbacks to elements in the browser,
  the server can arrange to be notified when the user interacts with the GUI.
  You can close the page and come back to it later if you want!
"""))

toggler = lambda element: lambda event: element.toggle_visibility()
for line in open(__file__).readlines():
  text = Text("  "+line.strip("\n"), code=True)
  button = Button("Toggle line", callback=toggler(text))
  gui.append(Container(button, text, inline=False))

print('Starting server. Use <Ctrl-C> to stop.')
try:
  serve_forever(gui)
except KeyboardInterrupt:
  print("Keyboard interrupt received. Quitting.")
  gui.destroy()
