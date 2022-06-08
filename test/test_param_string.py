
from unittest import TestCase 
from exofile import ParamString

class TestParamString (TestCase):

  def test_quoted_string (self):
    self.assertEqual(ParamString(""), "")
    self.assertEqual(ParamString("abc"), "abc")
    self.assertEqual(ParamString(ParamString("abc")), "abc")

  def test_serialize (self):
    self.assertEqual(ParamString("").serialize(), '""')
    self.assertEqual(ParamString("abc").serialize(), '"abc"')
    with self.assertRaises(ValueError):
      ParamString("abc\"").serialize() #reserved character '"'.
    with self.assertRaises(ValueError):
      ParamString("abc;").serialize() #reserved character ';'.
  
  def test_deserialize (self):
    self.assertEqual(ParamString.deserialize('""'), "")
    self.assertEqual(ParamString.deserialize('"abc"'), "abc")
    with self.assertRaises(ValueError):
      ParamString.deserialize('')
