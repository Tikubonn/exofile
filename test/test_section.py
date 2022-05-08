
from exofile import Section
from unittest import TestCase 

class TestSection (TestCase):

  def test_section (self):
    section = Section()
    section["one"] = 1
    section["two"] = 2
    section["three"] = 3
    section["_name"] = 4
    section["_zero"] = 0
    sectionitems = iter(section.items())
    self.assertEqual(next(sectionitems), ("_name", 4))
    self.assertEqual(next(sectionitems), ("_zero", 0))
    self.assertEqual(next(sectionitems), ("one", 1))
    self.assertEqual(next(sectionitems), ("two", 2))
    self.assertEqual(next(sectionitems), ("three", 3))
    with self.assertRaises(StopIteration):
      next(sectionitems)

  def test_section2 (self):
    section = Section()
    section["one"] = 1
    section["two"] = 2
    section["three"] = 3
    del section["one"]
    del section["two"]
    del section["three"]
    sectionitems = iter(section.items())
    with self.assertRaises(StopIteration):
      next(sectionitems)
