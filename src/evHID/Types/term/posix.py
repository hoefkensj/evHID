#!/usr/bin/env python
import atexit
import os
import shutil
import sys
import termios
import tty
from time import time_ns

import evHID.Types.data
from evHID.Types.term.color import Colors
from evHID.Types.term.cursors import Cursor
from evHID.Types.term.size import Size



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
