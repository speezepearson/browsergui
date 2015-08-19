from browsergui import ColorField
from . import BrowserGUITestCase

class ColorFieldTest(BrowserGUITestCase):
  def setUp(self):
    ColorField.warn_about_potential_browser_incompatibility = False

  def test_validation(self):
    c = ColorField()

    for good_object in ((0,0,0), (1,2,3), [1,2,3]):
      c.value = good_object

    for bad_object in (None, (x for x in [1,2,3]), (1, 2, 3.0), '123', (1, 2, '3'), 123):
      with self.assertRaises(TypeError):
        c.value = bad_object

    for bad_object in ((1, 2, -3), (1, 2, 256)):
      with self.assertRaises(ValueError):
        c.value = bad_object
