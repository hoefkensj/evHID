#!/usr/bin/env python
from evHID.hid.kbev import KBEV_Posix as KBEV
from evHID.term.posix import  Term
from evHID.Types.callback import  Callback
from signal import pause
import sys
EXIT=0
def cbExit(s):
	def cbexit(key):
		global EXIT
		if key.char == 'q':
			print('q')
			EXIT=1
	return cbexit

cb=Callback(fn=cbExit)
cb.scope+=[Callback.Scope.GLOBAL]
cb.event+=[Callback.Event.DOWN]

term=Term()
with KBEV(term=term,cb=cbExit) as kb:
	i=0
	while not EXIT:
		if kb.event():
			key=kb.key()
			print(kb.key.name)
			if key == 'left':
				print(f'\x1b[10;10H{(i:=i-1)}')
			if key == 'right':
				print(f'\x1b[10;10H{(i:=i+1)}')
		
