import argparse
import os
import browsergui.examples

parser = argparse.ArgumentParser()
parser.add_argument('examplename', nargs='?', choices=list(browsergui.examples.EXAMPLES.keys()), default='tour',
                    help='name of example to run (default: tour)')

def main():
  args = parser.parse_args()

  browsergui.examples.EXAMPLES[args.examplename].main()

if __name__ == '__main__':
  main()