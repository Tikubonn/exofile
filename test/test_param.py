
from unittest import TestCase 
from exofile import ParamColor, ParamString, Float, Int, Param

class TestParam (TestCase):

  def test_serialize (self):
    param = Param({
      "a": Int(1),
      "b": Int(2),
      "c": Int(3),
    })
    self.assertEqual(param.serialize(), "a=1;b=2;c=3;")

  def test_serialize2 (self):
    param = Param({
      "a": Float(1.0, decimalpartdigits=2),
      "b": Float(2.0, decimalpartdigits=2),
      "c": Float(3.0, decimalpartdigits=2),
    })
    self.assertEqual(param.serialize(), "a=1.00;b=2.00;c=3.00;")

  def test_serialize3 (self):
    param = Param({
      "a": ParamString("a"),
      "b": ParamString("b"),
      "c": ParamString("c"),
    })
    self.assertEqual(param.serialize(), 'a="a";b="b";c="c";')

  def test_serialize4 (self):
    param = Param({
      "a": ParamColor(0, 0, 0),
      "b": ParamColor(0x12, 0x34, 0x56),
      "c": ParamColor(0xab, 0xcd, 0xef),
    })
    self.assertEqual(param.serialize(), 'a=0x000000;b=0x123456;c=0xabcdef;')

  def test_deserialize (self):
    param = Param.deserialize("a=1;b=2;c=3;")
    self.assertIsInstance(param["a"], Int)
    self.assertIsInstance(param["b"], Int)
    self.assertIsInstance(param["c"], Int)
    self.assertEqual(param["a"], Int(1))
    self.assertEqual(param["b"], Int(2))
    self.assertEqual(param["c"], Int(3))

  def test_deserialize2 (self):
    param = Param.deserialize("a=1.00;b=2.00;c=3.00;")
    self.assertIsInstance(param["a"], Float)
    self.assertIsInstance(param["b"], Float)
    self.assertIsInstance(param["c"], Float)
    self.assertEqual(param["a"], Float(1.0))
    self.assertEqual(param["b"], Float(2.0))
    self.assertEqual(param["c"], Float(3.0))
    self.assertEqual(param["a"].decimalpartdigits, 2)
    self.assertEqual(param["b"].decimalpartdigits, 2)
    self.assertEqual(param["c"].decimalpartdigits, 2)

  def test_deserialize3 (self):
    param = Param.deserialize('a="a";b="b";c="c";')
    self.assertIsInstance(param["a"], ParamString)
    self.assertIsInstance(param["b"], ParamString)
    self.assertIsInstance(param["c"], ParamString)
    self.assertEqual(param["a"], ParamString("a"))
    self.assertEqual(param["b"], ParamString("b"))
    self.assertEqual(param["c"], ParamString("c"))

  def test_deserialize4 (self):
    param = Param.deserialize('a=0x000000;b=0x123456;c=0xabcdef;')
    self.assertIsInstance(param["a"], ParamColor)
    self.assertIsInstance(param["b"], ParamColor)
    self.assertIsInstance(param["c"], ParamColor)
    self.assertEqual(param["a"], ParamColor(0, 0, 0))
    self.assertEqual(param["b"], ParamColor(0x12, 0x34, 0x56))
    self.assertEqual(param["c"], ParamColor(0xab, 0xcd, 0xef))

  def test_deserialize_with_whitespace (self): #--colorダイアログは空白を含んでしまうので、それでも問題なく動作するかを検証します。
    param = Param.deserialize('a= 0x000000;b= 0x123456;c= 0xabcdef;')
    self.assertIsInstance(param["a"], ParamColor)
    self.assertIsInstance(param["b"], ParamColor)
    self.assertIsInstance(param["c"], ParamColor)
    self.assertEqual(param["a"], ParamColor(0, 0, 0))
    self.assertEqual(param["b"], ParamColor(0x12, 0x34, 0x56))
    self.assertEqual(param["c"], ParamColor(0xab, 0xcd, 0xef))

  def test_deserialize_local (self):
    param = Param.deserialize("local a=1;local b=2;local c=3;")
    self.assertIsInstance(param["local a"], Int)
    self.assertIsInstance(param["local b"], Int)
    self.assertIsInstance(param["local c"], Int)
    self.assertEqual(param["local a"], Int(1))
    self.assertEqual(param["local b"], Int(2))
    self.assertEqual(param["local c"], Int(3))

  def test_deserialize_local2 (self):
    param = Param.deserialize("local a=1.00;local b=2.00;local c=3.00;")
    self.assertIsInstance(param["local a"], Float)
    self.assertIsInstance(param["local b"], Float)
    self.assertIsInstance(param["local c"], Float)
    self.assertEqual(param["local a"], Float(1.0))
    self.assertEqual(param["local b"], Float(2.0))
    self.assertEqual(param["local c"], Float(3.0))
    self.assertEqual(param["local a"].decimalpartdigits, 2)
    self.assertEqual(param["local b"].decimalpartdigits, 2)
    self.assertEqual(param["local c"].decimalpartdigits, 2)

  def test_deserialize_local3 (self):
    param = Param.deserialize('local a="a";local b="b";local c="c";')
    self.assertIsInstance(param["local a"], ParamString)
    self.assertIsInstance(param["local b"], ParamString)
    self.assertIsInstance(param["local c"], ParamString)
    self.assertEqual(param["local a"], ParamString("a"))
    self.assertEqual(param["local b"], ParamString("b"))
    self.assertEqual(param["local c"], ParamString("c"))

  def test_deserialize_local4 (self):
    param = Param.deserialize('local a=0x000000;local b=0x123456;local c=0xabcdef;')
    self.assertIsInstance(param["local a"], ParamColor)
    self.assertIsInstance(param["local b"], ParamColor)
    self.assertIsInstance(param["local c"], ParamColor)
    self.assertEqual(param["local a"], ParamColor(0, 0, 0))
    self.assertEqual(param["local b"], ParamColor(0x12, 0x34, 0x56))
    self.assertEqual(param["local c"], ParamColor(0xab, 0xcd, 0xef))
