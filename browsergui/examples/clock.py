import time
import threading
from browsergui import Text, GUI

def main():
  now = Text("")

  def update_now_forever():
    while True:
      now.text = time.strftime("%Y-%m-%d %H:%M:%S")
      time.sleep(1)

  t = threading.Thread(target=update_now_forever)
  t.daemon = True
  t.start()

  GUI(Text("The time is: "), now).run()

if __name__ == '__main__':
  main()