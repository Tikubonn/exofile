
from unittest import TestCase 
from exofile import Color

class TestColor (TestCase):

  def test_color (self):
    color = Color(0x12, 0x34, 0x56)
    self.assertEqual(color.red, 0x12)
    self.assertEqual(color.green, 0x34)
    self.assertEqual(color.blue, 0x56)
    self.assertEqual(color.serialize(), "123456")

  def test_color_error (self):
    color = Color(-1, 0, 0)
    with self.assertRaises(ValueError):
      color.serialize()
    color = Color(0, -1, 0)
    with self.assertRaises(ValueError):
      color.serialize()
    color = Color(0, 0, -1)
    with self.assertRaises(ValueError):
      color.serialize()
    color = Color(256, 0, 0)
    with self.assertRaises(ValueError):
      color.serialize()
    color = Color(0, 256, 0)
    with self.assertRaises(ValueError):
      color.serialize()
    color = Color(0, 0, 256)
    with self.assertRaises(ValueError):
      color.serialize()

  def test_color_deserialize (self):
    color = Color.deserialize("123456")
    self.assertEqual(color.red, 0x12)
    self.assertEqual(color.green, 0x34)
    self.assertEqual(color.blue, 0x56)
    self.assertEqual(color.serialize(), "123456")

  def test_color_deserialize_error (self):
    with self.assertRaises(ValueError):
      Color.deserialize("12345") #under 5
    with self.assertRaises(ValueError):
      Color.deserialize("1234567") #over 6
  
  def test_color_compare (self):
    self.assertEqual(Color(0x12, 0x34, 0x56), Color(0x12, 0x34, 0x56))
    self.assertNotEqual(Color(0x12, 0x34, 0x56), Color(0x0, 0x34, 0x56))
    self.assertNotEqual(Color(0x12, 0x34, 0x56), Color(0x12, 0x0, 0x56))
    self.assertNotEqual(Color(0x12, 0x34, 0x56), Color(0x12, 0x34, 0x0))
