import code
import threading
import browsergui
from browsergui import GUI, Paragraph, CodeBlock, Paragraph, run

def main():
  gui = GUI()
  gui.append(Paragraph("""
    Run commands in the REPL.
    As you change `gui`, this page will update.
    Some commands you might run are:
  """))

  for sample in ("gui.append(Text('Hiiii!'))",
                 "gui.append(Button(callback=(lambda: gui.append(Paragraph('Clicked!')))))"):
    gui.append(CodeBlock(sample))

  gui.append(Paragraph("The code for this page is:"))
  gui.append(CodeBlock(open(__file__).read()))

  t = threading.Thread(target=run, args=(gui,), kwargs=dict(quiet=True))
  t.daemon = True
  t.start()

  repl_locals = vars(browsergui).copy()
  repl_locals.update(gui=gui)
  code.interact(
    banner="""
      Here's an interpreter! You have access to everything in the `browsergui`
      namespace, plus a ready-made GUI named `gui`.
      
      The server startup might print a couple things on top of the prompt -
      don't worry, you're still in the interpreter.
      
      Exiting the interpreter will terminate the program.
    """,
    local=repl_locals)
  gui.destroy()

if __name__ == '__main__':
  main()