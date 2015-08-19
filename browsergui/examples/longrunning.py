import os
import threading
import collections
from browsergui import *

def find_extension(path):
  filename = os.path.basename(path)
  if not filename.startswith('.') and '.' in filename:
    extension = filename.rsplit('.', 1)[-1]
    if extension.isalnum():
      return extension.upper()
  return None

def file_paths():
  for root, dirs, files in os.walk("."):
    for entry in files:
      yield os.path.join(root, entry)

class ExtensionTallierGUI(GUI):
  def __init__(self):
    self.extension_counts = collections.defaultdict(int)
    self.current_file_text = CodeSnippet("")
    self.extension_counts_text = CodeBlock("")
    super(ExtensionTallierGUI, self).__init__(
      Paragraph("This will walk all files under the current directory and tally their extensions."),
      Paragraph("It might take a while. Feel free to close the window and come back later!"),
      Button(text="Start!", callback=self.tally),
      Container(Text("Currently visiting: "), self.current_file_text),
      Container(Text("Current extension counts:"), self.extension_counts_text))

  def tally(self):
    for path in file_paths():
      self.current_file_text.text = path
      extension = find_extension(path)
      self.extension_counts[extension] += 1
      self.extension_counts_text.text = "\n".join("{}: {}".format(k, v) for k, v in sorted(self.extension_counts.items(), key=(lambda kv: kv[1]), reverse=True))

def main():
  run(ExtensionTallierGUI(), quiet=True)

if __name__ == '__main__':
  main()