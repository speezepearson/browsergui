from browsergui import GUI, Button, Div
from browsergui.server import serve_forever

def iter_fibonacci_numbers():
  a, b = 1, 1
  while True:
    yield a
    a, b = b, a+b

fibs = iter_fibonacci_numbers()

gui = GUI()

button = Button(text="More!")
fibonacci_div = Div()

gui.body.append(button)
gui.body.append(fibonacci_div)

button.add_callback("click", (lambda event: fibonacci_div.append(Div(contents=str(next(fibs))))))

print('Starting server. Use <Ctrl-C> to stop.')
try:
  serve_forever(gui)
except KeyboardInterrupt:
  print("Keyboard interrupt received. Quitting.")
  gui.destroy()
