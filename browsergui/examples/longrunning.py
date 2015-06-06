import os
import threading
import collections
from browsergui import GUI, Paragraph, Text, Button, CodeSnippet, CodeBlock, Container, run, call_in_background

extension_counts = collections.defaultdict(int)
current_file_text = CodeSnippet("")
extension_counts_text = CodeBlock("")

def file_paths():
  for root, dirs, files in os.walk("."):
    for entry in files:
      yield os.path.join(root, entry)

def find_extension(filename):
  if not filename.startswith('.') and '.' in filename:
    extension = filename.rsplit('.', 1)[-1]
    if extension.isalnum():
      return extension.upper()
  return None

def tally_extensions():
  for root, dirs, files in os.walk("."):
    for entry in files:
      path = os.path.join(root, entry)
      current_file_text.text = path
      extension = find_extension(entry)
      extension_counts[extension] += 1
      extension_counts_text.text = "\n".join("{}: {}".format(k, v) for k, v in sorted(extension_counts.items(), key=(lambda kv: kv[1]), reverse=True))


def main():
  run(
    GUI(
      Paragraph("This will walk all files under the current directory and tally their extensions."),
      Paragraph("It might take a while. Feel free to close the window and come back later!"),
      Button(text="Start!", callback=lambda: call_in_background(tally_extensions, daemon=True)),
      Container(Text("Currently visiting: "), current_file_text),
      Container(Text("Current extension counts:"), extension_counts_text)),
    quiet=True)

if __name__ == '__main__':
  main()