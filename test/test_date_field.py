import datetime
from browsergui import DateField
from . import BrowserGUITestCase

class DateFieldTest(BrowserGUITestCase):
  def setUp(self):
    DateField.warn_about_potential_browser_incompatibility = False

  def test_validation(self):
    d = DateField()

    for good_object in (None, datetime.date(2015, 9, 30)):
      d.value = good_object

    for bad_object in ('2015-05-05', 0):
      with self.assertRaises(TypeError):
        d.value = bad_object

    for bad_object in (datetime.datetime(2015, 3, 2, 0, 0, 0),):
      with self.assertRaises(ValueError):
        d.value = bad_object
