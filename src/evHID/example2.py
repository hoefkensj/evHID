#!/usr/bin/env python
from evHID import KBEV
from signal import pause
from evHID import Callback
import sys
EXIT=0
def cbExit(key):
	def cbexit(key):
		global EXIT
		if key.char == 'q':
			print('q')
			EXIT=1
	return cbexit

cb=Callback(fn=cbExit)
cb.event='kd'
cb.scope='global'

with KBEV(cb=[cb]) as kb:
	i=0
	while not EXIT:
		if kb.event():
			key=kb.key()
			if key == 'left':
				print(f'\x1b[10;10H{(i:=i-1)}')
			if key == 'right':
				print(f'\x1b[10;10H{(i:=i+1)}')
		
		pause()
