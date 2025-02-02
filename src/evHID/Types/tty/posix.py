#!/usr/bin/env python
import sys
from select import select

from Clict import Clict


class KBTty(Clict):
	def __init__(__s,parent=None,term=None):
		super().__init__()
		__s.term=parent.term or term
		__s._buffer=[]
		__s._event=False

	@property
	def event(__s):
		__s._event=select([__s.term.fd], [], [], 0)[0]
		return __s._event

		# if event:
		# 	while event:
		# 		__s._buffer += [sys.stdin.read(1)]
		# 		event = select([__s.term.fd], [], [], 0)[0]

	
	def read(__s):
		if __s.event:
			while __s.event:
				__s._buffer += [sys.stdin.read(1)]
				# __s._event = select([__s.term.fd], [], [], 0)[0]
		return __s._buffer

	def getch(__s):
		if len(__s.buffer)!=0:
			c=__s.buffer[-1]
			__s.flush()
	def flush(__s):
		__s.buffer=[]
		sys.stdin.flush()





