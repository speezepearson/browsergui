import re
import unittest
import xml.dom.minidom
import contextlib

def walk(tag):
  yield tag
  for child in tag.childNodes:
    for descendant in walk(child):
      yield descendant

class BrowserGUITestCase(unittest.TestCase):
  def setUp(self):
    self.last_event = None

  def set_last_event(self, event):
    self.last_event = event

  @contextlib.contextmanager
  def assertSetsEvent(self, event):
    self.last_event = None
    yield
    self.assertEqual(event, self.last_event)

  def assertHTMLIn(self, included, html):
    self.assertIn(re.sub("\s", "", included), re.sub("\s", "", html))

  def assertHTMLLike(self, expected_string, element, ignored_attrs=['id']):
    """Asserts the HTML for an element is equivalent to the given HTML.

    :param str expected_string: XML string the element's HTML should look like
    :param Element element:
    :param iterable ignored_attrs: ignore differences in attributes with these names
    """
    expected_tag = xml.dom.minidom.parseString(expected_string).documentElement
    tag = xml.dom.minidom.parseString(element.tag.toxml()).documentElement

    for attr in ignored_attrs:
      for descendant in walk(tag):
        if descendant.attributes is None: continue
        if attr in descendant.attributes.keys():
          descendant.removeAttribute(attr)
      for descendant in walk(expected_tag):
        if descendant.attributes is None: continue
        if attr in descendant.attributes.keys():
          descendant.removeAttribute(attr)

    self.assertEqual(tag.toxml(), expected_tag.toxml())

  def assertUnstyledHTMLLike(self, xml, grid, ignored_attrs=['id']):
    ignored_attrs = set(ignored_attrs)
    ignored_attrs.add('style')
    self.assertHTMLLike(xml, grid, ignored_attrs=ignored_attrs)
