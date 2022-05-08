
import re 
from collections import OrderedDict
from .serializable import Serializable
from .serializable_value import serialize_value
from .mutable_mapping_proxyer import MutableMappingProxyer

class EXOFile (Serializable, MutableMappingProxyer):

  def __init__ (self):
    self.sections = OrderedDict()

  def get_object_section_ids (self):
    sectionids = dict()
    for sectionid, section in self.items():
      matchresult = re.match(r"(\d+)$", sectionid) #object.
      if matchresult:
        objid, = matchresult.groups()
        sectionids.setdefault(objid, list())
      matchresult = re.match(r"(\d+)\.(\d+)$", sectionid) #object param.
      if matchresult:
        objid, objparamid = matchresult.groups()
        sectionids.setdefault(objid, list())
        sectionids[objid].append(sectionid)
    return { objid: sorted(objparamids) for objid, objparamids in sectionids.items() }

  def set (self, sectionid, key, value):
    if sectionid not in self.sections:
      self.sections[sectionid] = Section()
    self.sections[sectionid][key] = value

  def get (self, sectionid, key, default=None):
    if sectionid not in self.sections:
      return default
    return self.sections[sectionid].get(key, default)

  def remove (self, sectionid, key):
    del self.sections[sectionid][key]
    if not self.sections[sectionid]:
      del self.sections[sectionid] #delete section automatically if it's empty.

  def remove_section (self, sectionid):
    del self.sections[sectionid]

  def contains (self, sectionid, key):
    return sectionid in self.sections and key in self.sections[sectionid]

  def contains_section (self, sectionid):
    return sectionid in self.sections

  def get_proxy_mutable_mapping (self):
    if "exedit" in self.sections:
      self.sections.move_to_end("exedit", last=False)
    return self.sections

  @classmethod
  def load (cls, stream):
    exofile = EXOFile()
    section = Section() 
    for line in stream:
      matchresult = re.match(r"\[(.*)\]", line)
      if matchresult:
        sectionid, = matchresult.groups()
        section = Section()
        exofile[sectionid] = section
      matchresult = re.match(r"(.*?)=(.*)", line)
      if matchresult:
        key, value = matchresult.groups()
        section[key] = value
    return exofile

  def dump (self, stream):
    for sectionid, section in self.items():
      stream.write("[{}]\n".format(sectionid))
      for key, value in section.items():
        serializedvalue = serialize_value(value)
        stream.write("{}={}\n".format(key, serializedvalue))

class Section (MutableMappingProxyer):

  def __init__ (self):
    self.params = OrderedDict()

  def get_proxy_mutable_mapping (self):
    underbarkeys = [ key for key in self.params.keys() if key.startswith("_") ]
    for underbarkey in underbarkeys:
      self.params.move_to_end(underbarkey, last=False)
    if "_name" in self.params:
      self.params.move_to_end("_name", last=False)
    return self.params
