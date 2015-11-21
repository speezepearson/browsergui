from fractions import Fraction
from browsergui import Slider
from . import BrowserGUITestCase

class SliderTest(BrowserGUITestCase):
  def test_type_validation(self):
    s = Slider(min=0, max=10)

    for good_object in [0, 1, 1.1, Fraction(1,10)]:
      s.value = good_object

    for bad_object in [float('NaN'), 1j, []]:
      with self.assertRaises(TypeError):
        s.value = bad_object

  def test_range_validation(self):
    s = Slider(min=0, max=5)

    for good_value in [0, 1, 5, 2**0.5]:
      s.value = good_value

    for bad_value in [-1, 6, float('inf'), float('-inf')]:
      with self.assertRaises(ValueError):
        s.value = bad_value

  def test_bounds(self):
    s = Slider(min=0, max=5)
    self.assertEqual(s.min, 0)
    self.assertEqual(s.max, 5)

    # Make sure more the bounds aren't, say, coerced to floats
    self.assertIsInstance(s.min, int)
    self.assertIsInstance(s.max, int)

  def test_set_bounds(self):
    s = Slider(min=0, max=5)
    s.value = 3
    s.min = 1
    self.assertEqual(s.min, 1)
    self.assertEqual(s.value, 3)
    s.min = 3
    self.assertEqual(s.min, 3)
    self.assertEqual(s.value, 3)

    with self.assertRaises(ValueError):
      s.min = 4

    s.min = 0
    self.assertEqual(s.min, 0)

    s.max = 4
    self.assertEqual(s.max, 4)
    self.assertEqual(s.value, 3)
    s.max = 3
    self.assertEqual(s.max, 3)
    self.assertEqual(s.value, 3)

    with self.assertRaises(ValueError):
      s.max = 1


  def test_set_bounds__marks_dirty(self):
    s = Slider(min=0, max=5)
    with self.assertMarksDirty(s):
      s.min = 1
    with self.assertMarksDirty(s):
      s.max = 4

  def test_exotic_bounds(self):
    s = Slider(min=Fraction(1,10), max=Fraction(9,10))
    self.assertEqual(s.min, Fraction(1, 10))
    self.assertEqual(s.max, Fraction(9, 10))
