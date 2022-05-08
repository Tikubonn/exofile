
from abc import abstractmethod
from collections.abc import MutableMapping 

class MutableMappingProxyer (MutableMapping):

  @abstractmethod
  def get_proxy_mutable_mapping (self):
    pass

  def __getitem__ (self, *args, **kwargs): 
    return self.get_proxy_mutable_mapping().__getitem__(*args, **kwargs) 

  def __setitem__ (self, *args, **kwargs): 
    return self.get_proxy_mutable_mapping().__setitem__(*args, **kwargs) 

  def __delitem__ (self, *args, **kwargs): 
    return self.get_proxy_mutable_mapping().__delitem__(*args, **kwargs) 

  def __iter__ (self, *args, **kwargs): 
    return self.get_proxy_mutable_mapping().__iter__(*args, **kwargs) 

  def __len__ (self, *args, **kwargs): 
    return self.get_proxy_mutable_mapping().__len__(*args, **kwargs)

  def pop (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().pop(*args, **kwargs) 

  def popitem (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().popitem(*args, **kwargs) 

  def clear (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().clear(*args, **kwargs) 

  def update (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().update(*args, **kwargs) 

  def setdefault (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().setdefault(*args, **kwargs)

  def __contains__ (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().__contains__(*args, **kwargs) 

  def keys (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().keys(*args, **kwargs) 

  def items (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().items(*args, **kwargs) 

  def values (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().values(*args, **kwargs) 

  def get (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().get(*args, **kwargs) 

  def __eq__ (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().__eq__(*args, **kwargs) 

  def __ne__ (self, *args, **kwargs): #override for avoid mutation error on iteration.
    return self.get_proxy_mutable_mapping().__ne__(*args, **kwargs)
