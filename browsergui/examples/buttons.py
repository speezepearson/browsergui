from browsergui import GUI, Button, Text, CodeSnippet, Container, run

gui = GUI(Text("What follows is the program that generates this page."))

for line in open(__file__[:-1] if __file__.endswith('.pyc') else __file__).readlines(): # Python 2's __file__ points to .pyc, not .py
  text = CodeSnippet("  "+line.strip("\n"))
  button = Button("Toggle line", callback=text.toggle_visibility)
  gui.append(Container(button, text))

def main():
  run(gui)

if __name__ == '__main__':
  main()