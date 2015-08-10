import re
import unittest
import xml.dom.minidom
import contextlib

def delete_ids(tag):
  if tag.attributes is not None and 'id' in tag.attributes.keys():
    tag.removeAttribute('id')
  for child in tag.childNodes:
    delete_ids(child)

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

  def assertHTMLLike(self, expected_string, element, ignore_id=True):
    """Asserts the HTML for an element is equivalent to the given HTML.

    If `ignore_id` is given, ignores all given elements' `id` attribute,
    since they're presumably automatically generated and irrelevant.
    """
    expected_tag = xml.dom.minidom.parseString(expected_string).documentElement
    tag = xml.dom.minidom.parseString(element.tag.toxml()).documentElement
    if ignore_id:
      delete_ids(tag)

    self.assertEqual(tag.toxml(), expected_tag.toxml())
