#!/usr/bin/env python
from select import select
from Clict import Clict
from pynput import keyboard
from evHID.Term import Term
from signal import SIGUSR1
import os


import sys

class KBDev(Clict):
	def __init__(__s,term=None):
		super().__init__()
		__s.term=term
		__s._buffer=[]
		__s._current=[]
		__s._history=[*(None,)*64]
		__s.default.KD=__s.__default_KD__
		__s.default.KU=__s.__default_KU__
		__s.onpress=__s.default.KD
		__s.onrelease=__s.default.KU
		__s.listener=__s.__listener__
		__s._buffersize=0
		__s.event=False
		__s.signal=lambda:__s.__signal__()
		__s.__create__()

	def __create__(__s):
		__s.listener = keyboard.Listener(on_press=__s.getKD(),on_release=__s.getKU())
		__s.start=__s.listener.start
		__s.join=__s.listener.join
		__s.stop=__s.listener.stop


	def __enter__(__s):
		__s.start()
		return __s

	def __exit__(__s,*a,**k):
		__s.listener.stop()

	def setKD(__s,fn):
		__s.onpress=fn
	def getKD(__s):
		return lambda key : __s.onpress(key)

	def setKU(__s,fn):
		__s.onrelease=fn
	def getKU(__s):
		return lambda key : __s.onrelease(key)

	def __default_KD__(__s,key):
		__s._current += [key]
		__s._current = [*set(__s._current)]
		__s._history =[*__s._history[1:] + [(key, 1)]]
		__s._buffer += [key]
		__s._buffersize+=1
		__s.event=True

	def __default_KU__(__s,key):
		__s._history += [(key, 0)]
		if key in __s._current:
			__s._current.remove(key)

	def __listener__(__s):
		return

	def __signal__(__s):
		os.kill(__s.term.pid, SIGUSR1)

	def buffer(__s):
		while True:
			if __s.event:
				ret=[__s._buffer.pop() for i in range(__s._buffersize)]
				__s._buffersize=len(__s._buffer)
				__s.event=False
				break
		return ret




class KBTty(Clict):
	def __init__(__s,term=None):
		super().__init__()
		__s.term=term
		__s.buffer=[]
		__s.history=[*(None,)*64]
		__s.event=__s.__event__
		__s.count=0
		__s._event=0

	def __event__(__s):
		state=any(select([sys.stdin], [], [], 0))
		__s._event=__s._event or bool(state)
		__s.count+=int(state)
		return __s._event
	def read(__s,n=1):
		if __s.event():
			buffer=[]
			for i in range(n):
				buffer+=[sys.stdin.read(1)]
			__s.history =[*__s.history[1:] + buffer]
			__s.last=repr(''.join(buffer))
			__s.buffer=[buffer]
		__s._event=0

	# def getKey(__s):
	# 	__s.read(1)
	# 	if len(__s.buffer)>0:
	# 	key=__s.buffer.pop(-1)



	def getch(__s):
		if len(__s.buffer)!=0:
			c=__s.buffer[-1]
			__s.flush()
	def flush(__s):
		__s.buffer=[]


class KBEV_Posix(Clict):
	def __init__(__s,*a,**k):
		super().__init__()
		__s.term = Term()
		__s.dev = KBDev(__s.term)
		__s.tty = KBTty(__s.term)
		__s.event=__s.tty.event
		__s.history.key=[*(None,)*64]
		__s.history.code=[*(None,)*64]
		__s.history.stdin=[*(None,)*64]
		__s.last.key=None
		__s.last.code=None
		__s.last.stdin=None
		__s.term.mode('ctl')
		__s.event=lambda : __s.tty.event()





	def __enter__(__s):
		__s.dev.start()
		return __s

	# 	return
	# 	__s
	def __exit__(__s,*a,**k):
		__s.dev.__exit__()




	def getKey(__s):
		key = __s.__getKBKey__()

		if 'name' in dir(key):
			rkey=str(key.name).split('.')[-1]

		elif 'char' in dir(key):
			rkey = key.char
		else:
			print(f'\x1b[8;1H\x1b[K{key}')
			print(f'\x1b[9;1H\x1b[K{dir(key)}')
		return rkey

	def getCode(__s):
		key=__s.__getKBKey__()
		# sys.stdin.read(key.clr)
		if 'value' in dir(key):
			if key == keyboard.Key.space:
				code=ord(str(key.value)[1:-1])
			else:
				code=int(str(key.value)[1:-1])
		elif 'char' in dir(key):
			code = ord(key.char)
		else:
			print(f'\x1b[8;1H\x1b[K{key}')
			print(f'\x1b[9;1H\x1b[K{dir(key)}')

		return code
	def __getKBKey__(__s):
		def getkbkey():
			K=keyboard.Key
			key=__s.dev.buffer()[-1]
			if 'value' in dir(key):
				if key in [K.space,K.enter,K.home,K.end,K.page_down,K.page_up]:
					__s.tty.read(1)
					stdin=__s.tty.buffer[0]
				else:
					key.clr=3
					sys.stdin.read(3)
			elif 'char' in dir(key):
				key.clr=1
				sys.stdin.read(1)
			else:
				print(f'\x1b[8;1H\x1b[K{key}')
				print(f'\x1b[9;1H\x1b[K{dir(key)}')
			return key
		keyc=None
		while not keyc:
			if len(__s.kbdev.buffer)>0:
				keyc=getkbkey()
				break
			else:
				__s.kbdev.buffer.clear()
			# time.sleep(1e-6)
		__s.kbdev.buffer.clear()
		return keyc

from time import sleep
from signal import pause
if __name__ == '__main__':
	term=Term()
	term.mode('ctl')
	kbdev=KBDev()
	with kbdev as kb:
		while True:
			if kb.event:
				key=kb.buffer()[0]
				print(str(key))
				print(type(key))

				if 'value' in dir(key):
	 				print('val:',key.value)

				if 'char' in dir(key):
					print('char:', key.char)
					
					if str(key.char)=='\n':
						print('works')
					if str(key.char)=='d':
						print('works')
					print()
				if str(repr(key))==' ':
					print('works')

				

		#
		# def handle_signal(signum, frame):
		# 	print(f"Custom signal {signum} received, handling the signal.")
		# 	exit(0)
		#
		#
		# # Set the signal handler for SIGUSR1
		# signal.signal(signal.SIGUSR1, handle_signal)

			# print('..',end='',flush=True)
			# sleep(0.5)
			# print('..',end='',flush=True)
			# sleep(0.5)
			# print('..',end='',flush=True)
