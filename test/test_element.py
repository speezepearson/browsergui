from browsergui import Element, CLICK, KEYDOWN, KEYUP
from browsergui.elements import NoSuchCallbackError

from . import BrowserGUITestCase

class ElementTest(BrowserGUITestCase):

  def test_construction(self):

    Element(tag_name="a")
    Element(tag_name="a", children=[Element(tag_name="b")])
      
    with self.assertRaises(TypeError):
      Element(tag_name="a", children=0)
    with self.assertRaises(TypeError):
      Element(tag_name="a", children=[0])

  def test_hash_static(self):
    a = Element(tag_name="a")
    h = hash(a)

    self.assertEqual(h, hash(a))

    a.append(Element(tag_name="b"))
    self.assertEqual(h, hash(a))

    a.add_callback("blahblahtrigger", self.set_last_event)
    self.assertEqual(h, hash(a))

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

    second.extract()
    self.assertTrue(second.orphaned)

  def test_parent(self):
    container = Element(tag_name="c")
    first = Element(tag_name="f")
    second = Element(tag_name="s")

    self.assertIsNone(first.parent)

    container.append(first)
    self.assertEqual(container, first.parent)

    first.insert_after(second)
    self.assertEqual(container, second.parent)

    container.disown(first)
    self.assertIsNone(first.parent)

    second.extract()
    self.assertIsNone(second.parent)

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

    second.extract()
    self.assertEqual(list(container.children), [])

  def test_callbacks(self):

    e = Element(tag_name="a")
    e.add_callback(CLICK, self.set_last_event)
    e.add_callback(KEYDOWN, self.set_last_event)

    e.handle_event({'type': CLICK, 'id': e.id})
    self.assertEqual(self.last_event, {'type': CLICK, 'id': e.id})

    e.handle_event({'type': KEYDOWN, 'id': e.id, 'key': 'a'})
    self.assertEqual(self.last_event, {'type': KEYDOWN, 'id': e.id, 'key': 'a'})

    e.remove_callback(CLICK, self.set_last_event)
    with self.assertRaises(NoSuchCallbackError):
      e.remove_callback(CLICK, self.set_last_event)

    self.assertEqual(list(e.callbacks[CLICK]), [])
    self.assertEqual(list(e.callbacks[KEYDOWN]), [self.set_last_event])
    self.assertEqual(list(e.callbacks[KEYUP]), [])

  def test_toggle_visibility(self):
    e = Element(tag_name='a')
    e.toggle_visibility()
    self.assertEqual('none', e.get_style('display'))
    e.toggle_visibility()
    self.assertIsNone(e.get_style('display'))
