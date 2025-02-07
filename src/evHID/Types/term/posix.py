#!/usr/bin/env python
import os
import termios
import tty
import atexit
import re
import sys
from time import time_ns
from shutil import get_terminal_size
from dataclasses import dataclass, field
from Clict import Clict



@dataclass(frozen=True, order=True)
class xy:
	x: int = field(default=1)
	y: int = field(default=1)

	@property
	def xy(self) -> tuple[int, int]:
		return (self.x, self.y)
@dataclass(frozen=True)
class color:
	R: int = field(default=0, metadata={"range": (0, 65535)})
	G: int = field(default=0, metadata={"range": (0, 65535)})
	B: int = field(default=0, metadata={"range": (0, 65535)})
	BIT: int = field(default=8, metadata={"set": (4, 8, 16, 32)})

	def __post_init__(self):
		for attr_name in ("R", "G", "B"):
			value = getattr(self, attr_name)
			if not isinstance(value, int):
				raise ValueError(f"{attr_name.upper()} must be an integer between 0 and 65535. Got {value}.")
		if not isinstance(getattr(self, "BIT"), int):
			raise ValueError(f"{attr_name.upper()} must be one of 4,8,16,32. Got {value}.")

	@property
	def RGB(self) -> tuple[int, int, int]:
		return (self.R, self.G, self.B)


class Cursor(Clict):
	def __init__(__s, term):
		super().__init__()
		__s.term = term
		__s.ansi.esc = '\x1b'
		__s.ansi.q = '[6n'
		__s.ansi.save = '[s'
		__s.ansi.load = '[u'
		__s.ansi.show = '[?25h'
		__s.ansi.hide = '[?25l'

		__s.re = re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R", re.VERBOSE)
		__s.position = __s.__update__
		__s.xy = lambda: __s.__update__()
		__s.history = [*(None,) * 64]
		__s.init = __s.__update__()

	def __update__(__s, get='XY'):
		def Parser():
			buf = ' '
			while buf[-1] != "R":
				buf += sys.stdin.read(1)
			# reading the actual values, but what if a keystroke appears while reading
			# from stdin? As dirty work around, getpos() returns if this fails: None
			try:
				groups = __s.re.search(buf).groupdict()
				result = {'X': int(groups['X']), 'Y': int(groups['Y'])}
			except AttributeError:
				result = None
			return result

		result = None
		timeout = Clict()
		timeout.limit = 500
		timeout.start = time_ns() // 1e6
		timeout.running = 0
		while not result:
			result = __s.term.ansi(''.join([__s.ansi.esc, __s.ansi.q]), Parser)
		__s.X = result['X']
		__s.Y = result['Y']
		__s.XY = tuple(result.values())
		__s.history = [__s.history[1:], __s.XY]
		return __s.get(get)

	def show(__s, state=True):
		if state:
			print('\x1b[?25h', end='', flush=True)
		else:
			__s.hide()

	def hide(__s, state=True):
		if state:
			print('\x1b[?25l', end='', flush=True)
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
	def __init__(__s, term, x=1, y=1):
		super().__init__()
		__s.term = term
		__s.position = __s.__update__
		__s.x = lambda: __s.__update__('X')
		__s.y = lambda: __s.__update__('Y')
		__s.xy = lambda: __s.__update__()
		__s.history = [*(None,) * 64]
		__s.controled = False
		__s.bound = True
		__s.frozen = False
		__s.init = __s.__update__()

	def freeze(__s, state=True):
		if state:
			__s.frozen = True
			__s.bind(False)
			__s.control(False)
		else:
			__s.frozen = False

	def __update__(__s, get='XY'):
		pass

	def show(__s, state=True):
		if state:
			print('\x1b[?25h', end='', flush=True)
		else:
			__s.hide()

	def hide(__s, state=True):
		if state:
			print('\x1b[?25l', end='', flush=True)
			atexit.register(__s.show)
		else:
			__s.show()


class Size():
	def __init__(__s, **k):
		__s.parent = None
		__s.getsize = get_terminal_size
		__s.time = None
		__s.last = None
		__s.xy = xy(1, 1)
		__s._tmp = xy(1, 1)
		__s.rows = 1
		__s.cols = 1
		__s.history = []
		__s.changed = False
		__s.changing = False
		__s.__kwargs__(**k)
		__s.init = __s.__update__()

	@property
	def rc(__s):
		__s.__update__()
		return (__s.cols, __s.rows)

	def __kwargs__(__s, **k):
		__s.term = k.get('parent')

	def __update__(__s):
		if __s.time is None:
			__s.last = time_ns()
		size = xy(*__s.getsize())
		if size != __s.xy:
			if size != __s._tmp:
				__s.changing = True
				__s._tmp = size
				__s._tmptime = time_ns()
			if size == __s._tmp:
				if (time_ns() - __s._tmptime) * 1e6 > 500:
					__s.changing = False
					__s.changed = True
					__s.history += [__s.xy]
					__s.xy = size
					__s.rows = __s.xy.y
					__s.cols = __s.xy.x
				else:
					__s._tmp = size
		if size == __s.xy:
			__s.changed = False

class Colors():
	def __init__(__s, **k):
		__s.parent = None
		__s.specs = {'fg': 10, 'bg': 11}
		__s._ansi = '\x1b]{spec};?\a'
		__s.__kwargs__(**k)
		__s.fg = color(255, 255, 255)
		__s.bg = color(0, 0, 0)
		__s.init = __s.__update__()

	def __kwargs__(__s, **k):
		__s.term = k.get('parent')

	@staticmethod
	def _ansiparser_():
		buf = ''
		try:
			for i in range(23):
				buf += sys.stdin.read(1)
			rgb = buf.split(':')[1].split('/')
			rgb = [int(i, base=16) for i in rgb]
			rgb = color(*rgb, 16)
		except Exception as E:
			print(E)
			rgb = None
		return rgb

	def __update__(__s):
		for ground in __s.specs:
			result = None
			while not result:
				result = __s.term.ansi(__s._ansi.format(spec=__s.specs[ground]), __s._ansiparser_)
			__s.__setattr__(ground, result)

		return {'fg': __s.fg, 'bg': __s.bg}

class Term():
	def __init__(__s,*a,**k):
		super().__init__()
		__s.pid       = os.getpid()
		__s.ppid      = os.getpid()
		
		__s.fd        = sys.stdin.fileno()
		__s.tty       = os.ttyname(__s.fd)

		__s.setcbreak = tty.setcbreak
		__s.tcsetattr = termios.tcsetattr
		__s.tcgetattr = termios.tcgetattr
		__s.TCSAFLUSH = termios.TCSAFLUSH
		__s.ECHO      = termios.ECHO
		__s.ICANON    = termios.ICANON
		__s.TCSANOW   = termios.TCSANOW
		
		__s.live      = __s.tcgetattr(__s.fd)
		__s.save      = __s.tcgetattr(__s.fd)
		
		__s._mode     = 0
		__s.mode      = __s.__mode__
		atexit.register(__s.mode,'normal')
		__s.cursor    = Cursor(__s)
		__s.size      = Size(parent=__s)
		__s.color     = Colors(parent=__s)

	
	def echo(__s,enable):

		__s.live[3] &= ~__s.ECHO
		if enable:
			__s.live[3] |= __s.ECHO
		__s.update()
	def canonical(__s,enable):
		__s.live[3] &= ~__s.ICANON
		if enable:
			__s.live[3] |= __s.ICANON
		__s.update()
	def __mode__(__s,mode=None):
		def Normal():
			__s.cursor.show(True)
			__s.echo(True)
			__s.canonical(True)
			__s.tcsetattr(__s.fd, __s.TCSAFLUSH, __s.save)
			__s._mode = nmodi.get('normal')

		def Ctl():
			__s.cursor.show(False)
			__s.echo(False)
			__s.canonical(False)
			__s._mode = nmodi.get('ctl')

		nmodi={'normal' : 1,'ctl': 2 }
		fmodi = {
			1   :  Normal,
			2   :  Ctl,
		}
		if mode is not None and mode != __s._mode:
			nmode=nmodi.get(mode)
			fmodi.get(nmode)()
		return __s._mode
		
	def update(__s):
		__s.tcsetattr(__s.fd, __s.TCSAFLUSH, __s.live)

	def ansi(__s, ansi, parser):
		__s.setcbreak(__s.fd, __s.TCSANOW)
		try:
			sys.stdout.write(ansi)
			sys.stdout.flush()
			result = parser()
		finally:
			__s.tcsetattr(__s.fd, termios.TCSAFLUSH, __s.live)
		return result
#
