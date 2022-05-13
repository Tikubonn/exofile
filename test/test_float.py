
from unittest import TestCase 
from exofile import Float

class TestFloat (TestCase):

  def test_serialize (self):
    num = Float(-100.50, decimalpartdigits=2)
    self.assertEqual(num, -100.50)
    self.assertEqual(num.serialize(), "-100.50")
    num = Float(100.50, decimalpartdigits=2)
    self.assertEqual(num, 100.50)
    self.assertEqual(num.serialize(), "100.50")
    num = Float(0.0)
    self.assertEqual(num, 0.0)
    self.assertEqual(num.serialize(), "0.0") 

  def test_deserialize (self):
    num = Float.deserialize("-100.50")
    self.assertEqual(num, -100.50)
    self.assertEqual(num.serialize(), "-100.50")
    num = Float.deserialize("100.50")
    self.assertEqual(num, 100.50)
    self.assertEqual(num.serialize(), "100.50")
    num = Float.deserialize("0.0")
    self.assertEqual(num, 0.0)
    self.assertEqual(num.serialize(), "0.0") 

  def test_deserialize_error (self):
    with self.assertRaises(ValueError):
      Float.deserialize("-100")
    with self.assertRaises(ValueError):
      Float.deserialize("100")
    with self.assertRaises(ValueError):
      Float.deserialize("0")
    with self.assertRaises(ValueError):
      Float.deserialize("")

  def test_copy (self):
    num = Float(-100.50, decimalpartdigits=2)
    numcopy = Float(num)
    self.assertEqual(numcopy, num)
    self.assertEqual(numcopy.decimalpartdigits, num.decimalpartdigits)
