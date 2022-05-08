
import re
import base64
from io import StringIO
from abc import ABC, abstractmethod, abstractclassmethod
from collections import OrderedDict

class SerializableValue (ABC):

  @abstractmethod
  def serialize (self) -> str:
    pass

  @abstractclassmethod
  def deserialize (cls, text: str) -> "SerializableValue":
    pass

def serialize_value (value):
  if isinstance(value, SerializableValue):
    return value.serialize()    
  else:
    return str(value)

class Params (OrderedDict, SerializableValue):

  def serialize (self):
    with StringIO() as buffer:
      for key, value in self.items():
        buffer.write('{}="{}";'.format(key, serialize_value(value)))
      return buffer.getvalue()

  @classmethod
  def deserialize (cls, text):
    params = Params()
    tx = text
    while tx:
      matchresult = re.match(r'(.+?)="(.+?)";', tx)
      if matchresult:
        start, end = matchresult.span()
        key, value = matchresult.groups()
        params[key] = value
        tx = tx[end:]
      else:
        break
    return params

class Color (SerializableValue):

  def __init__ (self, *args):
    if len(args) == 1:
      color, = args
      if isinstance(color, Color):
        self.red = color.red
        self.green = color.green
        self.blue = color.blue
      else:
        raise TypeError("First argument of {} is not a Color instance.".format(color)) #error
    elif len(args) == 3:
      red, green, blue = args
      self.red = red
      self.green = green
      self.blue = blue
    else:
      raise ValueError("Initial arguments length must be 1 or 3.") #error

  def __eq__ (self, color):
    return (
      isinstance(color, Color) and 
      self.red == color.red and 
      self.green == color.green and 
      self.blue == color.blue
    )

  def serialize (self):
    if (0x00 <= self.red <= 0xff 
        and 0x00 <= self.green <= 0xff 
        and 0x00 <= self.blue <= 0xff):
      return "{:02x}{:02x}{:02x}".format(self.red, self.green, self.blue)
    else:
      raise ValueError()

  @classmethod
  def deserialize (cls, text:str) -> "Color":
    if len(text) == 6:
      red = int(text[0:2], 16)
      green = int(text[2:4], 16)
      blue = int(text[4:6], 16)
      return cls(red, green, blue)
    else:
      raise ValueError("Serialized text's length must be 6 like as 0088ff.") #error

class Text (str, SerializableValue):

  MAX_SERIALIZED_LENGTH = 4096
  MAX_DESERIALIZED_LENGTH = 4096 // 2 // 2 - 1

  def serialize (self):
    if len(self) <= self.MAX_DESERIALIZED_LENGTH:
      encoded = self.encode("utf-16-le")
      b16encoded = base64.b16encode(encoded).decode("ascii").lower()
      padding = "0" * (self.MAX_SERIALIZED_LENGTH - len(b16encoded))
      return b16encoded + padding
    else:
      raise ValueError("Length of text for serializing is over {:d}.".format(self.MAX_DESERIALIZED_LENGTH)) #error

  @classmethod
  def deserialize (cls, text):
    if len(text) == cls.MAX_SERIALIZED_LENGTH:
      b16decoded = base64.b16decode(text, casefold=True)
      decoded = b16decoded.decode("utf-16-le")
      foundnulindex = decoded.find("\0")
      if 0 <= foundnulindex:
        return Text(decoded[:foundnulindex])
      else:
        raise ValueError("Could not find NUL character into deserialized text.") #error
    else:
      raise ValueError("Serialized text chunk's length must be 4096.") #error

class String (str, SerializableValue):

  def serialize (self):
    return self 

  @classmethod
  def deserialize (cls, text):
    return cls(text)

class Float (float, SerializableValue):

  def __new__ (cls, *args, decimalpartdigits=1, **kwargs):
    self = float.__new__(cls, *args, **kwargs)
    self.decimalpartdigits = decimalpartdigits
    return self 

  def serialize (self):
    fm = "{:.0" + format(self.decimalpartdigits, "d") + "f}"
    return fm.format(self)

  @classmethod
  def deserialize (cls, text):
    matchresult = re.match(r"^(-?)(\d+)\.(\d+)$", text)
    if matchresult:
      signpart, intpart, decimalpart = matchresult.groups()
      return cls(text, decimalpartdigits=len(decimalpart))
    else:
      raise ValueError()

class Int (int, SerializableValue):

  def serialize (self):
    return "{:d}".format(self)

  @classmethod
  def deserialize (cls, text):
    if re.match(r"^-?\d+$", text):
      return cls(text)
    else:
      raise ValueError()

class Boolean (int, SerializableValue):

  def serialize (self):
    return "{:d}".format(self)

  @classmethod
  def deserialize (cls, text):
    if re.match(r"^[01]$", text):
      return cls(int(text))
    else:
      raise ValueError()
