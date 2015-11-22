from fractions import Fraction
import datetime
from browsergui import Slider, FloatSlider, IntegerSlider
from . import BrowserGUITestCase

class SliderTest(BrowserGUITestCase):

  def test_range_validation(self):
    s = FloatSlider(min=0, max=5)

    for good_value in [0, 1, 5]:
      s.value = good_value

    for bad_value in [-1, 6]:
      with self.assertRaises(ValueError):
        s.value = bad_value

  def test_bounds(self):
    s = FloatSlider(min=0, max=5)
    self.assertEqual(s.min, 0)
    self.assertEqual(s.max, 5)

  def test_set_bounds(self):
    s = FloatSlider(min=0, max=5)
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
    s = FloatSlider(min=0, max=5)
    with self.assertMarksDirty(s):
      s.min = 1
    with self.assertMarksDirty(s):
      s.max = 4

  def test_set_value(self):
    s = FloatSlider(min=0, max=5)
    s.value = 3
    self.assertEqual(s.value, 3)

    with self.assertRaises(ValueError):
      s.value = -1
    with self.assertRaises(ValueError):
      s.value = 6

    self.assertEqual(s.value, 3)

class FloatSliderTest(BrowserGUITestCase):

  def test_type_validation(self):
    s = FloatSlider(min=0, max=5)
    for good_value in [1, 2**0.5, Fraction(1, 10)]:
      s.value = good_value

    for bad_value in [[], '3', float('NaN'), float('inf'), float('-inf')]:
      with self.assertRaises(TypeError):
        s.value = bad_value

class IntegerSliderTest(BrowserGUITestCase):
  def test_type_validation(self):
    s = IntegerSlider(min=0, max=10)

    for good_object in [0, 1, 10]:
      s.value = good_object

    for bad_object in [0.0, 1.2, 1j, []]:
      with self.assertRaises(TypeError):
        s.value = bad_object

_DATE_ZERO = datetime.date(2015, 1, 1)
class DateSlider(Slider):
  DISCRETE = True
  @staticmethod
  def value_to_number(x):
    if not isinstance(x, datetime.date):
      raise TypeError('expected date, got {}'.format(type(x).__name__))
    return int(round((x-_DATE_ZERO).total_seconds() / datetime.timedelta(days=1).total_seconds()))
  @staticmethod
  def value_from_number(x):
    return _DATE_ZERO + datetime.timedelta(days=x)
class DateSliderTest(BrowserGUITestCase):
  def test_type_validation(self):
    s = DateSlider(min=datetime.date(2015, 1, 1), max=datetime.date(2015, 1, 31))

    for good_object in [datetime.date(2015, 1, 8)]:
      s.value = good_object

    for bad_object in [0, datetime.datetime(2015, 1, 1, 12, 0, 0)]:
      with self.assertRaises(TypeError):
        s.value = bad_object
