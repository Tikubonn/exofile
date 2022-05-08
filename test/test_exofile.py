
from exofile import EXOFile
from unittest import TestCase 

class TestEXOFile (TestCase):

  def test_exofile (self):
    exofile = EXOFile()
    exofile.set("example", "one", "1")
    exofile.set("example", "two", "2")
    exofile.set("example", "three", "3")
    exofile.set("exedit", "one", "1")
    exofile.set("exedit", "two", "2")
    exofile.set("exedit", "three", "3")
    exofile.set("example2", "one", "1")
    exofile.set("example2", "two", "2")
    exofile.set("example2", "three", "3")
    exofilekeys = iter(exofile.keys())
    self.assertEqual(next(exofilekeys), "exedit")
    self.assertEqual(next(exofilekeys), "example")
    self.assertEqual(next(exofilekeys), "example2")
    with self.assertRaises(StopIteration):
      next(exofilekeys)

  def test_exofile2 (self):
    TEST_DATA = """[exedit]
one=1
two=2
three=3
[example]
one=1
two=2
three=3
[example2]
one=1
two=2
three=3
"""
    exofile = EXOFile()
    exofile.set("example", "one", "1")
    exofile.set("example", "two", "2")
    exofile.set("example", "three", "3")
    exofile.set("exedit", "one", "1")
    exofile.set("exedit", "two", "2")
    exofile.set("exedit", "three", "3")
    exofile.set("example2", "one", "1")
    exofile.set("example2", "two", "2")
    exofile.set("example2", "three", "3")
    self.assertEqual(exofile.dumps(), TEST_DATA)

  def test_exofile3 (self):
    TEST_DATA = """[exedit]
one=1
two=2
three=3
[example]
one=1
two=2
three=3
[example2]
one=1
two=2
three=3
"""
    exofile = EXOFile.loads(TEST_DATA)
    self.assertEqual(exofile.get("exedit", "one"), "1")
    self.assertEqual(exofile.get("exedit", "two"), "2")
    self.assertEqual(exofile.get("exedit", "three"), "3")
    self.assertEqual(exofile.get("example", "one"), "1")
    self.assertEqual(exofile.get("example", "two"), "2")
    self.assertEqual(exofile.get("example", "three"), "3")
    self.assertEqual(exofile.get("example2", "one"), "1")
    self.assertEqual(exofile.get("example2", "two"), "2")
    self.assertEqual(exofile.get("example2", "three"), "3")
    self.assertEqual(exofile.dumps(), TEST_DATA)

  def test_exofile4 (self):
    TEST_DATA = """[exedit]
_two=2
one=1
three=3
[example]
_two=2
one=1
three=3
[example2]
_two=2
one=1
three=3
"""
    exofile = EXOFile()
    exofile.set("example", "one", "1")
    exofile.set("example", "_two", "2")
    exofile.set("example", "three", "3")
    exofile.set("exedit", "one", "1")
    exofile.set("exedit", "_two", "2")
    exofile.set("exedit", "three", "3")
    exofile.set("example2", "one", "1")
    exofile.set("example2", "_two", "2")
    exofile.set("example2", "three", "3")
    self.assertEqual(exofile.dumps(), TEST_DATA)
