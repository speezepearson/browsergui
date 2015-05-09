from browsergui import GUI, Button, Text
from browsergui.server import serve_forever

def iter_fibonacci_numbers():
  a, b = 1, 1
  while True:
    yield a
    a, b = b, a+b

fibs = iter_fibonacci_numbers()

gui = GUI()

button = Button(text="More!")
gui.append(button)

button.set_callback(lambda event: gui.append(Text(str(next(fibs)))))

print('Starting server. Use <Ctrl-C> to stop.')
try:
  serve_forever(gui)
except KeyboardInterrupt:
  print("Keyboard interrupt received. Quitting.")
  gui.destroy()
