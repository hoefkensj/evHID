#!/usr/bin/env python
import atexit
import os
import shutil
import sys
import termios
import tty
from time import time_ns

from Clict import Clict

import evHID.Types.data
from evHID.Types.term.color import Colors
from evHID.Types.term.cursors import Cursor
from evHID.Types.term.size import Size


class Term():
	def __init__(__s,*a,**k):
		super().__init__()
		__s.pid=os.getpid()
		__s.ppid=os.getpid()
		
		__s.fd  = sys.stdin.fileno()
		
		__s.tty = os.ttyname(__s.fd)
		__s.setcbreak = tty.setcbreak
		__s.tcsetattr = termios.tcsetattr
		__s.tcgetattr = termios.tcgetattr
		__s.TCSAFLUSH = termios.TCSAFLUSH
		__s.ECHO			= termios.ECHO
		__s.ICANON    = termios.ICANON
		
		__s.live = __s.tcgetattr(__s.fd)
		__s.save = __s.tcgetattr(__s.fd)
		
		__s._mode='original'
		__s.mode   = __s.__mode__
		atexit.register(__s.mode,'normal')
		__s.cursor = Cursor(__s)
		__s.size   = Size(parent=__s)
		__s.color  = Colors(parent=__s)

	
	def echo(__s,enable):
		__s.live[3] &= ~__s.ICANON
		if enable:
			__s.live[3] |= __s.ICANON
		__s.update()

	def canonical(__s,enable):
		__s.live[3] &= ~__s.ECHO
		if enable:
			__s.live[3] |= __s.ECHO
		__s.update()
	def __mode__(__s,mode=None):
		def Normal():
			__s.cursor.show(True)
			__s.echo(True)
			__s.canonical(True)
			__s.tcsetattr(__s.fd, __s.TCSAFLUSH, __s.save)
			__s._mode='Normal'
		def Ctl():
			__s.cursor.show(False)
			__s.echo(False)
			__s.canonical(False)
			__s._mode='ctl'
		
		modi = {
			'ctl': Ctl,
			'normal': Normal
			}
		if mode is not None and mode != __s._mode:
			modi.get(mode)()
		return __s._mode
	
	def __size__(__s):
		def readTermSize(__s,dim='xy'):
			if __s.size.check==0:
				__s.size.check = time_ns()
			current={'x': (xy:=tuple([*shutil.get_terminal_size()]))[0],'y':xy[1],'xy':xy}
			if current != __s.size.current:
				__s.size.lastcheck=__s.size.check
				__s.size.check=time_ns()
				__s.size.changing=((__s.size.check- __s.size.lastcheck)*1e6<500)
				if not __s.size.changing:
					__s.size.history+=[__s.size.curent]
					__s.size.current=current
					__s.size.rows=current['y']
					__s.size.cols=current['x']
					evHID.Types.data.xy =current['xy']
					__s.size.changed=True
			else:
				__s.size.changed=False
			return current[dim]
		return readTermSize(__s)
		
	def update(__s):
		__s.tcsetattr(__s.fd, __s.TCSAFLUSH, __s.live)

	def ansi(__s, ansi, parser):
			__s.setcbreak(__s.fd, termios.TCSANOW)
			try:
				sys.stdout.write(ansi)
				sys.stdout.flush()
				result = parser()
			finally:
				__s.tcsetattr(__s.fd, termios.TCSAFLUSH, __s.live)
			return result
#
