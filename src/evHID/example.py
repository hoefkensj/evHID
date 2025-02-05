#!/usr/bin/env python

from evHID import KBEV
from signal import pause
from evHID.Types.data import Callback


## how this shit should work ideallly
# keypress-> triggers event trought device listener
# -> checks for readable on stdin if so the key was meant for us
# -> reads key from the device buffer
# -> uses that to clear number of chars from stdin
# -> key gets added to global buffer
# -> getkey pops last key from buffer
# -> getkeys gets all from buffer and wipes buffer


def KD(s):
	colr = '\x1b[{};60H\x1b[K\x1b[3{}m{}\x1b[60G{}   \x1b[80G{}\x1b[100G0x{}\x1b[m'
	window=[];n=0
	def kd(key):
		nonlocal window
		nonlocal n
		n+=1
		c = 2 if int(bin(n)[-1]) else 5
		window += [[c,n, key.name, key.char, key.value]]
		if len(window) > 5:
			window.pop(0)
		for i, line in enumerate(window):
			print(colr.format(i+6,*line))
	return kd


if __name__ == '__main__':
	coll = '\x1b[{};59H\x1b[1K\x1b[G\x1b[3{}m{} {}  \x1b[20G{}\x1b[40G0x{}\x1b[m'

	cb={
		'fn'    :  KD     ,
		'event' : 'kd'    ,
		'scope' : 'global',
		'vars'  : {'window': []}
	}
	with KBEV(cb=[Callback(**cb)]) as kb:
		print('\x1b[4;1H\x1b[1;32mLOCAL DETECT\x1b[60G\x1b[1;34mGLOBAL DETECT:\x1b[m')
		print('\x1b[5;1H\x1b[1mN   NAME\x1b[20GCHAR\x1b[40GKEYCODE\x1b[60GN   NAME\x1b[80GCHAR\x1b[100GKEYCODE\x1b[m')
		window=[];n=0
		while True:
			if kb.event():
				key=kb.key(); n+=1
				c=3 if int(bin(n)[-1]) else 4
				window+=[[c,n,key.name,key.char,key.value]]
				if len(window)>5:
					window.pop(0)
				for i,line in enumerate(window):
					print(coll.format(i+6,*line))
			pause()


