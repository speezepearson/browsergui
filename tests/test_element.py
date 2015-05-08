class ElementTest(unittest.TestCase):
  def assertEqual(self, x, y, hashes_too=False):
    self.assertEqual(x, y)
    if hashes_too:
      self.assertEqual(hash(x), hash(y))

  def test_construction(self):

    e = Element(tag_name="span")
    self.assertEqual("span", e.tag_name)

    e = Element(html="<div>foo</div>")
    self.assertEqual("div", e.tag_name)

    container = Element(tag_name="a", children=[e])

    with self.assertRaises(something):
      Element(html="raw string")
    with self.assertRaises(something):
      Element(html="<malformed")
    with self.assertRaises(something):
      Element(html="<malformed>")
    with self.assertRaises(something):
      Element(html="<mal></formed>")
    with self.assertRaises(something):
      Element(html="<two /><tags />")

  def test_equality(self):
    self.assertEqual(Element(html="<a>b</a>"), Element(html="<a>b</a>"), hashes_too=True)
    self.assertNotEqual(Element(html="<a>b</a>"), Element(html="<a>c</a>"))
    self.assertNotEqual(Element(html="<a>b</a>"), Element(html="<b>a</b>"))

    a1 = Element(html="<a></a>")
    a2 = Element(html="<a></a>")
    self.assertEqual(a1, a2, hashes_too=True)

    container = Element(tag_name="div")
    container.append(a1)
    self.assertEqual(a1, a2, hashes_too=True)

    a2.add_callback("blahblahtrigger", (lambda event: print(event)))
    self.assertNotEqual(a1, a2)

  def test_orphaned(self):
    container = Element(tag_name="c")
    first = Element(tag_name="f")
    second = Element(tag_name="s")
    
    self.assertTrue(container.orphaned)
    self.assertTrue(first.orphaned)
    self.assertTrue(second.orphaned)

    container.append(first)
    self.assertFalse(first.orphaned)

    first.insert_after(second)
    self.assertFalse(second.orphaned)

    container.disown(first)
    self.assertTrue(first.orphaned)

    second.remove_self()
    self.assertTrue(second.orphaned)

  def test_parent(self):
    container = Element(tag_name="c")
    first = Element(tag_name="f")
    second = Element(tag_name="s")

    self.assertNone(first.parent)

    container.append(first)
    self.assertEqual(container, first.parent)

    first.insert_after(second)
    self.assertEqual(container, second.parent)

    container.disown(first)
    self.assertNone(first.parent)

    second.remove_self()
    self.assertNone(second.parent)

  def test_children(self):
    container = Element(tag_name="c")
    first = Element(tag_name="f")
    second = Element(tag_name="s")

    self.assertEqual(list(container.children), [])

    container.append(first)
    self.assertEqual(list(container.children), [first])

    first.insert_after(second)
    self.assertEqual(list(container.children), [first, second])

    container.disown(first)
    self.assertEqual(list(container.children), [second])

    second.remove_self()
    self.assertEqual(list(container.children), [])

  def test_callbacks(self):
    last_event = None
    def set_event(event):
      nonlocal last_event
      last_event = event

    e = Element(tag_name="a")
    e.add_callback(CLICK, set_event)
    e.add_callback(KEYDOWN, set_event)

    e.handle_event({'type': CLICK, 'id': e.id})
    self.assertEqual(last_event, {'type': CLICK, 'id': e.id})

    e.handle_event({'type': KEYDOWN, 'id': e.id, 'key': 'a'})
    self.assertEqual(last_event, {'type': KEYDOWN, 'id': e.id, 'key': 'a'})

    with self.assertRaises(NoCallbackException):
      e.handle_event({'type': KEYUP, 'id': e.id, 'key': 'a'})

    e.remove_callback(CLICK, set_event)
    with self.assertRaises(NoCallbackException):
      e.handle_event({'type': CLICK, 'id': e.id})
    self.assertEqual(last_event, {'type': KEYDOWN, 'id': e.id, 'key': 'a'})

    self.assertEqual(list(e.callbacks[CLICK]), [])
    self.assertEqual(list(e.callbacks[KEYDOWN]), [set_event])
    self.assertEqual(list(e.callbacks[KEYUP]), [])