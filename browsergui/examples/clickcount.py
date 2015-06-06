from browsergui import run, GUI, Text, Button

n_clicks = 0
text = Text("0")

def increment():
  global n_clicks
  n_clicks += 1
  text.text = str(n_clicks)

def main():
  run(GUI(text, Button(callback=increment)))

if __name__ == '__main__':
  main()