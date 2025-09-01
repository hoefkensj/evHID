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
from enum import Enum
from Clict import Clict
from collections import namedtuple
from evHID.Types.coord import Coord2D as Coord



# Indices for termios list.
IFLAG = 0
OFLAG = 1
CFLAG = 2
LFLAG = 3
ISPEED = 4
OSPEED = 5
CC = 6


class TermAttrs():
	def __init__(s):
		s.stack=[]
		s.init=None
		s.staged=None
		s.active=None
	def stage(s):
		s.staged=list(s.active)
	def update(s,new):
		s.stack+=[s.staged]
		s.staged=None
		s.active=new


class Term():
	def __init__(s,*a,**k):
		# super().__init__()
		s.pid       = os.getpid()
		s.ppid      = os.getpid()
		
		s.fd        = sys.stdin.fileno()
		s.tty       = os.ttyname(s.fd)

		s.TCSAFLUSH = termios.TCSAFLUSH
		s.ECHO      = termios.ECHO
		s.ICANON    = termios.ICANON
		s.TCSANOW   = termios.TCSANOW

		s.attrs     = TermAttrs()


		s.attrs.active =  s.tcgetattr()
		s.attrs.init   =  list(s.attrs.active)
		s.attrs.stack += [list(s.attrs.active)]

		s._mode     = 0
		s.mode      = s.__mode__
		atexit.register(s.mode,'normal')
		s.cursor    = Cursor(s)
		s.vcursors  = {0:vCursor(s,s.cursor)}
		s.size      = Size(parent=s)
		s.color     = Colors(parent=s)


	def tcgetattr(s):
		return termios.tcgetattr(s.fd)

	def tcsetattr(s,when,attr):
		termios.tcsetattr(s.fd,when,attr)

	def setraw(s, when=TCSAFLUSH):
		"""Put terminal into raw mode."""
		s.attr.stage()
		# Clear all POSIX.1-2017 input mode flags.
		# See chapter 11 "General Terminal Interface"
		# of POSIX.1-2017 Base Definitions.
		s.attr.staged[IFLAG] &= ~( IGNBRK | BRKINT | IGNPAR | PARMRK | INPCK | ISTRIP | INLCR | IGNCR | ICRNL | IXON | IXANY | IXOFF)
		# Do not post-process output.
		s.attr.staged[OFLAG] &= ~OPOST
		# Disable parity generation and detection; clear character size mask;
		# let character size be 8 bits.
		s.attr.staged[CFLAG] &= ~(PARENB | CSIZE)
		s.attr.staged[CFLAG] |= CS8
		# Clear all POSIX.1-2017 local mode flags.
		s.attr.staged[LFLAG] &= ~(ECHO | ECHOE | ECHOK | ECHONL | ICANON | IEXTEN | ISIG | NOFLSH | TOSTOP)
		# POSIX.1-2017, 11.1.7 Non-Canonical Mode Input Processing,
		# Case B: MIN>0, TIME=0
		# A pending read shall block until MIN (here 1) bytes are received,
		# or a signal is received.
		s.attr.staged[CC] = list(s.attr.staged[CC])
		s.attr.staged[CC][VMIN] = 1
		s.attr.staged[CC][VTIME] = 0
		s.update(when)

	def setcbreak(s,when=TCSAFLUSH):
		"""Put terminal into cbreak mode."""
		# this code was lifted from the tty module and adapted for being a method
		s.attr.stage()
		# Do not echo characters; disable canonical input.
		s.attr.staged[LFLAG] &= ~(ECHO | ICANON)
		# POSIX.1-2017, 11.1.7 Non-Canonical Mode Input Processing,
		# Case B: MIN>0, TIME=0
		# A pending read shall block until MIN (here 1) bytes are received,
		# or a signal is received.
		s.attr.staged[CC] = list(s.attr.staged[CC])
		s.attr.staged[CC][VMIN] = 1
		s.attr.staged[CC][VTIME] = 0
		s.update(when)

	def echo(s,enable=False):
		s.attr.stage()
		s.attr.staged[3] &= ~s.ECHO
		if enable:
			s.attr.staged[3] |= s.ECHO
		s.update()

	def canonical(s,enable):
		s.attr.stage()
		s.attr.staged[3] &= ~s.ICANON
		if enable:
			s.attr.staged[3] |= s.ICANON
		s.update()

	def __mode__(s,mode=None):
		def Normal():
			# s.cursor.show(True)
			s.echo(True)
			s.canonical(True)
			s.tcsetattr(s.TCSAFLUSH, s.attr.init)
			s._mode = nmodi.get('normal')

		def Ctl():
			# s.cursor.show(False)
			s.echo(False)
			s.canonical(False)
			s._mode = nmodi.get('ctl')

		nmodi={'normal' : 1,'ctl': 2 }
		fmodi = {
			1   :  Normal,
			2   :  Ctl,
		}
		if mode is not None and mode != s._mode:
			nmode=nmodi.get(mode)
			fmodi.get(nmode)()
		return s._mode
		
	def update(s,when=TCSAFLUSH):
		s.tcsetattr(when, s.attr.staged)
		s.attr.update(s.tcgetattr())

	def ansi(s, ansi, parser):
		s.setcbreak()
		try:
			sys.stdout.write(ansi)
			sys.stdout.flush()
			result = parser()
		finally:
			s.tcsetattr(s.TCSAFLUSH, s.live)
		return result
#
