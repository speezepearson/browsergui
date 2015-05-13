Browser GUI
===========

Tools to design GUIs that run in a server, but are viewable in a browser.

This works by starting a server and pointing your browser at the server. Pretty much all the code execution happens on the server, and the browser is basically a [dumb terminal](http://en.wikipedia.org/wiki/Dumb_terminal), blindly evaluating whatever JavaScript the browser server gives it (which keeps the browser's view up to date with the state of the server's GUI object).


Should I use this?
------------------

### Executive Summary
I think this is a great way to make simple little GUIs that don't have any fancy stuff. If you want to build a very basic UI that (a) installs without trouble and (b) has a very shallow learning curve, I recommend this. If you want your UI to be pretty or extra-responsive, I do not recommend this.

Things that are prioritized in this package: portability, simplicity, and feeling-like-you're-writing-Python.

Things that are not prioritized in this package: performance and fine styling/layout control.

### Details

There are good things and bad things about this package.

The good:

- **Portability.** This package is pure Python that relies on only the standard library. This will not change while I have breath in my body.

  Consequently, it should be usable out of the box for every single person with Python 3, without installing Tk or Qt or wxWidgets or PyObjC or any of that stuff.

- **Easy to learn.** Making simple GUIs for simple tasks is simple. Check out the `examples` directory (particularly `examples/longrunning.py` for a vaguely realistic use case).

- **Code style.** It tries very hard to be Pythonic and object-oriented. It's not just a thin wrapper over HTML/JS.


The bad:

- **Performance.** It does not even try to be high-performance. There's an HTTP request every time the user interacts with the GUI, and an HTTP request every time the view needs updating. Performance is off the table. (Each request only takes several milliseconds' round trip for me, running on `localhost`, so it's not *awful*, but it's not awesome.)

- **(Transitive) Hackiness.** At the moment, it is not well-documented or well-tested, and it supports... basically just text and buttons. I will fix that (i.e. documenting, testing, and adding links/images/tables/(more input)) over the next month (i.e. by mid-June, 2015).

### Alternatives

I am aware of some GUI toolkits for Python that fill a similar niche. You should consider using these instead:

- `tkinter` (standard library)

  Advantages: it's in the standard library. It has always worked out of the box for me. If you want maximal portability, this is probably your best bet.

  Disadvantages: it feels like a wrapper around Tk, because it is. This gives good performance and detailed control, but writing it feels unintuitive (to me).

- [pyJS](http://pyjs.org), another Python package for making GUIs targeting browsers. It works by compiling your Python code into a slug of JavaScript which runs in the browser.

  Advantages: pyJS applications are much faster and much easier to deploy (since it doesn't require the user to run Python).

  Disadvantages: I had trouble installing it. And like `tkinter`, it's a wrapper, with the same dis/advantages.
