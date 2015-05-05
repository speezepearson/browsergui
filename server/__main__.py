from browsergui.gui import GUI, Element
from browsergui.server import serve_forever

def iter_fibonacci_numbers():
  a, b = 1, 1
  while True:
    yield a
    a, b = b, a+b

fibs = iter_fibonacci_numbers()

gui = GUI()

button = gui.body.add_child(tag="button", contents="More!")
fibonacci_div = gui.body.add_child(tag="div")

button.add_callback("click", (lambda event: fibonacci_div.add_child(tag="div", contents=str(next(fibs)))))

print('Starting server. Use <Ctrl-C> to stop.')
try:
  serve_forever(gui)
except KeyboardInterrupt:
  print("Keyboard interrupt received. Quitting.")
  gui.destroy()
