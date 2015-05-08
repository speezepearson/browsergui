class TestCaseWithImportantHashes(unittest.TestCase):
  def assertEqual(self, x, y, hashes_too=True):
    self.assertEqual(x, y)
    if hashes_too:
      self.assertEqual(hash(x), hash(y))

class ContainerTest(TestCaseWithImportantHashes):
  def test_construction(self):
    self.assertEqual(Container(), Element(tag_name="div"))
    self.assertEqual(Container(inline=True), Element(tag_name="span"))

    left = Container()
    right = Container()
    top = Container(left, right)
    self.assertEqual(list(top.children), [left, right])

    with self.assertRaises(TypeError):
      Container(0)

class TextTest(TestCaseWithImportantHashes):
  def test_construction(self):
    text = Text("blah")
    self.assertEqual(text.text, "blah")
    
    with self.assertRaises(TypeError):
      Text(0)

class ButtonTest(TestCaseWithImportantHashes):
  def test_construction(self):
    self.assertEqual(Button("Press me"), Element(html="<button>Press me</button>"))

  def test_default_text(self):
    self.assertEqual(Button().text, "Button!")

  def test_set_callback(self):
    clicked = False
    def toggle():
      nonlocal clicked
      clicked = True

    b = Button(callback=(lambda event: toggle()))
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertTrue(clicked)

    clicked = False
    b = Button()
    b.set_callback(lambda event: toggle())
    b.handle_event({'type': CLICK, 'id': b.id})
    self.assertTrue(clicked)