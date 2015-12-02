Browser GUI
===========

Tools to design GUIs viewable in a browser.

Everybody has a browser, and a lot of very smart people have designed browsers so that it's easy to make pretty, interactive pages. Wouldn't it be great if we could take advantage of this in Python? Well, now we can!

Ways to install:
- `pip install browsergui`
- `easy_install browsergui`
- download this directory, through either
  - unzipping [this](https://github.com/speezepearson/browsergui/archive/master.zip), or
  - `git clone git@github.com:speezepearson/browsergui.git`

  and then install it with either
  - `python setup.py install`, or
  - plop the `browsergui` subfolder anywhere on your Python path

Once it's installed, I recommend running `python -m browsergui.examples` to see a catalog of all the kinds of building blocks available to you, then running `python -m browsergui.examples interactive` to experiment on your own. See [the wiki][wiki] for help learning about this package.

[wiki]: https://github.com/speezepearson/browsergui/wiki

Examples
--------

Here are a few short demos, to give you a taste of what this GUI framework looks like. (You can close/reopen the browser window at any time; Ctrl-C will stop the server.)

- Hello world:

        from browsergui import GUI, Text
        GUI(Text("Hello world!")).run()

- A number that increments every time you press a button:

        from browsergui import GUI, Text, Button

        button = Button('0')
        @button.def_callback
        def increment():
          button.text = str(int(button.text)+1)

        GUI(button).run()

- A clock:

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

### Alternatives

I am aware of some GUI toolkits for Python that fill a similar niche. You should consider using these instead:

- [tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter) (standard library)

  Advantages: it's in the standard library. It has always worked out of the box for me. If you want maximal portability, this is probably your best bet.

  Disadvantages: it feels like a wrapper around Tk, because it is. This gives good performance and detailed control, but writing it feels unintuitive (to me).

- [pyJS](http://pyjs.org), another Python package for making GUIs targeting browsers. It works by compiling your Python code into a slug of JavaScript which runs in the browser.

  Advantages: pyJS applications are much faster and much easier to deploy (since it doesn't require the user to run Python).

  Disadvantages: I had trouble installing it. And like `tkinter`, it's a wrapper, with the same dis/advantages.
