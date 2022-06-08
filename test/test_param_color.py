
from unittest import TestCase 
from exofile import ParamColor, Color 

class TestParamColor (TestCase):

  def test_param_color (self):
    self.assertEqual(ParamColor(0 ,0, 0), Color(0, 0, 0))
    self.assertEqual(ParamColor(0x12, 0x34, 0x56), Color(0x12, 0x34, 0x56))
    self.assertEqual(ParamColor(0xab, 0xcd, 0xef), Color(0xab, 0xcd, 0xef))

  def test_serialize (self):
    self.assertEqual(ParamColor(0, 0, 0).serialize(), "0x000000")
    self.assertEqual(ParamColor(0x12, 0x34, 0x56).serialize(), "0x123456")
    self.assertEqual(ParamColor(0xab, 0xcd, 0xef).serialize(), "0xabcdef")

  def test_deserialize (self):
    self.assertEqual(ParamColor.deserialize("0x000000"), ParamColor(0, 0, 0))
    self.assertEqual(ParamColor.deserialize("0x123456"), ParamColor(0x12, 0x34, 0x56))
    self.assertEqual(ParamColor.deserialize("0xabcdef"), ParamColor(0xab, 0xcd, 0xef))
    with self.assertRaises(ValueError):
      ParamColor.deserialize("")
    with self.assertRaises(ValueError):
      ParamColor.deserialize("000000")
