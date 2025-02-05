What is this?
-------------
It's a GUI framework prioritizing portability, simplicity, and a Pythonic feel. The two facts I think will best hook you:
- Simple GUIs are simple to make: `GUI(Text("Hello world!")).run()`.
- You could type `easy_install browsergui && python -m browsergui.examples` *this instant*, and it would work. (Well, maybe you need to `sudo`.) There's no complex application framework you need to install first.

  (Corollary: if you build a GUI using this package, your co-developers/users also won't need to install anything complicated.)

If you want to build a simple GUI for a simple task, this is a great library. [Here's a mock-up][demo] that shows all the stuff you can do with it.

If you want to build a video game, or a nice, fluid 3D visualization, this is easily the worst GUI framework I have ever seen.

- [Why is it good?](#why-is-it-good)
- [Why is it bad?](#why-is-it-bad)
- [What are the alternatives?](#what-are-the-alternatives)
- [How do I install it?](#how-do-i-install-it)
- [How do I learn to use it?](#how-do-i-learn-to-use-it)


Why is it good?
---------------

This package prioritizes ease of use, portability, and good documentation above all else. The following statements will remain true:

- **It feels like Python.** It uses HTML/CSS/JS under the hood, but that fact is carefully hidden under nice object-oriented abstractions. Contrast with [Tkinter][tkinter], which feels like Tk, because it is.
- **It has a shallow learning curve.** "Hello World" is `GUI(Text("Hello world!")).run()`. Minesweeper, including the game logic, is [less than 100 lines of code][minesweeper-code] and [looks like this][minesweeper-screenshot].
- **It's super-portable.** `pip install browsergui && python -m browsergui.examples` has worked, with no snags, on every system I've tried (OS X, Debian, and Ubuntu, with both Python 2.7 and a few Python 3.Xs). Seriously, you could run that right now and it would work, without a single abstruse error message about your Qt/wx/PyObjC installation. At the risk of tooting my own horn, I've never seen another GUI library so easy to install.
- **It's well-documented.** There's a [wiki][wiki] to teach you how to use it. There are [examples](#how-do-I-learn-to-use-it). There's a [reference manual][docs]. There's a [runnable demo for every predefined kind of element][demo]. I've spent more time documenting than I've spent writing actual code.

Why is it bad?
--------------

- **It's slow.** It does not even try to be high-performance. There's an HTTP request every time the user interacts with the GUI, and again every time the view is updated. Performance is off the table. (It's not *frustratingly* slow -- you can drag a slider and see the value update with no perceptible delay -- but it's not good for fancy stuff.)
- **It's not super-easy to make super-pretty things.** I just haven't prioritized styling: any styling you want to do, you have to do through CSS. I'm not sure `element.css['color'] = 'red'` is so much worse than `widget.config(foreground="#f00")`, but it *does* feel like a thin wrapper over CSS (because it is), which is gross.
- **Its input-handling is limited.** Full-powered GUI libraries let you capture every mouse movement, every keypress, anything you can dream. That might come to Browsergui eventually, but for now, you're pretty much limited to predefined input fields.
- **It doesn't provide utility functions.** Every other GUI framework I can recall seeing provides things like timers: things that are *nice* to have when you're making a GUI, but aren't directly related to user-interaction. This package doesn't offer those and probably never will. If you want timers, get them from a different package.

What are the alternatives?
--------------------------

I am aware of some GUI toolkits for Python that fill a similar niche. You should consider using these instead:

- [RemI][remi], which has exactly the same idea (build a GUI in Python, run it in a browser). Definitely worth a look.

  Advantages: (at the time of writing) has more features, e.g. file-input dialogs. Looks significantly prettier.

  Disadvantages: (at the time of writing) less thorough tutorials/documentation. Simple apps are more verbose.

- [tkinter][tkinter] (standard library)

  Advantages: it's well-known. Lots of people have written tutorials and documentation for it.

  Disadvantages: it feels like a wrapper around Tk, because it is. This gives good performance and detailed control, but writing it feels unintuitive (to me). Also, I've had trouble getting it to work with multiple Python installations.

- [pyJS][pyjs], another Python package for making GUIs targeting browsers. It works by compiling your Python code into a slug of JavaScript which runs in the browser.

  Advantages: pyJS applications are much faster and much easier to deploy (since it doesn't require the user to run Python).

  Disadvantages: I had trouble installing it. And like `tkinter`, it's a wrapper, with the same dis/advantages.

- [flexx][flexx], which (if I understand correctly) compiles a Python app to JavaScript. I haven't investigated it very much.

There are, of course, many other GUI toolkits. [Here][official-alternatives] is a list of those popular enough to earn the notice of Official Python People. [Here][unofficial-alternatives] is a paralytically long listing of less-notable ones.

How do I install it?
--------------------

If you use pip, `pip install browsergui`.

If you use easy_install, `easy_install browsergui`.

If you don't like package managers, just unzip [this][download-zip] and put the `browsergui` folder anywhere on your Python path.

Once it's installed, I recommend running `python -m browsergui.examples` to see a catalog of all the kinds of building blocks available to you, or checking out [the wiki][wiki] for tutorial-type stuff.


How do I learn to use it?
-------------------------

[The wiki][wiki] has several tutorial-type pages. Or you could just extrapolate from these examples:

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

        now = Text("")

        def update_now_forever():
          while True:
            now.text = time.strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(1)

        t = threading.Thread(target=update_now_forever)
        t.daemon = True
        t.start()

        GUI(Text("The time is: "), now).run()

(You can close/reopen the browser window at any time; Ctrl-C will stop the server.)

Each kind of element (`Text`, `Button`, `ColorField`, `Grid`...) also has a simple example showing you how to use it: `python -m browsergui.examples` will display all those examples to you.

[remi]: https://github.com/dddomodossola/remi
[flexx]: https://github.com/zoofIO/flexx
[demo]: http://speezepearson.github.io/misc/fake-browsergui-demo.html
[minesweeper-code]: https://github.com/speezepearson/browsergui/blob/master/browsergui/examples/minesweeper.py
[minesweeper-screenshot]: http://i.imgur.com/8Ax04sZ.png
[download-zip]: https://github.com/speezepearson/browsergui/archive/master.zip
[wiki]: https://github.com/speezepearson/browsergui/wiki
[docs]: http://pythonhosted.org/browsergui
[download-zip]: https://github.com/speezepearson/browsergui/archive/master.zip
[tkinter]: https://docs.python.org/3/library/tkinter.html#module-tkinter
[pyjs]: http://pyjs.org
[official-alternatives]: http://docs.python.org/2/library/othergui.html
[unofficial-alternatives]: http://wiki.python.org/moin/GuiProgramming
