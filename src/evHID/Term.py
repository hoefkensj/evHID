#!/usr/bin/env python
import atexit
import os
import sys
import termios
import re
import tty
import shutil
from Clict import Clict

# # Open the new pseudoterminal for reading
# new_stdin_fd = os.open(new_pts, os.O_RDONLY)
#
# # Duplicate the new pseudoterminal's file descriptor onto sys.stdin
# os.dup2(new_stdin_fd, sys.stdin.fileno())
# #
def ansi(term,ansi, parser):
	tty.setcbreak(term.fd, termios.TCSANOW)
	try:
		sys.stdout.write(ansi)
		sys.stdout.flush()
		result = parser()
	finally:
		termios.tcsetattr(term.fd, termios.TCSAFLUSH, term.live)
	return result
#

# def info():
#
# 	def pos_cursor():
# 		def Parser():
# 				buf=''
# 				while buf[-1] != "R":
# 					buf += sys.stdin.read(1)
# 				# reading the actual values, but what if a keystroke appears while reading
# 				# from stdin? As dirty work around, if this fails returns None
# 				try:
# 					groups=rexy.search(buf).groupdict()
# 					result={'X': groups['X'],'Y':groups['Y']}
# 				except AttributeError:
# 					result = None
# 				return result
# 		rexy = re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R", re.VERBOSE)
# 		ansiesc='\x1b[6n'
# 		result=None
# 		while not result:
# 			result=ansi(ansiesc,Parser)
# 		return result
#
# 	def bg_color():
# 		def Parser():
# 			buf = ''
# 			for i in range(23):
# 				buf += sys.stdin.read(1)
# 			rgb=buf.split(':')[1].split('/')
# 			rgb={c:int(i,base=16) for c,i in zip([*'RGB'],rgb)}
# 			tot=[*rgb.values()]
# 			tot=sum(tot)
# 			rgb['avg']=(tot/3)/65535
# 			rgb['max']=65535
# 			return rgb
# 		ansiesc='\x1b]11;?\a'
# 		return ansi(ansiesc,Parser)
#
# 	def size():
# 		s= {'C'  :(shutil.get_terminal_size()[0]),
# 		 'L' : (shutil.get_terminal_size()[1])}
# 		return s
#
# 	term={'stdout':'not a tty'}
# 	if sys.stdout.isatty():
# 		term=Clict()
# 		term.size={**size()}
# 		term.cursor={**pos_cursor()}
# 		term.color.bg={**bg_color()}
# 		term.get_size=size
# 		term.get_cursor=pos_cursor
# 		term.get_color.bg=bg_color
# 	return term	def __cursor_hide__(__s):
# 		print('\x1b[?25l',end='',flush=True)
# 		atexit.register(__s.cursor.show)
# 	def __cursor_show__(__s):
# 		print('\x1b[?25h',end='',flush=True)
# 	def __cursor_pos_get__(__s):
# 		def Parser():
# 			buf=' '
# 			while buf[-1] != "R":
# 				buf += sys.stdin.read(1)
# 			# reading the actual values, but what if a keystroke appears while reading
# 			# from stdin? As dirty work around, getpos() returns if this fails: None
# 			try:
# 				groups=rexy.search(buf).groupdict()
# 				result={'X': groups['X'],'Y':groups['Y']}
# 			except AttributeError:
# 				result=None
# 			return result
# 		rexy= re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R",re.VERBOSE)
# 		ansiesc='\x1b[6n'
# 		result=None
# 		while not result:
# 			result=ansi(ansiesc,Parser)
# 		return result

class Cursor(Clict):
	def __init__(__s,term):
		super().__init__()
		__s.term=term
		__s.ansi='\x1b[6n'
		__s.re=re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R",re.VERBOSE)
		__s.loc=__s.__update__
		__s.x=lambda :__s.__update__('X')
		__s.y=lambda : __s.__update__('Y')
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
				result={'X': groups['X'],'Y':groups['Y']}
			except AttributeError:
				result=None
			return result
		result=None
		while not result:
			result=ansi(__s.term,__s.ansi,Parser)
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

class Color(Clict):
	def __init__(__s,term,spec=None):
		specs={'fg': 10 , 'bg': 11}
		super().__init__()
		__s.term=term
		__s.ansi=f'\x1b]{specs.get(spec,10)};?\a'
		__s.r=lambda :__s.__update__('R')
		__s.g=lambda : __s.__update__('G')
		__s.b=lambda : __s.__update__('B')
		__s.rgb=lambda : __s.__update__()

		__s.init=__s.__update__()

	def __update__(__s,get='RGB'):
		def Parser():
			buf = ''
			try:
				for i in range(23):
					buf += sys.stdin.read(1)
				rgb=buf.split(':')[1].split('/')
				rgb={c:int(i,base=16) for c,i in zip([*'RGB'],rgb)}
				rgb['N']=65536
			except Exception as E:
				print(E)
				rgb=None
			return rgb
		result=None
		while not result:
			result = ansi(__s.term, __s.ansi, Parser)
		__s.R=result['R']
		__s.G=result['G']
		__s.B=result['B']
		__s.RGB=tuple(result.values())
		return result


class Term(Clict):
	def __init__(__s,*a,**k):
		super().__init__()
		__s.pid=os.getpid()
		__s.ppid=os.getpid()
		__s.fd  = sys.stdin.fileno()
		__s.tty = os.ttyname(__s.fd)
		__s.live = termios.tcgetattr(__s.fd)
		__s.save = termios.tcgetattr(__s.fd)
		__s.normal =lambda: termios.tcsetattr(__s.fd, termios.TCSAFLUSH, __s.save)
		atexit.register(__s.normal)
		__s.cursor = Cursor(__s)
		__s.color.fg = Color(__s,'fg')
		__s.color.bg = Color(__s,'bg')

	def echo(__s,enable):
		__s.live[3] &= ~termios.ICANON
		if enable:
			__s.live[3] |= termios.ICANON
		__s.update()

	def canonical(__s,enable):
		__s.live[3] &= ~termios.ECHO
		if enable:
			__s.live[3] |= termios.ECHO
		__s.update()
	def mode(__s,mode):
		def normal():
			__s.cursor.show(True)
			__s.echo(True)
			__s.canonical(True)
			__s.normal()
		def Ctl():
			__s.cursor.show(False)
			__s.echo(False)
			__s.canonical(False)

		if mode=='ctl':
			Ctl()
		elif mode=='normal':
			normal()

	def update(__s):
		termios.tcsetattr(__s.fd, termios.TCSAFLUSH, __s.live)




if __name__ == '__main__' :

		T = Term()
		print(T.cursor.x())
		print(T.cursor.Y)
		print(T.cursor.X)
		print(T.cursor.y())
		print(T.color.bg.rgb())
