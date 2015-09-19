from browsergui import List, Text
from . import BrowserGUITestCase

def list_of_texts_xml(*strings):
  return '<ol style="list-style-type: disc">{}</ol>'.format(''.join('<li><span>{}</span></li>'.format(s) for s in strings))

class ListTest(BrowserGUITestCase):

  def test_construction(self):
    List()
    List(items=[List()])
    List(numbered=True)
    List(numbered=False)

  def test_children(self):
    first = List()
    second = List()
    top = List(items=(first, second))
    self.assertEqual(list(top.children), [first, second])

  def test_getitem(self):
    first = Text('1')
    second = Text('2')
    top = List(items=(first, second))

    self.assertEqual(top[0], first)
    self.assertEqual(top[1], second)
    with self.assertRaises(IndexError):
      top[2]

  def test_delitem(self):
    first = Text('1')
    second = Text('2')
    top = List(items=(first, second))

    del top[0]
    self.assertIsNone(first.parent)
    self.assertEqual(list(top.children), [second])
    self.assertEqual(second, top[0])
    with self.assertRaises(IndexError):
      top[1]

    self.assertHTMLLike(list_of_texts_xml('2'), top)

  def test_setitem(self):
    first = Text('1')
    second = Text('2')
    new = Text('new')
    top = List(items=(first, second))

    top[0] = new
    self.assertEqual(top[0], new)
    self.assertIsNone(first.parent)
    self.assertEqual(top, new.parent)
    self.assertEqual(list(top.children), [new, second])

    self.assertHTMLLike(list_of_texts_xml('new', '2'), top)

  def test_insert(self):
    first = Text('1')
    second = Text('2')
    third = Text('3')
    fourth = Text('4')
    top = List()

    top.insert(0, second)
    self.assertEqual(top, second.parent)
    self.assertEqual(list(top.children), [second])

    top.insert(0, first)
    self.assertEqual(list(top.children), [first, second])

    top.insert(99, fourth)
    self.assertEqual(list(top.children), [first, second, fourth])

    top.insert(-1, third)
    self.assertEqual(list(top.children), [first, second, third, fourth])

    self.assertHTMLLike(list_of_texts_xml('1', '2', '3', '4'), top)

  def test_children_must_be_elements(self):
    with self.assertRaises(TypeError):
      List(items=[0])

  def test_tag(self):
    self.assertHTMLLike('<ol style="list-style-type: disc"/>', List(numbered=False))
    self.assertHTMLLike('<ol style="list-style-type: decimal"/>', List(numbered=True))
    self.assertHTMLLike('<ol style="list-style-type: disc"><li><span>hi</span></li></ol>', List(items=[Text("hi")]))
