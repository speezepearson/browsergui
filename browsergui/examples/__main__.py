import argparse
import os

here = os.path.abspath(os.path.dirname(__file__))

example_filenames = {f[:-3]: f for f in os.listdir(here) if f.endswith('.py') and not f.startswith('_')}

parser = argparse.ArgumentParser()
parser.add_argument('example', choices=list(example_filenames.keys()))

def main():
  args = parser.parse_args()

  with open(os.path.join(here, example_filenames[args.example])) as f:
    exec(f.read())

if __name__ == '__main__':
  main()