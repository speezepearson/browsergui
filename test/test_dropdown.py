from browsergui import Dropdown, Text
from . import BrowserGUITestCase

def dropdown_xml(*options):
  return '<select>{}</select>'.format(''.join('<option value="{s}">{s}</option>'.format(s=s) for s in options))

class DropdownTest(BrowserGUITestCase):

  def test_construction(self):
    self.assertEqual(['a', 'b'], list(Dropdown(['a', 'b'])))

    with self.assertRaises(ValueError):
      Dropdown([])

  def test_options_must_be_strings(self):
    with self.assertRaises(TypeError):
      Dropdown([()])

    d = Dropdown(['a'])
    with self.assertRaises(TypeError):
      d[0] = ()
    with self.assertRaises(TypeError):
      d.insert(0, ())

  def test_getitem(self):
    d = Dropdown(['a', 'b'])
    self.assertEqual(['a', 'b'], d[:])
    self.assertEqual('a', d[0])
    with self.assertRaises(IndexError):
      d[2]

  def test_delitem(self):
    d = Dropdown(['a', 'b'])

    del d[0]
    self.assertEqual('b', d[0])
    with self.assertRaises(IndexError):
      d[1]

    self.assertHTMLLike(dropdown_xml('b'), d, ignored_attrs=['id', 'oninput', 'selected'])

  def test_setitem(self):
    d = Dropdown(['a', 'b'])

    d[0] = 'c'
    self.assertEqual(d[0], 'c')
    self.assertEqual(2, len(d))

    self.assertHTMLLike(dropdown_xml('c', 'b'), d, ignored_attrs=['id', 'oninput', 'selected'])

  def test_insert(self):
    d = Dropdown(['b'])
    d.insert(0, 'a')
    d.insert(99, 'd')
    d.insert(-1, 'c')
    self.assertEqual(['a', 'b', 'c', 'd'], list(d))
    self.assertHTMLLike(dropdown_xml('a', 'b', 'c', 'd'), d, ignored_attrs=['id', 'oninput', 'selected'])

  def test_tag(self):
    self.assertHTMLLike('<select oninput="notify_server({target_id: this.getAttribute(&quot;id&quot;), type_name: event.type, value: this.value})"><option value="a" selected="true">a</option></select>', Dropdown(['a']), ignored_attrs=['id'])
    self.assertHTMLLike('<select><option value="a">a</option><option value="b">b</option></select>', Dropdown(['a', 'b']), ignored_attrs=['id', 'oninput', 'selected'])

  def test_validation(self):
    d = Dropdown(['a', 'b', 'c'])

    for good_object in ('a', 'b', 'c', u'a'):
      d.value = good_object

    for bad_object in (0, []):
      with self.assertRaises(TypeError):
        d.value = bad_object

    for bad_object in ('not in it'):
      with self.assertRaises(ValueError):
        d.value = bad_object
