#!/usr/bin/env python
from dataclasses import dataclass, field
from pynput import keyboard
from contextlib import suppress
class Callback():
	def __init__(s,*a,**k):
		s.scope=None
		s.event=None
		s.vars={}
		s.func=None
		s.scope=None
		s.vars=None
		s.key=None
		s.__kwargs__(**k)
	def __kwargs__(s,**k):
		s.scope=k.get('scope','global')
		s.event=k.get('event')
		s.vars=k.get('vars',{})
		for var in s.vars:
			setattr(s,var,s.vars[var])
		fn=k.get('fn')
		s.func=fn(s)
	def __call__(s, key):
		s.key=key
		s.fn()

	def fn(s):
		s.func(s.key)

@dataclass(frozen=True)
class Key():
	__qualname__= keyboard.Key.__name__
	key:keyboard.Key
	name:str
	char:str
	value:int
	
	def __str__(__s):
		return str(__s.key).strip("'")
	
	def __repr__(__s):
		return f'key({__s.name},{__s.value},\'{__s.char}\')'
	
	def __int__(__s):
		return __s.value
	
	def __eq__(__s, other):
		r = (other in [__s.key, __s.name, __s.char, __s.value, str(__s.value), str(__s.key), str(__s.char)])
		if r is False:
			for s in [str, chr, repr]:
				with suppress(Exception):
					r = (__s._char == s(other))
				if r is True:
					break
		
		if r is False:
			with suppress(Exception):
				r = __s._value == other.value
		if r is False:
			with suppress(Exception):
				r = __s._value == str(other.value)
		return r
	
def FullKey(key):
	K=FKey(key)
	newkey= Key(K.key, K.name, K.char, K.value)
	return newkey

@dataclass()
class FKey():
	__qualname__ = keyboard.Key.__name__
	_key:keyboard.Key
	_name:str=field(default='')
	_char:str=field(default='')
	_value:int=field(default=0)
	# _term:int=field(default=0)
	def __post_init__(__s):
		for attr_name in ("char", "value" ,"name"):
			attr = getattr(__s._key, attr_name,None)
			if attr_name=="char":
				if attr is None:
					attr=getattr(__s._key, "name",str(__s._key))
				attr_name=f'_{attr_name}'
			elif attr_name == "value":
				if attr is None:
					attr=ord(getattr(__s._key, "char"))
				attr_name=f'_{attr_name}'
			elif attr_name=="name":
				if attr is None or attr=='':
					attr = __s.char
				attr_name=f'_{attr_name}'

			setattr(__s, attr_name, attr)
		if __s._name=='space':
			setattr(__s,'_char',' ')
			setattr(__s,'_value', 0x20)




	@property
	def key(__s):     	return __s._key
	@key.setter
	def key(__s, key):  __s._key = key
	
	@property
	def value(__s):    return __s._value
	@value.setter
	def value(__s,value):		__s._value = value
	
	@property
	def char(__s):     return __s._char
	@char.setter
	def char(__s,char):	__s._char = char
	
	@property
	def name(__s): return __s._name
	@name.setter
	def name(__s,name): __s._name = name
	
	# @property
	# def term(__s): return __s._term
	
	# @term.setter
	# def term(__s,term):
	# 	with suppress(Exception):
	# 		__s._term = len(str(__s).strip("'"))

	


	



	




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
