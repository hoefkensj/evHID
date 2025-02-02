#!/usr/bin/env python
from evHID import KBEV
from pynput import keyboard
from signal import pause
import sys
EXIT=0
def cbexit(key):
	global EXIT
	if key.char == 'q':
		print('q')
		EXIT=1


with KBEV(kd=cbexit) as kb:
	i=0
	while not EXIT:
		if kb.event():
			key=kb.key()
			if key == 'left':
				print(f'\x1b[10;10H{(i:=i-1)}')
			if key == 'right':
				print(f'\x1b[10;10H{(i:=i+1)}')
		
		pause()
