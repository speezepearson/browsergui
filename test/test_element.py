import json
from browsergui import Element, Container, Event, Click

from . import BrowserGUITestCase

class ElementTest(BrowserGUITestCase):

  def test_construction(self):
    Element(tag_name="a")
