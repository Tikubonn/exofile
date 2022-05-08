
from unittest import TestCase 
from exofile import Int

class TestInt (TestCase):

  def test_int (self):
    num = Int.deserialize("-100")
    self.assertEqual(num, -100)
    self.assertEqual(num.serialize(), "-100")
    num = Int.deserialize("100")
    self.assertEqual(num, 100)
    self.assertEqual(num.serialize(), "100")
    num = Int.deserialize("0")
    self.assertEqual(num, 0)
    self.assertEqual(num.serialize(), "0")

  def test_int2 (self):
    num = Int(-100)
    self.assertEqual(num, -100)
    self.assertEqual(num.serialize(), "-100")
    num = Int(100)
    self.assertEqual(num, 100)
    self.assertEqual(num.serialize(), "100")
    num = Int(0)
    self.assertEqual(num, 0)
    self.assertEqual(num.serialize(), "0")

  def test_int_error (self):
    with self.assertRaises(ValueError):
      Int.deserialize("-100.0")
    with self.assertRaises(ValueError):
      Int.deserialize("100.0")
    with self.assertRaises(ValueError):
      Int.deserialize("0.0")
