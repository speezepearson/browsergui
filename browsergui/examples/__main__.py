import argparse
import os
import browsergui.examples

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--example', choices=list(browsergui.examples.EXAMPLES.keys()), default='tour')

def main():
  args = parser.parse_args()

  browsergui.examples.EXAMPLES[args.example].main()

if __name__ == '__main__':
  main()