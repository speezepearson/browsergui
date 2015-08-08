Browser GUI
===========

Tools to design GUIs viewable in a browser.

Everybody has a browser, and a lot of very smart people have designed browsers so that it's easy to make pretty, interactive pages. Wouldn't it be great if we could take advantage of this in Python? Well, now we can!

Install with `pip install browsergui`, or download it and either run `python setup.py install` or plop the `browsergui` subfolder anywhere on your Python path. Once you've done that, you can run various demos with `python -m browsergui.examples [--help] [-e ...]`.


Examples
--------

Here are a few short demos, to give you a taste of what this GUI framework looks like.

- Hello world:

        from browsergui import run, GUI, Text
        run(GUI(Text("Hello world!")))

- A number that increments every time you press a button:

        from browsergui import run, GUI, Text, Button

        n_clicks = 0
        text = Text("0")

        def increment():
          global n_clicks
          n_clicks += 1
          text.text = str(n_clicks)

        run(GUI(text, Button(callback=increment)))

- A clock:

        import datetime
        from browsergui import *

        now = Text("")

        def update_now():
          now.text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        RepeatingTimer(interval=0.1, callback=update_now, daemon=True).start()

        run(GUI(Text("The time is: "), now))


Should I use this?
------------------

### Summary

Things that are prioritized in this package: easy installation, simplicity, and the feeling that you're writing Python.

Things that are not prioritized in this package: performance and fine styling/layout control.

I think this is a great way to make simple little GUIs that don't have any fancy stuff. If you want to build a very basic UI that (a) installs without trouble and (b) has a very shallow learning curve, I recommend this. If you want your UI to be pretty or extra-responsive, I do not recommend this.

### Details

There are good things and bad things about this package.

The good:

- **Easy installation.** This package is pure Python that relies on only the standard library. This will not change while I have breath in my body.

  Consequently, it should be usable out of the box for every single person with Python 2.7 or later, without installing Tk or Qt or wxWidgets or PyObjC or any of that stuff.

- **Easy to learn.** Making simple GUIs for simple tasks is simple. Check out the `examples` directory (particularly `examples/longrunning.py` for a vaguely realistic use case).

- **Code style.** It tries very hard to be Pythonic and object-oriented. It's not just a thin wrapper over HTML/JS.


The bad:

- **Performance.** It does not even try to be high-performance. There's an HTTP request every time the user interacts with the GUI, and an HTTP request every time the view needs updating. Performance is off the table. (Each request only takes several milliseconds' round trip for me, running on `localhost`, so it's not *awful*, but it's not awesome.)

- **(Transitive) Hackiness.** At the moment, it is not well-tested, and it supports... basically just text and buttons. I will fix that (i.e. testing, and adding links/images/tables/(more input)) over the next month (i.e. by mid-June, 2015).

### Alternatives

I am aware of some GUI toolkits for Python that fill a similar niche. You should consider using these instead:

- `tkinter` (standard library)

  Advantages: it's in the standard library. It has always worked out of the box for me. If you want maximal portability, this is probably your best bet.

  Disadvantages: it feels like a wrapper around Tk, because it is. This gives good performance and detailed control, but writing it feels unintuitive (to me).

- [pyJS](http://pyjs.org), another Python package for making GUIs targeting browsers. It works by compiling your Python code into a slug of JavaScript which runs in the browser.

  Advantages: pyJS applications are much faster and much easier to deploy (since it doesn't require the user to run Python).

  Disadvantages: I had trouble installing it. And like `tkinter`, it's a wrapper, with the same dis/advantages.

How it Works
------------

Basically, we just start a server and point the browser at the server. All the fancy computation happens on the server: the browser is basically a [dumb terminal](http://en.wikipedia.org/wiki/Dumb_terminal), which (a) notifies the server when the user does something and (b) blindly executes whatever JavaScript the server gives it, thereby keeping the view up-to-date.
