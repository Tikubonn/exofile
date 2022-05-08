
from io import StringIO
from abc import ABC, abstractmethod, abstractclassmethod

class Serializable (ABC):

  @abstractclassmethod
  def load (cls, stream):
    pass

  @abstractmethod
  def dump (self, stream):
    pass

  @classmethod
  def loads (cls, text):
    with StringIO(text) as stream:
      return cls.load(stream)

  def dumps (self):
    with StringIO() as stream:
      self.dump(stream)
      return stream.getvalue()
