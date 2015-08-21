import fractions
from browsergui import NumberField
from . import BrowserGUITestCase

class NumberFieldTest(BrowserGUITestCase):
  def test_validation(self):
    n = NumberField()

    for good_object in (None, 0, 1, 1.1, -1.1, fractions.Fraction(1,1)):
      n.value = good_object

    for bad_object in (1j, []):
      with self.assertRaises(TypeError):
        n.value = bad_object
