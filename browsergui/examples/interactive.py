import code
import browsergui
import threading
from browsergui import GUI, Paragraph, CodeBlock, Paragraph

def run_repl(gui):
  interpreter = code.InteractiveConsole(locals={'_gui': gui})
  interpreter.runsource('from browsergui import *')
  interpreter.runsource('gui = _gui')
  interpreter.interact(
    banner="""
      Here's an interpreter! You have access to everything in the `browsergui`
      namespace, plus a ready-made GUI named `gui`.
      
      The server startup might print a couple things on top of the prompt -
      don't worry, you're still in the interpreter.
      
      Exiting the interpreter will terminate the program.
    """)

def main():
  gui = GUI(Paragraph("""
    Run commands in the REPL.
    As you change `gui`, this page will update.
    Some commands you might run are:
  """))

  for sample in ("gui.body.append(Text('Hiiii!'))",
                 "gui.body.append(Button(callback=(lambda: gui.body.append(Paragraph('Clicked!')))))"):
    gui.body.append(CodeBlock(sample))

  t = threading.Thread(target=gui.run, kwargs={'quiet': True})
  t.daemon = True
  t.start()
  run_repl(gui)

  if gui.running: # If the user killed the GUI in the REPL, it might not still be running.
    gui.stop_running()


if __name__ == '__main__':
  main()