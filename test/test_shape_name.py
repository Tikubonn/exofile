
from exofile import ShapeName, String 
from unittest import TestCase 

class TestShapeName (TestCase):

  def test_serialize (self):
    shapename = ShapeName("")
    self.assertEqual(shapename, "")
    self.assertEqual(shapename.serialize(), "")
    shapename = ShapeName("./example.png")
    self.assertEqual(shapename, "./example.png")
    self.assertEqual(shapename.serialize(), "*./example.png")

  def test_deserialize (self):
    shapename = ShapeName.deserialize("")
    self.assertIsInstance(shapename, ShapeName)
    self.assertEqual(shapename, "")
    self.assertEqual(shapename.serialize(), "")
    shapename = ShapeName.deserialize("*./example.png")
    self.assertIsInstance(shapename, ShapeName)
    self.assertEqual(shapename, "./example.png")
    self.assertEqual(shapename.serialize(), "*./example.png")

  def test_deserialize_error (self):
    with self.assertRaises(ValueError):
      ShapeName.deserialize("./example.png") #must starts with *.
