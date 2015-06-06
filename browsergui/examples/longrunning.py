import os
import threading
import collections
from browsergui import GUI, Paragraph, Text, CodeSnippet, CodeBlock, Container, run

def file_paths():
  for root, dirs, files in os.walk("."):
    for entry in files:
      yield os.path.join(root, entry)

def run_in_background(function):
  threading.Thread(target=function).start()


def main():
  extension_counts = collections.defaultdict(int)
  current_file_text = CodeSnippet("")
  extension_counts_text = CodeBlock("")

  def background_task():
    import time; time.sleep(5)
    for root, dirs, files in os.walk("."):
      for entry in files:
        path = os.path.join(root, entry)
        current_file_text.text = path
        if '.' in entry and not entry.startswith('.'):
          extension = entry.rsplit('.', 1)[-1]
          if not extension.isalpha():
            continue
          extension_counts[extension.upper()] += 1
          extension_counts_text.text = "\n".join("{}: {}".format(k, v) for k, v in extension_counts.items())

  run_in_background(background_task)

  run(
    GUI(
      Paragraph("This might take a while. Feel free to close the window and come back later."),
      Container(Text("Currently visiting: "), current_file_text),
      Container(Text("Current extension counts:"), extension_counts_text)),
    quiet=True)

if __name__ == '__main__':
  main()