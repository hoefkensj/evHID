#!/usr/bin/env python
from evHID import KBEV
from pynput import keyboard
### how this shit should work ideallly
# keypress-> triggers event trought device listener
# -> checks for readable on stdin if so the key was meant for us
# -> reads key from the device buffer
# -> uses that to clear number of chars from stdin
# -> key gets added to global buffer
# -> getkey pops last key from buffer
# -> getkeys gets all from buffer and wipes buffer

def kd(*a,**k):
	print(*a,**k)
	
from time import sleep
if __name__ == '__main__':
	pynspace=keyboard.Key.space
	

	with KBEV(kd=kd) as kb:
		while True:
			if kb.event():
				key=kb.key()
				if key ==pynspace:
					print(' spaceman ')
				else:
					print(key)
			sleep(0.0005)

