import datetime
from browsergui import *

now = Text("")

def update_now():
  now.text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
  RepeatingTimer(interval=0.1, callback=update_now, daemon=True).start()
  run(GUI(Text("The time is: "), now))

if __name__ == '__main__':
  main()