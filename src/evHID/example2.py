#!/usr/bin/env python
from evHID import KBEV
from signal import pause
from evHID import Callback
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

with KBEV() as kb:
	i=0
	while not EXIT:
		if kb.event():
			print(kb.key.namedasdfss)
			time.sleep(500)
			# if key == 'left':
			# 	print(f'\x1b[10;10H{(i:=i-1)}')
			# if key == 'right':
			# 	print(f'\x1b[10;10H{(i:=i+1)}')
		
