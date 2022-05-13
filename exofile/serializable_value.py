
import re
import base64
from io import StringIO
from abc import ABC, abstractmethod, abstractclassmethod
from enum import IntEnum, unique, auto 
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

    """
    Color(color) => copy
    Color(red, green, blue) => new 
    """

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

  """
  Float(Float) => copy 
  Float(float, decimalpartdigits=1) => new 
  """

  def __new__ (cls, *args, decimalpartdigits=1, **kwargs):
    if args:
      if isinstance(args[0], Float):
        self = float.__new__(cls, *args, **kwargs)
        self.decimalpartdigits = args[0].decimalpartdigits
        return self 
      else:
        self = float.__new__(cls, *args, **kwargs)
        self.decimalpartdigits = decimalpartdigits
        return self 
    else:
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
      raise ValueError("Could not deserialize {} to {}.".format(text, cls)) #error

class Int (int, SerializableValue):

  def serialize (self):
    return "{:d}".format(self)

  @classmethod
  def deserialize (cls, text):
    if re.match(r"^-?\d+$", text):
      return cls(text)
    else:
      raise ValueError("Could not deserialize {} to {}.".format(text, cls)) #error

class Boolean (int, SerializableValue):

  def serialize (self):
    return "{:d}".format(self)

  @classmethod
  def deserialize (cls, text):
    if re.match(r"^[01]$", text):
      return cls(int(text))
    else:
      raise ValueError("Could not deserialize {} to {}.".format(text, cls)) #error

@unique
class TextType (IntEnum):

  STANDARD_TEXT = 0
  SHADOWED_TEXT = auto()
  SHADOWED_TEXT_THIN = auto()
  BORDERED_TEXT = auto()
  BORDERED_TEXT_THIN = auto()

@unique
class TextAlignment (IntEnum):

  ALIGN_LEFT_TOP = 0
  ALIGN_CENTER_TOP = auto()
  ALIGN_RIGHT_TOP = auto()
  ALIGN_LEFT_MIDDLE = auto()
  ALIGN_CENTER_MIDDLE = auto()
  ALIGN_RIGHT_MIDDLE = auto()
  ALIGN_LEFT_BOTTOM = auto()
  ALIGN_CENTER_BOTTOM = auto()
  ALIGN_RIGHT_BOTTOM = auto()
  ALIGN_VERTICAL_TOP_RIGHT = auto()
  ALIGN_VERTICAL_MIDDLE_RIGHT = auto()
  ALIGN_VERTICAL_BOTTOM_RIGHT = auto()
  ALIGN_VERTICAL_TOP_CENTER = auto()
  ALIGN_VERTICAL_MIDDLE_CENTER = auto()
  ALIGN_VERTICAL_BOTTOM_CENTER = auto()
  ALIGN_VERTICAL_TOP_LEFT = auto()
  ALIGN_VERTICAL_MIDDLE_LEFT = auto()
  ALIGN_VERTICAL_BOTTOM_LEFT = auto()

@unique
class TrackBarType (IntEnum):

  NONE = 0
  LINEAR = 1
  ACCELERATION = 7 
  CURVE = 2
  TELEPORTATION = 3
  IGNORE_MIDPOINT = 4
  MOVE_CERTAIN_AMOUNT = 5 #移動量指定
  RANDOM = 6
  REPETITION = 8

class TrackBarRange (SerializableValue):

  type = None 
  type_pattern = None 

  def __init__ (self, *args, **kwargs):

    """
    TrackBarRange(TrackBarRange) => copy 
    TrackBarRange(TrackBarRange.type) => new 
    TrackBarRange(start, end, TrackBarType, accelerate=False, decelerate=False, parameter=None) => new 
    """

    if len(args) == 1:
      value, = args 
      if isinstance(value, TrackBarRange):
        self.start = value.start
        self.end = value.end
        self.trackbartype = value.trackbartype
        self.accelerate = value.accelerate
        self.decelerate = value.decelerate
        self.parameter = value.parameter
      else:
        self.start = self.type(value)
        self.end = self.type(value)
        self.trackbartype = TrackBarType.NONE
        self.accelerate = False
        self.decelerate = False
        self.parameter = None 
    elif len(args) == 3:
      start, end, trackbartype = args
      self.start = self.type(start)
      self.end = self.type(end)
      self.trackbartype = trackbartype
      self.accelerate = kwargs.get("accelerate", False)
      self.decelerate = kwargs.get("decelerate", False)
      self.parameter = kwargs.get("parameter", None)
    else:
      raise ValueError("Argument count must be 1 or 3.")

  @classmethod
  def parse_flags (cls, flags):
    trackid = flags & 0b0001111
    accelerate = 0 < flags & 0b1000000
    decelerate = 0 < flags & 0b0100000
    return trackid, accelerate, decelerate

  @classmethod
  def unparse_flags (cls, trackid, accelerate, decelerate):
    accelerateflag = 0b1000000 if accelerate else 0
    decelerateflag = 0b0100000 if decelerate else 0
    return trackid | accelerateflag | decelerateflag

  def serialize (self):
    with StringIO() as buffer:
      if self.trackbartype == TrackBarType.NONE:
        buffer.write(serialize_value(self.start))
        return buffer.getvalue()
      else:
        buffer.write(serialize_value(self.start))
        buffer.write(",")
        buffer.write(serialize_value(self.end))
        buffer.write(",")
        if isinstance(self.trackbartype, str):
          flags = self.unparse_flags(0b1111, self.accelerate, self.decelerate)
          buffer.write("{:d}@{:s}".format(flags, self.trackbartype))
        elif isinstance(self.trackbartype, int):
          flags = self.unparse_flags(self.trackbartype, self.accelerate, self.decelerate)
          buffer.write("{:d}".format(flags))
        else:
          raise ValueError()
        if self.parameter is not None:
          buffer.write(",")
          buffer.write(serialize_value(self.parameter))
        return buffer.getvalue()

  @classmethod
  def deserialize (cls, text):
    matchresult = re.match("({}),({}),(\\d+)@(.+),(\\d+)$".format(cls.type_pattern, cls.type_pattern), text)
    if matchresult:
      start, end, idandflags, trackname, parameter = matchresult.groups()
      trackid, accelerate, decelerate = cls.parse_flags(int(idandflags))
      return cls(cls.type.deserialize(start), cls.type.deserialize(end), trackname, accelerate=accelerate, decelerate=decelerate, parameter=int(parameter))
    matchresult = re.match("({}),({}),(\\d+),(\\d+)$".format(cls.type_pattern, cls.type_pattern), text)
    if matchresult:
      start, end, idandflags, parameter = matchresult.groups()
      trackid, accelerate, decelerate = cls.parse_flags(int(idandflags))
      return cls(cls.type.deserialize(start), cls.type.deserialize(end), int(trackid), accelerate=accelerate, decelerate=decelerate, parameter=int(parameter))
    matchresult = re.match("({}),({}),(\\d+)@(.+)$".format(cls.type_pattern, cls.type_pattern), text)
    if matchresult:
      start, end, idandflags, trackname = matchresult.groups()
      trackid, accelerate, decelerate = cls.parse_flags(int(idandflags))
      return cls(cls.type.deserialize(start), cls.type.deserialize(end), trackname, accelerate=accelerate, decelerate=decelerate)
    matchresult = re.match("({}),({}),(\\d+)$".format(cls.type_pattern, cls.type_pattern), text)
    if matchresult:
      start, end, idandflags = matchresult.groups()
      trackid, accelerate, decelerate = cls.parse_flags(int(idandflags))
      return cls(cls.type.deserialize(start), cls.type.deserialize(end), int(trackid), accelerate=accelerate, decelerate=decelerate)
    matchresult = re.match("({})$".format(cls.type_pattern), text)
    if matchresult:
      value, = matchresult.groups()
      return cls(cls.type.deserialize(value))
    raise ValueError("Could not deserialize text {} to {}.".format(text, cls)) #error

class IntTrackBarRange (TrackBarRange):

  type = Int
  type_pattern = "-?\\d+"

class FloatTrackBarRange (TrackBarRange):

  type = Float
  type_pattern = "-?\\d+\\.\\d+"

@unique 
class ShapeType (IntEnum):

  CIRCLE = 1
  SQUARE = 2
  TRIANGLE = 3
  PENTAGON = 4
  HEXAGON = 5
  STAR = 6
  FILE = 0 #これを選択した場合nameパラメータの先頭に*を付与しなければなりません。

class ShapeName (str):

  def serialize (self):
    if self:
      return "*" + self
    else:
      return ""

  @classmethod
  def deserialize (cls, text):
    if text:
      if text.startswith("*"):
        return cls(text[1:])
      else:
        raise ValueError("{} must starts with *.".format(text)) #error 
    else:
      return cls("")
