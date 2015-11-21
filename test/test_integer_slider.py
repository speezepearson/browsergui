from fractions import Fraction
from browsergui import IntegerSlider
from . import BrowserGUITestCase

class IntegerSliderTest(BrowserGUITestCase):
  def test_type_validation(self):
    s = IntegerSlider(min=0, max=10)

    for good_object in [0, 1, 10]:
      s.value = good_object

    for bad_object in [0.0, 1.2, 1j, []]:
      with self.assertRaises(TypeError):
        s.value = bad_object

  def test_range_validation(self):
    s = IntegerSlider(min=0, max=5)

    for good_value in [0, 1, 5]:
      s.value = good_value

    for bad_value in [-1, 6]:
      with self.assertRaises(ValueError):
        s.value = bad_value

  def test_bounds(self):
    s = IntegerSlider(min=0, max=5)
    self.assertEqual(s.min, 0)
    self.assertEqual(s.max, 5)

  def test_set_bounds(self):
    s = IntegerSlider(min=0, max=5)
    s.value = 3
    s.min = 1
    self.assertEqual(s.value, 3)
    s.min = 3
    self.assertEqual(s.value, 3)

    with self.assertRaises(ValueError):
      s.min = 4

    s.min = 0

    with self.assertRaises(ValueError):
      s.max = 1
