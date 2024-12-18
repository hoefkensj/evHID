#!/usr/bin/env python
import atexit
import re
import sys
from time import time_ns

from Clict import Clict



class Cursor(Clict):
	def __init__(__s,term):
		super().__init__()
		__s.term=term
		__s.ansi.esc='\x1b'
		__s.ansi.q='[6n'
		__s.ansi.save='[s'
		__s.ansi.load='[u'
		__s.ansi.show='[?25h'
		__s.ansi.hide='[?25l'
		
		__s.re=re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R",re.VERBOSE)
		__s.position=__s.__update__
		__s.xy=lambda : __s.__update__()
		__s.history=[*(None,)*64]
		__s.init=__s.__update__()

	def __update__(__s,get='XY'):
		def Parser():
			buf=' '
			while buf[-1] != "R":
				buf += sys.stdin.read(1)
			# reading the actual values, but what if a keystroke appears while reading
			# from stdin? As dirty work around, getpos() returns if this fails: None
			try:
				groups=__s.re.search(buf).groupdict()
				result={'X': int(groups['X']),'Y':int(groups['Y'])}
			except AttributeError:
				result=None
			return result
		result=None
		timeout=Clict()
		timeout.limit=500
		timeout.start=time_ns()//1e6
		timeout.running=0
		while not result:
			result=__s.term.ansi(''.join([__s.ansi.esc,__s.ansi.q]),Parser)
		__s.X=result['X']
		__s.Y=result['Y']
		__s.XY=tuple(result.values())
		__s.history=[__s.history[1:],__s.XY]
		return __s.get(get)
	def show(__s,state=True):
		if state:
			print('\x1b[?25h',end='',flush=True)
		else:
			__s.hide()
	def hide(__s,state=True):
		if state:
			print('\x1b[?25l',end='',flush=True)
			atexit.register(__s.show)
		else:
			__s.show()

	@property
	def x(__s):
		__s.__update__('X')
		return __s.X
	@property
	def y(__s):
		__s.__update__('Y')
		return __s.Y
		
		
class vCursor(Cursor):
	def __init__(__s,term,x=1,y=1):
		super().__init__()
		__s.term=term
		__s.position=__s.__update__
		__s.x=lambda :__s.__update__('X')
		__s.y=lambda : __s.__update__('Y')
		__s.xy=lambda : __s.__update__()
		__s.history=[*(None,)*64]
		__s.controled=False
		__s.bound=True
		__s.frozen=False
		__s.init=__s.__update__()
		
	
	def freeze(__s,state=True):
		if state:
			__s.frozen=True
			__s.bind(False)
			__s.control(False)
		else :
			__s.frozen=False
	
	def __update__(__s,get='XY'):
		pass
	def show(__s,state=True):
		if state:
			print('\x1b[?25h',end='',flush=True)
		else:
			__s.hide()
	def hide(__s,state=True):
		if state:
			print('\x1b[?25l',end='',flush=True)
			atexit.register(__s.show)
		else:
			__s.show()
