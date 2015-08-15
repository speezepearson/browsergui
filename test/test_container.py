from browsergui import Container, Click
from . import BrowserGUITestCase

class ContainerTest(BrowserGUITestCase):
  def test_construction(self):
    left = Container()
    right = Container()
    top = Container(left, right)
    self.assertEqual(list(top.children), [left, right])

  def test_children_must_be_elements(self):
    with self.assertRaises(TypeError):
      Container(0)

  def test_tag(self):
    self.assertHTMLLike('<div />', Container())
    self.assertHTMLLike('<span />', Container(tag_name='span'))

  def test_children(self):
    container = Container()
    first = Container()
    second = Container()

    self.assertEqual(list(container.children), [])

    container.append(first)
    self.assertEqual(list(container.children), [first])

    container.insert_after(second, reference_child=first)
    self.assertEqual(list(container.children), [first, second])

    container.disown(first)
    self.assertEqual(list(container.children), [second])

    container.disown(second)
    self.assertEqual(list(container.children), [])

  def test_hash_static(self):
    c = Container()
    h = hash(c)

    self.assertEqual(h, hash(c))

    c.append(Container())
    self.assertEqual(h, hash(c))

    c.add_callback(Click, self.set_last_event)
    self.assertEqual(h, hash(c))
