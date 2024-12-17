#!/usr/bin/env python
import sys
from select import select

from Clict import Clict


class KBTty(Clict):
	def __init__(__s,parent=None,term=None):
		super().__init__()
		__s.term=parent.term or term

	@property
	def event(__s):
		return any(select([__s.term.fd], [], [], 0))

	
	def read(__s,n=1):
		buffer=[]
		for i in range(n):
			buffer+=[sys.stdin.read(1)]
		sys.stdin.flush()
		return buffer

	def getch(__s):
		if len(__s.buffer)!=0:
			c=__s.buffer[-1]
			__s.flush()
	def flush(__s):
		__s.buffer=[]
		sys.stdin.flush()





