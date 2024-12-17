#!/usr/bin/env python
from dataclasses import dataclass, field

from pynput import keyboard


@dataclass()
class fullkey():
	__qualname__ = keyboard.Key.__name__
	_key:keyboard.Key
	name:str=field(default='')
	_char:str=field(default='')
	_value:int=field(default=0)
	def __post_init__(__s):
		for attr_name in ("name","char", "value" ):
			attr = getattr(__s._key, attr_name,None)
			if attr_name=="char":
				if attr is None:
					attr=getattr(__s._key, "name",str(__s._key))
				attr_name=f'_{attr_name}'
			elif attr_name == "value":
				if attr is None:
					attr=ord(getattr(__s._key, "char"))
				attr_name=f'_{attr_name}'
			setattr(__s, attr_name, attr)
		if __s.name=='space':
			setattr(__s,'_char',' ')
			setattr(__s,'_value', 0x20)
			
			
	@property
	def value(__s):
		return f'<{__s._value}>'
	@property
	def char(__s):
		return __s._char
	
	def __str__(__s):
		return str(__s._key)
	def __repr__(__s):
		return f'key({__s.name},{__s.value},\'{__s.char}\')'
	def __int__(__s):
		return __s._value
	
	def __eq__(__s, other):
		
		result=False
		if __s._key == other:
			result=True
		elif __s.name == other:
			result=True
		elif __s.char == other:
			result=True
		elif __s.value == other:
			result=True
		elif __s._char == str(other):
			result=True
		elif __s._value == other:
			result=True
		else:
			if (vother:=getattr(other,'value',None )) is not None:
				if __s.value == vother:
					result = True
				elif __s._value == vother:
					result = True
		return result


@dataclass(frozen=True)
class color:
	R:   int = field(default=0, metadata={"range": (0, 65535)})
	G:   int = field(default=0, metadata={"range": (0, 65535)})
	B:   int = field(default=0, metadata={"range": (0, 65535)})
	BIT: int = field(default=8, metadata={"set": (4, 8,16,32)})
	def __post_init__(self):
		for attr_name in ("R", "G", "B"):
			value = getattr(self, attr_name)
			if not isinstance(value, int) :
				raise ValueError(f"{attr_name.upper()} must be an integer between 0 and 65535. Got {value}.")
		if not isinstance(getattr(self,"BIT"),int):
			raise ValueError(f"{attr_name.upper()} must be one of 4,8,16,32. Got {value}.")
	
	@property
	def RGB(self) -> tuple[int, int, int]:
		return (self.R, self.G, self.B)


@dataclass(frozen=True,order=True)
class xy:
	x:   int = field(default=1)
	y:   int = field(default=1)
	@property
	def xy(self) -> tuple[int, int]:
		return (self.x, self.y)
