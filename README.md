Browser GUI
===========

Tools to design GUIs that run in a server, but are viewable in a browser.

This works by starting a server and pointing your browser at the server. Pretty much all the code execution happens on the server, and the browser is basically a [dumb terminal](http://en.wikipedia.org/wiki/Dumb_terminal), blindly evaluating whatever JavaScript the browser server gives it (which keeps the browser's view up to date with the state of the server's GUI object).


Pros and Cons
=============

Good things about this package:

- It requires only the standard library and a modernish browser. This will not change while I have breath in my body.
- Consequently, it should be usable by anybody with Python 3, without installing Tk or Qt or wxWidgets or PyObjC or any of that stuff.
- It tries very hard to be Pythonic and object-oriented. (i.e. It's not just a thin wrapper over HTML/JS.)
- The GUI lives in the Python process: you can close the browser window and come back any time for a long-running background job.
- Making simple GUIs for simple tasks is simple. Check out the `examples` directory (particularly `examples/longrunning.py` for a vaguely realistic use case).


Bad things about this package:

- It does not even try to be high-performance. There's an HTTP request every time anything interesting happens: performance is off the table. (Each request only takes several milliseconds round trip for me, running on `localhost`, so it's not *awful*, but it's not awesome.)


So should I use this?
---------------------
I think this is a great way to make simple little GUIs that don't have any fancy stuff. If you find yourself thinking, "I wish my program could have a slightly richer interface than I can achieve with a terminal without learning ncurses," you should consider this library.

If you want to make a little game that draws on the screen at 30fps, I recommend absolutely anything else.


Alternatives
------------

I am aware of some GUI toolkits for Python that fill a similar niche. You should consider using these instead:

- `tkinter` (standard library)

  Advantages: it's in the standard library. It has always worked out of the box for me. If you want maximal portability, this is probably your best bet.

  Disadvantages: it feels like a wrapper around Tk, because it is. This gives performance and detailed control, but writing it feels unintuitive (to me).

- [pyJS](http://pyjs.org), another Python package for making GUIs targeting browsers. It works by compiling your Python code into a slug of JavaScript which runs in the browser.

  Advantages: pyJS applications are much faster and much easier to deploy (since it doesn't require the user to run Python).

  Disadvantages: I had trouble installing it. And like `tkinter`, it's a wrapper, with the same dis/advantages.
