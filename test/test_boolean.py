
from unittest import TestCase 
from exofile import Boolean

class TestBoolean (TestCase):

  def test_boolean (self):
    b = Boolean.deserialize("1")
    self.assertEqual(b, True)
    self.assertEqual(b.serialize(), "1")
    b = Boolean.deserialize("0")
    self.assertEqual(b, False)
    self.assertEqual(b.serialize(), "0")

  def test_boolean2 (self):
    b = Boolean(True)
    self.assertEqual(b, True)
    self.assertEqual(b.serialize(), "1")
    b = Boolean(False)
    self.assertEqual(b, False)
    self.assertEqual(b.serialize(), "0")

  def test_boolean_error (self):
    with self.assertRaises(ValueError): 
      Boolean.deserialize("-1")
    with self.assertRaises(ValueError): 
      Boolean.deserialize("2")
    with self.assertRaises(ValueError): 
      Boolean.deserialize("11")
    with self.assertRaises(ValueError): 
      Boolean.deserialize("00")
    with self.assertRaises(ValueError): 
      Boolean.deserialize("")
