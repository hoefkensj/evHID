#!/usr/bin/env python
from dataclasses import dataclass, field
from os import supports_effective_ids

from pynput import keyboard
from contextlib import suppress
from typing import Literal
from enum import Enum
import time
class Callback():
	class Scope(Enum):
		GLOBAL = "global"
		APPLICATION = "application"
		LOCAL = "local"
	class Event(Enum):
		INIT = 'init'
		DOWN = 'down'
		UP   = 'up'

	scope: Literal["global", "application", "local"]  #
	event: Literal['down','up']
	match: keyboard.Key
	results:list
	_uservars: dict
	_userfn: callable
	_callfn: callable
	def __init__(s,*a,**k):
		s.scope : list[Callback.Scope]= [Callback.Scope.LOCAL,]
		s.event : list[Callback.Event] = [Callback.Event.DOWN,]
		s.match : keyboard.key = k.get('key')
		s.results=[]
		s._uservars=dict=k.get('vars',k.get('uservars',{}))
		s._userfn=callable = k.get('function',k.get('fn'))
		s.armed=callable =  None
		if len(s._uservars) > 0:
			s.uservars(s._uservars)
		s.__arm__()


	@property
	def function(__s):
		return __s._userfn
	@function.setter
	def function(__s,function):
		__s._userfn = function
		__s.__arm__()

	def __call__(s, *a,**k):
		s.results+=[s.armed(*a,**k)]

	def __arm__(s):
		s.armed=s._userfn(s)

	def uservars(s,**vars):
		for var in vars:
			setattr(s, var, vars.get(var))
		s.__arm__()
		return s._uservars


@dataclass(frozen=True)
class Key():
	__qualname__= keyboard.Key.__name__
	key:keyboard.Key
	name:str
	char:str
	value:int
	event:int


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

def FullKey(key,event):
	print('makefull',key)
	K=FKey(key)
	newkey= Key(K.key, K.name, K.char, K.value ,event)
	print(newkey.key,newkey.name,newkey.char,newkey.value,newkey.event)
	return newkey

@dataclass()
class FKey():
	_key:keyboard.Key
	_name:str=field(default='')
	_char:str=field(default='')
	_value:int=field(default=0)
	_down: bool=field(default=False)
	_up: bool=field(default=True)
	# _term:int=field(default=0)
	def __post_init__(__s):
		print('making FKEY',__s._key)
		for attr in ["char", "value" ,"name"]:
			setattr(__s,attr,getattr(__s._key,attr,None))
		missing=[name for  name in ("char", "value" ,"name")  if getattr(__s,f'_{name}',None) is None ]
		if "char" in missing:
			__s.char=getattr(__s._key, "name", str(__s._key))
		if 'value' in missing:
			__s._value=ord(getattr(__s._key, "char"))
		if 'name' in missing:
			__s.name = __s.char
		if __s.name=='space':
			setattr(__s,'_char',' ')
			setattr(__s,'_value', 0x20)
		__s.__qualname__ = __s._key.__name__
	@property
	def key(__s):     	return __s._key
	@key.setter
	def key(__s, key):  __s._key = key

	@property
	def value(__s):
		return __s._value
	@value.setter
	def value(__s,value):
		print(value)
		__s._value = int(str(value).strip('<').strip('>'))

	@property
	def char(__s):     return __s._char
	@char.setter
	def char(__s,char):	__s._char = char

	@property
	def name(__s): return __s._name
	@name.setter
	def name(__s,name): __s._name = name


